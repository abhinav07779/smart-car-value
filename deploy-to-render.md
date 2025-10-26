# Deploy to Render - Step by Step

## 🚀 Quick Start (Copy-Paste These Steps)

### 1. Go to Render Dashboard
Open: https://dashboard.render.com/

### 2. Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### 3. Connect Repository
1. If not connected: Click **"Connect account"** next to GitHub
2. Click **"Connect"** to authorize GitHub
3. Select repository: **"drive-price-ai-main"** or **"smart-car-value"**
4. Click **"Connect"**

### 4. Configure Service
Use these EXACT settings:

```
Service Name: smart-car-value
Region: Singapore (or Mumbai/India if available)
Branch: main
Root Directory: backend
```

**Environment:**
- Select: **Python 3**
- Version: **Python 3.9 or higher**

**Build:**
```
Build Command:
apt-get update && apt-get install -y build-essential && pip install -r requirements.txt
```

**Start:**
```
Start Command:
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

### 5. Advanced Settings (Optional)
Click **"Advanced"** and add (optional):
- Instance Type: **Free** (or Starter for $7/month to avoid spin-down)
- Health Check Path: `/health`
- Auto-Deploy: **Yes**

### 6. Deploy!
1. Click **"Create Web Service"** at the bottom
2. Wait 5-10 minutes for first build
3. ✅ Your backend is live!

### 7. Get Your Backend URL
Your API will be at: `https://smart-car-value.onrender.com`

### 8. Test Your Backend
Open in browser:
```
https://[your-backend-url]/health
```

Should return:
```json
{"status":"healthy","version":"1.0"}
```

---

**⚠️ First request may take 30 seconds** (Render free tier spins down after 15 min idle)

**Next Steps:**
1. Copy your Render URL
2. Use it to deploy frontend on Vercel
3. Update CORS in `backend/app.py` with your Vercel URL

