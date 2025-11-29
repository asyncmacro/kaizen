#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------------
# Obsidian Vault Git Sync Script
# - Safe for Android (Termux) + Desktop
# - Handles conflicts gracefully
# - No empty commits
# - Stash → Pull → Reapply → Commit → Push
# - Timestamp auto commit message
# -------------------------------------------------------------

timestamp=$(date "+%Y-%m-%d %H:%M:%S")

echo "📦 Starting Obsidian Vault Sync..."
echo "⏱  Timestamp: $timestamp"
echo ""

# Ensure we are inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ This directory is not a git repository."
  exit 1
fi

# Step 1: Stash local changes if any
if ! git diff-index --quiet HEAD --; then
  echo "📌 Local changes detected → stashing temporarily..."
  git stash push -m "obsidian-auto-stash-$timestamp"
  stashed=1
else
  stashed=0
fi

echo "🔄 Pulling remote changes (merging)..."
git pull --no-rebase --autostash || {
  echo "❌ Pull failed. Resolve conflicts manually."
  exit 1
}

# Step 2: Reapply stash if created
if [ "$stashed" -eq 1 ]; then
  echo "📌 Reapplying stashed changes..."
  if ! git stash pop; then
    echo "⚠️ Conflict occurred while applying stash!"
    echo "🛑 Please resolve manually, then run script again."
    exit 1
  fi
fi

# Step 3: Check if anything actually changed
if git diff-index --quiet HEAD --; then
  echo "✨ Nothing to commit — vault is already fully synced."
  echo "📤 Still pushing in case remote has diverged..."
  git push || {
    echo "❌ Push failed. Fix manually."
    exit 1
  }
  echo "✅ Sync complete."
  exit 0
fi

# Step 4: Add + commit
echo "➕ Adding updated files..."
git add -A

echo "📝 Committing changes..."
git commit -m "vault-sync: $timestamp"

# Step 5: Push
echo "📤 Pushing to remote..."
git push || {
  echo "❌ Push failed — remote updated while you were editing."
  echo "🔁 Run script again to auto-resolve."
  exit 1
}

echo ""
echo "🎉 Sync complete — your vault is up-to-date!"
