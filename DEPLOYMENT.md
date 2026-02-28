# 🚀 Sonora Deployment Guide - Render.com (Free Tier)

## Overview
This guide walks you through deploying Sonora to **Render.com** - a free, reliable platform perfect for Flask applications.

### Prerequisites
- ✅ GitHub account (you already have the code pushed)
- ✅ Render.com account (free to create)
- ✅ All code updated and ready

---

## Step-by-Step Deployment

### Step 1: Create a Render Account
1. Go to [render.com](https://render.com)
2. Click **Sign Up**
3. Choose **Sign up with GitHub** (easiest option)
4. Authorize Render to access your GitHub account

### Step 2: Create a New Web Service
1. On Render dashboard, click **New +** → **Web Service**
2. Click **Connect a repository**
3. Find and select your `flute-scale-detector` repository
4. Click **Connect**

### Step 3: Configure Your Service
Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `sonora-scale-detector` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT src.app:app` |
| **Plan** | `Free` |

### Step 4: Add Environment Variables (Optional)
1. Scroll down to **Environment** section
2. Add the following variables:
   ```
   FLASK_ENV = production
   SECRET_KEY = your-super-secret-random-key-here
   PYTHON_VERSION = 3.11
   ```

3. For `SECRET_KEY`, generate a random key using:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 5: Deploy!
1. Click **Create Web Service**
2. Render will automatically:
   - Install dependencies
   - Build your application
   - Deploy to production
3. Wait for the build to complete (usually 2-5 minutes)

### Step 6: Get Your Live URL
Once deployment is complete, you'll see a URL like:
```
https://sonora-scale-detector.onrender.com
```

This is your public link! 🎉

---

## What's Happening Behind the Scenes

### Files Used for Deployment:
- **`requirements.txt`** - Python dependencies (includes Gunicorn)
- **`Procfile`** - Defines how to start the web server
- **`render.yaml`** - Render-specific configuration
- **`src/app.py`** - Flask application with environment variable support

### Automatic Redeploy
Whenever you push to GitHub:
1. Render automatically detects the changes
2. Pulls the latest code
3. Rebuilds and redeploys your application
4. Updates go live automatically

---

## After Deployment

### ✅ Testing Your Live App
Visit your URL and verify:
- 🏠 Home page loads
- 🎤 Detector page works
- 📚 Learn pages functional
- 👤 Profile page accessible
- 📧 Contact form submits
- ✨ All navigation links work

### 📊 Monitoring
- View logs: Click your service on Render dashboard
- Check health: Visit `https://your-url/health`

### 🔧 Common Issues & Solutions

**Issue: "Build failed"**
- Check that `requirements.txt` is in the root directory
- Verify all dependencies are listed

**Issue: "Application crashed"**
- Check logs on Render dashboard
- Ensure `Procfile` format is correct
- Verify Flask routes are working locally first

**Issue: "Static files not loading"**
- Files in `src/static/` are automatically served
- No additional configuration needed

---

## Free Tier Limitations & Features

### ✅ Included (Free Tier)
- Unlimited projects
- 750 hours/month of free service (enough for continuous running)
- Automatic SSL certificates
- Auto-deploy from GitHub
- PostgreSQL databases (you don't need this)
- Simple logging and monitoring

### ⚠️ Limitations
- Application spins down after 15 minutes of inactivity (first request might be slower)
- Shared CPU/RAM resources
- No custom domain (unless you add 🔗)

### 💡 To Keep It Always Active
Add a health check monitor (free service that pings your app every 5 minutes):
- Use UptimeRobot.com (free tier)
- Point it to: `https://your-url/health`
- Prevents spinning down

---

## Sharing Your Link

### For Everyone:
Simply share: `https://sonora-scale-detector.onrender.com`

(Or whatever custom name you choose)

### To Share with GitHub Link:
Add to your GitHub README:
```markdown
🚀 **Live Demo**: [Sonora Scale Detector](https://sonora-scale-detector.onrender.com)
```

---

## Next Steps (Optional)

### 1. Custom Domain
- Go to Render dashboard → Settings → Custom Domain
- Add your own domain (paid feature)

### 2. Upgrade Plan
- For persistent storage and better performance
- Click **Change Plan** on your service

### 3. Database (Future Enhancement)
- Add PostgreSQL for storing more user data
- Replace JSON file storage with persistent database

---

## Getting Help

- **Render Documentation**: https://render.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Check Render Logs**: Go to service → Logs tab

---

## Deployment Summary

```
✅ Code ready (with Procfile & render.yaml)
✅ Requirements.txt updated (with Gunicorn)
✅ App configured for production
✅ Environment variables set
✅ Auto-deploy from GitHub enabled
✅ Live URL ready to share

🎉 Your Sonora app is now live to the world!
```

---

**Questions?** Everything is automated. Just commit your changes to GitHub and Render handles the rest!
