# Manual Push Instructions

Since there's an authentication issue, please push manually:

## Option 1: Use GitHub Desktop

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. File → Add Local Repository
4. Select: /Users/adisheshiyengar/Documents/data-quality-analyzer
5. Click "Publish repository"

## Option 2: Fix Token & Push

1. Go to: https://github.com/settings/tokens
2. Delete the old token (or verify repo permissions)
3. Create new token with full repo access
4. Run:

```bash
cd /Users/adisheshiyengar/Documents/data-quality-analyzer
git push -u origin main
```

Paste your new token when prompted.

## Option 3: Use GitHub Web UI

1. Go to https://github.com/adiyengar/data-quality-analyzer
2. Click "uploading an existing file"
3. Drag all files from the project folder

