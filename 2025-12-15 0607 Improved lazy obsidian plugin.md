---
created: 2025-12-15
tags:
  - note
  - journal
  - ideas
  - plugins
  - developments
day: "[[2025-12-15]]"
---
## 🚀 The Optimized Plugin Architecture

This plugin manages the startup sequence of Obsidian by categorizing enabled plugins into five distinct loading behaviors.

### 1. The Five Loading Types

The core of the plugin revolves around a single dropdown per plugin. Switching types is seamless, and custom values are preserved even if the type is toggled.

- **Instant:** Loads immediately upon Obsidian startup (default behavior).
    
- **Short Delayed:** Loads after a global $x$ delay (e.g., 5s). Best for common utilities.
    
- **Long Delayed:** Loads after a global $y$ delay (e.g., 20s). Best for heavy indexing plugins.
    
- **Custom:** Allows a specific, per-plugin delay in seconds. Switching a plugin to a custom value automatically sets its type to "Custom."
    
- **Triggered (Replaces Deferred):** The plugin remains unloaded until the user manually invokes it.
    
    - **How it works:** A "Lazy Command Palette" command allows the user to pick a plugin to load on the fly.
        
    - **Feedback:** Displays a "Loading [Plugin Name]..." notice to manage user expectations during initialization.
        

---

### 2. Guardrails & Intelligence

To prevent user error and ensure the "Lazy" system actually works, the following logic is implemented:

- **The Time-Sanity Check:** * If a user sets the **Short Delay** global value higher than the **Long Delay**, the plugin will automatically swap them or flag an error. User input is never fully trusted.
    
- **The Specificity Hierarchy:**
    
    - When a plugin is set to **Short** or **Long**, it follows the global variables.
        
    - If a user inputs a specific number into the time field, the plugin type automatically switches to **Custom**. If they switch back to "Short," the custom value is hidden but saved in the background.
        
- **Startup Priority (The "Race" Guardrail):**
    
    - The plugin monitors its own position in the loading order. It will suggest (or force) itself to the top of the `community-plugins.json` list to ensure it can control the other plugins before they start their own load sequences.
        

---

### 3. Streamlined Settings & UX

- **No "Disabled" Redundancy:** We have removed the "Disabled" type. Users should use Obsidian’s native toggle for disabling plugins to avoid "Split Truth" (where a plugin looks "On" in settings but is "Off" in the loader).
    
- **Command Pollution Control:** By using **Triggered** loading, plugins that are rarely used don't clutter the Command Palette or the Ribbon until they are actually needed.
    
- **One-Click Reset with Confirmation:**
    
    - A "Restore Defaults" button is available, but it is protected by a confirmation modal to prevent the accidental loss of a complex, hand-tuned loading setup.
        

---

### 4. Technical Data Structure

To support the "hidden but saved" custom values and the trigger logic, the settings are stored as follows:

TypeScript

```
interface LazyLoaderSettings {
    globalShortDelay: number; // Default 'x'
    globalLongDelay: number;  // Default 'y'
    pluginRules: Record<string, {
        id: string;
        type: 'instant' | 'short' | 'long' | 'custom' | 'triggered';
        customTime: number; // Stored even if type is 'short'
        lastUsedTrigger?: string; 
    }>;
}
```

---

**Next Step:** Since we've finalized the flow, would you like me to help you write the **TypeScript class** for the Settings Tab that handles the "Auto-switch to Custom" logic when a user types in a number?