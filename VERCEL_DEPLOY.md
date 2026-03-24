# 🚀 Deploy Sonora to Vercel - Step by Step

Your Flute Scale Detector (Sonora) application is **ready for production deployment**!

## ✅ Quick Deployment (3 steps, 5 minutes)

### **Step 1: Go to Vercel Dashboard**
1. Open: https://vercel.com/dashboard
2. Click **Add New** → **Project**

### **Step 2: Import Repository**
1. Click **Import Git Repository**
2. Paste or search: `sivakanthb/sonora-flute`
3. Select your repository
4. Click **Import**

### **Step 3: Configure & Deploy**
The configuration page will appear:
- **Framework**: Leave as "Other" (Flask app)
- **Root Directory**: Leave as `./`
- **Environment Variables**: (Optional - leaveempty for now)
- Click **Deploy**

---

## 🎉 That's It!

Vercel will automatically:
- ✅ Build your Docker container
- ✅ Run production server
- ✅ Assign you a live URL
- ✅ Enable automatic redeployments on GitHub push

**Your app will be live at:** `https://sonora-<random>.vercel.app`

---

## 📊 What Gets Deployed

Your Sonora application includes:
- 🎤 Live microphone recording with flute scale detection
- 📁 File upload support (audio & video)
- 🏠 Beautiful home page with flute resources
- 🎨 Responsive design (mobile, tablet, desktop)
- 🤖 ML-based scale classification
- 📖 Educational content integration

---

## 🔧 Troubleshooting

If deployment fails:

1. **Check GitHub Connection**
   - Verify your repo shows on https://github.com/sivakanthb/sonora-flute

2. **View Build Logs**
   - After clicking Deploy, Vercel shows real-time build logs
   - Look for any error messages

3. **Python Dependencies**
   - The `Dockerfile` automatically installs all requirements
   - If an issue occurs, check `requirements.txt`

4. **Docker Configuration**
   - Vercel uses the included `Dockerfile`
   - It's pre-configured for Flask + Python dependencies

---

## 📝 After Deployment

Once deployed, you can:
- Share your app URL with others
- Push new changes to GitHub → automatic redeployment
- View analytics in Vercel dashboard
- Configure custom domain (optional)

---

**Questions?** Check the Vercel docs at https://vercel.com/docs
