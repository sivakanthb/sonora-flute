# Step 1: Push to GitHub

## Option A: Using Git Command Line (Recommended)

### Install Git (if not already installed):
1. Download from: https://git-scm.com/download/win
2. Run the installer and follow defaults
3. Restart PowerShell

### Then run these commands:

```powershell
cd "C:\Users\badis\OneDrive - Pegasystems Inc\Desktop\My Apps\sonora-flute"

# Configure Git (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all new files
git add .

# Commit with a message
git commit -m "Add production deployment configuration (Procfile, requirements.txt, render.yaml)"

# Push to GitHub
git push origin main
```

---

## Option B: Using GitHub Desktop (Easier)

1. Download: https://desktop.github.com/
2. Open GitHub Desktop
3. Open your repository
4. You'll see all the new files (Procfile, render.yaml, etc.)
5. Click **Commit to main** button
6. Click **Push origin** button

That's it! ✨

---

## Option C: Using VS Code Git Integration

1. In VS Code, go to **Source Control** (Ctrl+Shift+G)
2. You'll see all changed files
3. Type a commit message: "Add production deployment configuration"
4. Click **Commit** button
5. Click **Sync Changes** button

---

## What Gets Pushed:
- ✅ `Procfile` - Web server config
- ✅ `render.yaml` - Render configuration
- ✅ Updated `requirements.txt` - With Gunicorn
- ✅ Updated `app.py` - Production support
- ✅ `DEPLOYMENT.md` - Setup guide

## Once Pushed to GitHub:
1. Go to render.com
2. Create account (or log in)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Select this repository
6. Follow the deployment guide

**That's all! Render will automatically:**
- Clone your code
- Install dependencies
- Start your app
- Give you a live URL

Your app will be live within 5 minutes! 🚀
