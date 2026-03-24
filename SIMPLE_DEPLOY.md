# 🚀 Sonora - One-Click Deploy Guide

## ✨ Your Deploy Button

Copy and paste this into your Render dashboard to deploy instantly:

```
https://render.com/deploy?repo=github.com/sivakanthb/sonora-flute
```

---

## 📋 Simple 3-Step Setup

### Step 1: First Time Only - Push Code to GitHub
You need to push your code once. Choose ONE option below:

**Option A: Using GitHub Desktop (Easiest)**
1. Download https://github.com/apps/desktop
2. Install it (click Next → Finish)
3. Open GitHub Desktop
4. Click **File** → **Clone Repository**  
5. Search: `sonora-flute`
6. Click it → **Clone**
7. In the "Summary" box, type: `Initial deployment setup`
8. Click **Commit to main**
9. Click **Push origin**
✅ Done! Code is on GitHub.

**Option B: Command Line**
```bash
cd "path/to/sonora-flute"
git add .
git commit -m "Initial deployment setup"
git push origin main
```

---

### Step 2: Create Render Account
1. Go to: https://render.com
2. Click **Sign Up**
3. Click **Sign up with GitHub**
4. Click **Authorize render**
✅ Done! You have a Render account.

---

### Step 3: Deploy Your App
1. Go to: https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Click **Deploy existing repo**
4. Find `sonora-flute` and click **Connect**
5. Fill in the form with these values:

```
Name: sonora
Environment: Python
Region: Oregon (or closest)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT src.app:app
Plan: Free
```

6. Click **Create Web Service**
7. **Wait 3-5 minutes** for deployment
8. You'll see your live URL! 🎉

---

## 🌐 Your Live App

Once deployed, your app will be live at:
```
https://sonora.onrender.com
```

(Or whatever service name you chose - check Render dashboard)

---

## 🔄 Auto-Deploy Setup (After First Deploy)

Once your app is deployed on Render:

1. Go to your Render service settings
2. Find **Deploy Hook** section
3. Copy the deploy hook URL
4. Go to GitHub: https://github.com/sivakanthb/sonora-flute
5. Click **Settings** → **Secrets and variables** → **Actions**
6. Click **New repository secret**
7. Name: `RENDER_DEPLOY_HOOK`
8. Value: Paste the deploy hook URL from Render
9. Click **Add secret**

✅ **Now: Every time you push code to GitHub, it auto-deploys to Render!**

---

## 📱 Share Your App

Once live, share this link with anyone:
```
https://sonora.onrender.com
```

Works on:
- ✅ Desktop browsers
- ✅ Mobile phones  
- ✅ Tablets
- ✅ Any country/device

---

## 🆘 Troubleshooting

**Build is taking too long?**
- Free tier is slower. Check the logs in Render.

**App crashes after deployment?**
- Check Render logs for errors
- Usually is a missing dependency (already fixed in requirements.txt)

**Need help?**
- Share a screenshot, I'll help!

---

## 🎯 Summary

1. **First time:** Push code to GitHub (Option A or B above)
2. **Setup:** Create Render account and deploy (Step 3)
3. **Get link:** Your app is live! 
4. **Optional:** Setup auto-deploy with GitHub Actions (5 min extra)

**That's it! You now have a live Sonora app shared with the world!** 🌍
