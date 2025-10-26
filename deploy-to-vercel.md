# Deploy to Vercel - Step by Step

## 🚀 Quick Start (Copy-Paste These Steps)

### 1. Go to Vercel Dashboard
Open: https://vercel.com/login

### 2. Import Project
1. Click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Select **"abhinav07779/smart-car-value"**
4. Click **"Import"**

### 3. Configure Project
**Root Directory:** Leave as default (`.`)

**Build Settings:**
- Framework Preset: **Vite** (auto-detected)
- Build Command: `npm run build`
- Output Directory: `dist`

### 4. Add Environment Variable
Before clicking Deploy, click **"Environment Variables"** and add:

```
Variable Name: VITE_API_URL
Value: [YOUR_RENDER_URL] ← You'll get this from Render deployment
```

⚠️ **IMPORTANT**: If deploying backend first, paste your Render URL here. Otherwise, use temporary value `https://smart-car-value.onrender.com`

### 5. Deploy!
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Your app is live! 🎉

### 6. Get Your Frontend URL
Your app will be at: `https://[project-name]-[hash].vercel.app`
Example: `https://drive-price-ai-abc123.vercel.app`

---

**Next**: Go back to Render and update CORS with this Vercel URL

