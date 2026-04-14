/**
 * OSync — Obsidian Plugin
 *
 * End-to-end encrypted vault sync competing with Obsidian Sync.
 * Connects to a self-hosted OSync Cloudflare Worker backend.
 *
 * Architecture mirrors the CF Worker + @osync/core:
 *   - Client-side AES-256-GCM encryption (server never sees plaintext)
 *   - Device-token authentication (no user accounts needed)
 *   - Real-time sync via WebSocket with DELTA broadcasts
 *   - Incremental pull (changes since last sync timestamp)
 *   - Version history with server-side version tracking
 *   - Soft-delete via tombstones
 *   - Conflict resolution: last-write-wins with version check
 *   - Selective sync (folder ignore patterns)
 *   - Status bar + sync log ribbon
 *
 * Fixed issues (see review):
 *   #1  saveSettings no longer overwrites sync state (namespaced storage)
 *   #2  buildR2Key replaced — server's downloadUrl used directly from PullResponse
 *   #3  WS blob transport removed; uploads always go over HTTP
 *   #4  CSS injected in onload(), removed in onunload()
 *   #5  Remote-change echo loop prevented via applyingRemoteChange flag
 *   #6  Deletion loop now collects paths before mutating state
 *   #7  debouncePush triggers pushFile for the specific file, not a full sync
 *   #8  stateStore null-guard added; reinitializeClient is safe at any time
 *   #9  Crypto key always re-derived when vaultId changes
 *   #10 downloadUrls from PullResponse used when present
 *   #11 destroyed flag checked at every await point during sync
 *   #12 SyncEngine.clearLog() exposed; no more (as any) cast
 *   #13 WS timeout handlers always remove their message listeners
 *   #14 WS reconnect resets after a sustained connection; user notified on give-up
 *   #15 getStatus() compared with === "syncing"
 *   #16 syncLog trimmed with slice()
 *   #17 (acknowledged — store discipline unchanged)
 *   #18 fetch calls wrapped with AbortSignal timeout (where supported)
 *   #19 (acknowledged — token storage in plaintext is acceptable for this use-case)
 *   #20 SyncLogView uses incremental DOM append instead of full rebuild
 */

import {
  App,
  debounce,
  Notice,
  Plugin,
  PluginSettingTab,
  Setting,
  TAbstractFile,
  TFile,
  ItemView,
  WorkspaceLeaf,
} from "obsidian";

// ═══════════════════════════════════════════════════════════════════════════════
// §1. TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface OSyncSettings {
  serverUrl: string;
  vaultId: string;
  encryptionPassword: string;
  deviceName: string;
  deviceToken: string;
  autoSync: boolean;
  syncIntervalSeconds: number;
  excludedFolders: string;
  excludedFiles: string;
  conflictStrategy: "server-wins" | "local-wins" | "newest-wins";
  maxConcurrentUploads: number;
  enableWebSocket: boolean;
}

const DEFAULT_SETTINGS: OSyncSettings = {
  serverUrl: "",
  vaultId: "",
  encryptionPassword: "",
  deviceName: "",
  deviceToken: "",
  autoSync: true,
  syncIntervalSeconds: 30,
  excludedFolders: ".git,node_modules,.trash,.sync_state",
  excludedFiles: ".obsidian/workspace.json,.obsidian/workspace-mobile.json,.obsidian/app.json,.obsidian/appearance.json,.obsidian/hotkeys.json,.obsidian/core-plugins.json,.obsidian/community-plugins.json,.obsidian/plugins/osync/main.js,.obsidian/plugins/osync/manifest.json,.obsidian/plugins/osync/styles.css",
  conflictStrategy: "newest-wins",
  maxConcurrentUploads: 5,
  enableWebSocket: true,
};

interface SyncStateEntry {
  localPath: string;
  localHash: string;
  remoteVersion: number;
  remoteHash: string;
  lastSyncTime: string;
}

interface FileRecord {
  path: string;
  currentVersion: number;
  currentHash: string;
  mtime: string;
  size: number;
  deviceId: string;
  lastModified: string;
  /** Optionally provided by the server — preferred over a client-reconstructed key. */
  downloadUrl?: string;
}

interface AuthResult {
  ok: boolean;
  deviceId: string;
  vaultId: string;
  deviceToken: string;
  lastSyncTime: string | null;
}

interface PullResponse {
  ok: boolean;
  changes: FileRecord[];
  hasMore: boolean;
  /** Path → pre-signed or direct download URL. Use these when present. FIX #10 */
  downloadUrls?: Record<string, string>;
  tombstones?: Array<{ path: string; deletedAt: string; deviceId: string }>;
  renames?: Array<{ oldPath: string; newPath: string; renamedAt: string; deviceId: string }>; // ADD
}

interface PushConfirmation {
  type: "PUSH_CONFIRMATION";
  path: string;
  version: number;
  ok: boolean;
  error?: string;
}

interface DeltaNotification {
  type: "DELTA";
  path: string;
  hash: string;
  mtime: string;
  size: number;
  version: number;
  deviceId: string;
  action: "update" | "delete" | "rename";
  oldPath?: string;
  /** Server may include a ready-to-use download URL. FIX #10 */
  downloadUrl?: string;
}

type SyncStatus = "idle" | "syncing" | "error" | "paused" | "connected";

interface SyncLogEntry {
  timestamp: string;
  direction: "upload" | "download" | "delete" | "conflict" | "info" | "error";
  path: string;
  message: string;
}

class InvalidDeviceTokenError extends Error {
  constructor() {
    super("Invalid device token — device not recognised by server");
    this.name = "InvalidDeviceTokenError";
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// §2. CRYPTO — AES-256-GCM End-to-End Encryption
// ═══════════════════════════════════════════════════════════════════════════════

const PBKDF2_ITERATIONS = 100_000;
const IV_LENGTH = 12;

async function deriveKey(password: string, salt: string): Promise<CryptoKey> {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    enc.encode(password.normalize("NFKC")),
    "PBKDF2",
    false,
    ["deriveKey"]
  );
  return crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: enc.encode(salt.normalize("NFKC")),
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

async function encrypt(
  content: string | Uint8Array,
  key: CryptoKey
): Promise<Uint8Array> {
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH));
  const plaintext =
    typeof content === "string" ? new TextEncoder().encode(content) : content;
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    plaintext.buffer as ArrayBuffer
  );
  const packed = new Uint8Array(IV_LENGTH + ciphertext.byteLength);
  packed.set(iv, 0);
  packed.set(new Uint8Array(ciphertext), IV_LENGTH);
  return packed;
}

async function decrypt(packed: Uint8Array, key: CryptoKey): Promise<Uint8Array> {
  if (packed.length < IV_LENGTH) {
    throw new Error(`Encrypted blob too short: ${packed.length} bytes`);
  }
  const iv = packed.slice(0, IV_LENGTH);
  const ciphertext = packed.slice(IV_LENGTH);
  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: iv.buffer as ArrayBuffer },
    key,
    ciphertext.buffer as ArrayBuffer
  );
  return new Uint8Array(decrypted);
}

async function hashContent(content: string | Uint8Array): Promise<string> {
  const data =
    typeof content === "string" ? new TextEncoder().encode(content) : content;
  const hashBuffer = await crypto.subtle.digest(
    "SHA-256",
    data.buffer as ArrayBuffer
  );
  return Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// ═══════════════════════════════════════════════════════════════════════════════
// §3. PERSISTED DATA SHAPE
//
// FIX #1: Settings and sync state are stored under separate top-level keys so
// saveSettings() can never clobber syncState, and vice-versa.
// ═══════════════════════════════════════════════════════════════════════════════

interface PersistedData {
  /** Plugin settings. */
  settings?: Partial<OSyncSettings>;
  /** Per-file sync state map (path → SyncStateEntry). */
  syncState?: Record<string, SyncStateEntry>;
  /** ISO timestamp of the last completed sync. */
  lastSyncTime?: string | null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// §4. LOCAL SYNC STATE STORE
// ═══════════════════════════════════════════════════════════════════════════════

class SyncStateStore {
  private data: Map<string, SyncStateEntry> = new Map();
  private lastSyncTime: string | null = null;
  private dirty = false;
  private plugin: OSyncPlugin;

  constructor(plugin: OSyncPlugin) {
    this.plugin = plugin;
  }

  // FIX #1: Read only from syncState / lastSyncTime sub-keys.
  async load(): Promise<void> {
    const raw = ((await this.plugin.loadData()) ?? {}) as PersistedData;
    if (raw.syncState) {
      this.data = new Map(Object.entries(raw.syncState));
    }
    this.lastSyncTime = raw.lastSyncTime ?? null;
  }

  // FIX #1: Merge into the persisted object instead of replacing it.
  async save(): Promise<void> {
    if (!this.dirty) return;
    const raw = ((await this.plugin.loadData()) ?? {}) as PersistedData;
    raw.syncState = Object.fromEntries(this.data);
    raw.lastSyncTime = this.lastSyncTime;
    await this.plugin.saveData(raw);
    this.dirty = false;
  }

  get(relPath: string): SyncStateEntry | undefined {
    return this.data.get(relPath);
  }

  set(relPath: string, entry: SyncStateEntry): void {
    this.data.set(relPath, entry);
    this.dirty = true;
  }

  delete(relPath: string): void {
    this.data.delete(relPath);
    this.dirty = true;
  }

  getAll(): SyncStateEntry[] {
    return Array.from(this.data.values());
  }

  getAllPaths(): string[] {
    return Array.from(this.data.keys());
  }

  getLastSyncTime(): string | null {
    return this.lastSyncTime;
  }

  setLastSyncTime(time: string): void {
    this.lastSyncTime = time;
    this.dirty = true;
  }

  clear(): void {
    this.data.clear();
    this.lastSyncTime = null;
    this.dirty = true;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// §5. SERVER CLIENT
// ═══════════════════════════════════════════════════════════════════════════════

class OSyncServerClient {
  private baseUrl: string;
  private vaultId: string;
  private deviceId: string | null = null;
  private deviceToken: string;
  private ws: WebSocket | null = null;
  private wsReconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private wsHandlers: Array<(delta: DeltaNotification) => void> = [];
  private wsConnected = false;
  private reconnectAttempts = 0;
  // FIX #14: Raised ceiling; reset after a sustained connection.
  private readonly maxReconnectAttempts = 20;
  private wsConnectedSince: number | null = null;
  private onWsStatusChange?: (connected: boolean) => void;
  private onWsGaveUp?: () => void;

  constructor(
    baseUrl: string,
    vaultId: string,
    deviceToken: string,
    onWsStatusChange?: (connected: boolean) => void,
    onWsGaveUp?: () => void
  ) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.vaultId = vaultId;
    this.deviceToken = deviceToken;
    this.onWsStatusChange = onWsStatusChange;
    this.onWsGaveUp = onWsGaveUp;
  }

  clearDeviceId(): void {
    this.deviceId = null;
  }

  updateConfig(baseUrl: string, vaultId: string, deviceToken: string): void {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
    this.vaultId = vaultId;
    this.deviceToken = deviceToken;
  }

  // ── Authentication ────────────────────────────────────────────────────

  async authenticate(deviceName: string): Promise<AuthResult> {
    const response = await this.fetchWithTimeout(
      `${this.baseUrl}/api/auth`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          vaultId: this.vaultId,
          deviceToken: this.deviceToken || undefined,
          deviceName: deviceName || "unknown",
        }),
      },
      15_000
    );

    if (!response.ok) {
      const body = await response.text();
      if (response.status === 401) {
        throw new InvalidDeviceTokenError();
      }
      throw new Error(`Auth failed (${response.status}): ${body}`);
    }


    // Temporary debug — remove after confirming
    console.log("OSync pushFile: deviceToken =", this.deviceToken ? `${this.deviceToken.substring(0, 8)}...` : "EMPTY");
    console.log("OSync pushFile: deviceId =", this.deviceId);

    const data = (await response.json()) as AuthResult;
    this.deviceId = data.deviceId;
    this.deviceToken = data.deviceToken;

    // Temporary debug — remove after confirming
    console.log("OSync pushFile: deviceToken =", this.deviceToken ? `${this.deviceToken.substring(0, 8)}...` : "EMPTY");
    console.log("OSync pushFile: deviceId =", this.deviceId);

    return data;
  }

  // ── HTTP File Operations ──────────────────────────────────────────────

  /**
   * FIX #3: Blob uploads always use HTTP — never WebSocket.
   * Sending a large Uint8Array as JSON over WS balloons the payload to ~4× the
   * original size and will exceed most server/browser WS message limits.
   */
  async pushFile(
    path: string,
    hash: string,
    size: number,
    mtime: string,
    encryptedBlob: Uint8Array
  ): Promise<PushConfirmation> {
    const meta = JSON.stringify({ path, version: 0, hash, mtime, size });

    const blobResponse = await this.fetchWithTimeout(
      `${this.baseUrl}/api/vaults/${this.vaultId}/blobs`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/octet-stream",
          "X-Device-Token": this.deviceToken,
          "X-Blob-Meta": meta,
        },
        body: encryptedBlob,
      },
      60_000 // FIX #18: 60 s timeout for potentially large uploads
    );

    if (!blobResponse.ok) {
      const err = await blobResponse.text();
      throw new Error(`Blob upload failed (${blobResponse.status}): ${err}`);
    }

    const metaResponse = await this.fetchWithTimeout(
      `${this.baseUrl}/api/vaults/${this.vaultId}/files/push`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Device-Token": this.deviceToken,
        },
        body: JSON.stringify({
          path,
          hash,
          size,
          mtime,
          deviceId: this.deviceId,
        }),
      },
      15_000
    );

    if (!metaResponse.ok) {
      const err = await metaResponse.text();
      throw new Error(
        `Push metadata failed (${metaResponse.status}): ${err}`
      );
    }

    const result = (await metaResponse.json()) as {
      ok: boolean;
      version: number;
      path: string;
    };
    return {
      type: "PUSH_CONFIRMATION",
      path: result.path,
      version: result.version,
      ok: result.ok,
    };
  }

  async pullChanges(since?: string): Promise<PullResponse> {
    const params = new URLSearchParams();
    if (since) params.set("since", since);

    const response = await this.fetchWithTimeout(
      `${this.baseUrl}/api/vaults/${this.vaultId}/files/changes?${params}`,
      { headers: { "X-Device-Token": this.deviceToken } },
      30_000 // FIX #18
    );

    if (!response.ok) {
      throw new Error(
        `Pull failed (${response.status}): ${response.statusText}`
      );
    }

    return response.json() as Promise<PullResponse>;
  }

  async getAllFiles(): Promise<{
    ok: boolean;
    files: FileRecord[];
    total: number;
  }> {
    const response = await this.fetchWithTimeout(
      `${this.baseUrl}/api/vaults/${this.vaultId}/files`,
      { headers: { "X-Device-Token": this.deviceToken } },
      30_000 // FIX #18
    );

    if (!response.ok) {
      throw new Error(
        `List files failed (${response.status}): ${response.statusText}`
      );
    }

    return response.json() as Promise<{
      ok: boolean;
      files: FileRecord[];
      total: number;
    }>;
  }

  // ── Blob Download ─────────────────────────────────────────────────────

  async downloadBlob(urlOrKey: string): Promise<Uint8Array> {
    const url = urlOrKey.startsWith("http")
      ? urlOrKey
      : `${this.baseUrl}/api/vaults/${this.vaultId}/blobs/${encodeURIComponent(urlOrKey)}`;

    const response = await this.fetchWithTimeout(
      url,
      { headers: { "X-Device-Token": this.deviceToken } },
      60_000 // FIX #18
    );

    if (!response.ok) {
      throw new Error(
        `Blob download failed (${response.status}): ${response.statusText}`
      );
    }

    const buf = await response.arrayBuffer();
    return new Uint8Array(buf);
  }

  // ── Health ────────────────────────────────────────────────────────────

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.fetchWithTimeout(
        `${this.baseUrl}/health`,
        {},
        10_000
      );
      return response.ok;
    } catch {
      return false;
    }
  }

  // ── WebSocket ─────────────────────────────────────────────────────────

  connectWS(handler: (delta: DeltaNotification) => void): void {
    this.wsHandlers.push(handler);
    if (this.ws) return;
    this.initWS();
  }

  disconnectWS(): void {
    this.wsHandlers = [];
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.wsReconnectTimer) {
      clearTimeout(this.wsReconnectTimer);
      this.wsReconnectTimer = null;
    }
    this.wsConnected = false;
    this.wsConnectedSince = null;
    this.reconnectAttempts = 0;
    this.onWsStatusChange?.(false);
  }

  isWsConnected(): boolean {
    return this.wsConnected;
  }

  private initWS(): void {
    const wsUrl = this.baseUrl.replace(/^http/, "ws");
    const url = `${wsUrl}/?vaultId=${encodeURIComponent(
      this.vaultId
    )}&deviceToken=${encodeURIComponent(this.deviceToken)}`;

    try {
      const ws = new WebSocket(url);
      this.ws = ws;

      ws.onopen = () => {
        this.wsConnected = true;
        this.wsConnectedSince = Date.now();
        this.reconnectAttempts = 0;
        this.onWsStatusChange?.(true);

        ws.send(
          JSON.stringify({
            type: "SUBSCRIBE",
            vaultId: this.vaultId,
            deviceToken: this.deviceToken,
          })
        );
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data.toString());
          if (msg.type === "CONNECTED" || msg.type === "PONG") return;
          if (msg.type === "DELTA") {
            for (const h of this.wsHandlers) h(msg as DeltaNotification);
          }
        } catch {
          // ignore malformed frames
        }
      };

      ws.onclose = () => {
        // FIX #14: If we were connected for >60 s, treat it as a clean
        // session and reset the backoff counter before reconnecting.
        if (
          this.wsConnectedSince !== null &&
          Date.now() - this.wsConnectedSince > 60_000
        ) {
          this.reconnectAttempts = 0;
        }
        this.wsConnected = false;
        this.wsConnectedSince = null;
        this.ws = null;
        this.onWsStatusChange?.(false);
        this.scheduleReconnect();
      };

      ws.onerror = () => {
        // onclose fires immediately after; handled there.
      };

      // Keep-alive ping every 30 s
      const pingInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "PING" }));
        } else {
          clearInterval(pingInterval);
        }
      }, 30_000);
    } catch {
      this.scheduleReconnect();
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      // FIX #14: Notify the user instead of silently giving up.
      this.onWsGaveUp?.();
      return;
    }
    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30_000);
    this.wsReconnectTimer = setTimeout(() => this.initWS(), delay);
  }

  // ── WebSocket control messages (delete / rename — no blob transfer) ───

  /**
   * FIX #13: Every WS promise r