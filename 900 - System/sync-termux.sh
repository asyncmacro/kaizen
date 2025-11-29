#!/data/data/com.termux/files/usr/bin/env bash
set -e

# Format: 2025-11-29 14:32:12
timestamp=$(date "+%Y-%m-%d %H:%M:%S")

echo "🔄 Pulling latest changes..."
git pull

echo "➕ Adding all changes..."
git add .

echo "📝 Committing with timestamp..."
git commit -m "auto: $timestamp"

echo "📤 Pushing changes..."
git push

echo "✅ Done."
