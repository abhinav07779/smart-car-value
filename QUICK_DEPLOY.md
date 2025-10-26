# Quick Deployment Guide

Follow these steps to deploy your application to Render and Vercel.

## 🚀 Deployment Steps

### Step 1: Prepare Your Code

All configurations are ready! Just commit and push your changes:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy Backend to Render (5 minutes)

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Use these exact settings:

```
Name: smart-car-value
Environment: Python 3
Region: Singapore (or closest to India)
Branch: main
Build Command: apt-get update && apt-get install -y build-essential && pip install -r requirements.txt
Start Command: uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

5. Click **"Create Web Service"**
6. Wait for deployment (first deployment takes 5-10 minutes)
7. **Copy the URL** (e.g., `https://smart-car-value-abc123.onrender.com`)

### Step 3: Deploy Frontend to Vercel (3 minutes)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New..."** → **"Project"**
3. Connect your GitHub repository
4. Click on `drive-price-ai-main`
5. Click **"Environment Variables"**
6. Add this environment variable:

```
Name: VITE_API_URL
Value: [PASTE YOUR RENDER URL HERE from Step 2]
```

7. Click **"Add"** for Production, Preview, and Development
8. Click **"Deploy"**
9. Wait for deployment (2-3 minutes)
10. **Copy your Vercel URL** (e.g., `https://drive-price-ai.vercel.app`)

### Step 4: Update Backend CORS

1. Open `backend/app.py`
2. Find the `allow_origins` list (around line 20-28)
3. Add your Vercel URL to the list:

```python
allow_origins=[
    "*",  # Allow all origins for development
    "https://drive-price-ai.vercel.app",  # ADD THIS LINE
    # ... existing origins
],
```

4. Save the file and commit:

```bash
git add backend/app.py
git commit -m "Update CORS with Vercel URL"
git push origin main
```

5. Render will automatically redeploy (wait 2-3 minutes)

### Step 5: Test Your Deployment

1. Visit your Vercel URL
2. Try submitting a car price prediction
3. Check that everything works!

## ✅ You're Done!

Your application is now live on:
- **Frontend**: https://your-project.vercel.app
- **Backend**: https://your-project.onrender.com

## 🔧 Troubleshooting

**Backend is slow to respond:**
- Free tier on Render spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to wake up
- Consider upgrading to a paid plan for always-on service ($7/month)

**Frontend can't connect to backend:**
- Check that `VITE_API_URL` environment variable is set correctly in Vercel
- Verify backend is running by visiting `https://your-backend.onrender.com/health`
- Make sure CORS is configured correctly

**CORS errors:**
- Add your Vercel URL to `allow_origins` in `backend/app.py`
- Redeploy backend after making changes

## 📝 Important URLs to Save

- Vercel Dashboard: https://vercel.com/dashboard
- Render Dashboard: https://dashboard.render.com
- Your Frontend: [your-vercel-url]
- Your Backend: [your-render-url]

## 💡 Tips

1. Monitor usage in both dashboards
2. Enable logging for debugging
3. Set up auto-scaling if you expect high traffic
4. Consider adding a custom domain for better branding

---

**Need Help?** Check `DEPLOYMENT_GUIDE.md` for detailed troubleshooting.

