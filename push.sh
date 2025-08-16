#!/usr/bin/env bash
set -e
# Usage: ./scripts/push.sh <github-username> <repo-name>
USER="$1"
REPO="$2"
if [ -z "$USER" ] || [ -z "$REPO" ]; then
  echo "Usage: ./scripts/push.sh <github-username> <repo-name>"
  exit 1
fi
git init
git branch -m main || true
git add .
git commit -m "Initial commit: my-photo-host"
git remote add origin https://github.com/${USER}/${REPO}.git
git push -u origin main
echo "✅ Pushed to https://github.com/${USER}/${REPO}"
echo "Now enable Pages: Settings → Pages → Source: Deploy from a branch → Branch: main, Folder: /docs"
