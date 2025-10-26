# Deployment Guide

This guide will help you deploy your Car Price AI application to both Vercel (frontend) and Render (backend).

## Prerequisites

- GitHub account
- Vercel account (vercel.com)
- Render account (render.com)
- Git repository pushed to GitHub

## Part 1: Deploy Backend to Render

### Step 1: Connect Your Repository
1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** and select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select the `drive-price-ai-main` repository

### Step 2: Configure the Backend Service
Use these settings:

- **Name**: `smart-car-value` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users (e.g., `Singapore` for India)
- **Branch**: `main`
- **Root Directory**: `/` (root)
- **Build Command**: 
  ```bash
  apt-get update && apt-get install -y build-essential && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn backend.app:app --host 0.0.0.0 --port $PORT
  ```

### Step 3: Deploy
1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Note the service URL (e.g., `https://smart-car-value.onrender.com`)

**Important**: The backend includes model files and will take longer to build due to dependencies.

### Step 4: Update Backend CORS Settings
Once deployed, update `backend/app.py` to add your Vercel URL to the allowed origins.

## Part 2: Deploy Frontend to Vercel

### Step 1: Connect Your Repository
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Connect your GitHub account if not already connected
4. Select the `drive-price-ai-main` repository

### Step 2: Configure the Frontend Project
1. **Project Name**: `drive-price-ai` (or your preferred name)
2. **Framework Preset**: Vite (auto-detected)
3. **Root Directory**: `.` (root)
4. **Build Command**: `npm run build`
5. **Output Directory**: `dist`

### Step 3: Add Environment Variables
Click **"Environment Variables"** and add:

- **Variable Name**: `VITE_API_URL`
- **Value**: Your Render backend URL (e.g., `https://smart-car-value.onrender.com`)
- **Environments**: Production, Preview, Development

Click **"Add"** for each environment.

### Step 4: Deploy
1. Click **"Deploy"**
2. Wait for the build to complete (2-5 minutes)
3. Your app will be live at `https://your-project-name.vercel.app`

## Part 3: Update Backend CORS After Vercel Deployment

Once your Vercel frontend is deployed, you need to update the backend CORS settings:

1. Go to Render dashboard → Your backend service
2. Find the URL of your frontend (e.g., `https://drive-price-ai.vercel.app`)
3. Edit `backend/app.py` and add your Vercel URL to the `allow_origins` list:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-url.vercel.app",
        # ... existing origins
    ],
    # ...
)
```

4. Commit and push the changes
5. Render will automatically redeploy

## Part 4: Update Frontend API URL (Optional)

If you changed the backend URL, update `vercel.json`:

```json
{
  "env": {
    "VITE_API_URL": "https://your-render-backend.onrender.com"
  }
}
```

Then redeploy from Vercel dashboard.

## Troubleshooting

### Backend Issues

**Build Fails:**
- Check that `requirements.txt` has all dependencies
- Ensure Python 3.9+ is selected
- Check build logs for specific errors

**502 Bad Gateway:**
- Check that the start command is correct
- Verify `PORT` environment variable is being used
- Check Render service logs

**CORS Errors:**
- Add your frontend URL to `allow_origins` in `backend/app.py`
- Remove trailing slashes from URLs
- Clear browser cache

### Frontend Issues

**Build Fails:**
- Check that all dependencies are in `package.json`
- Run `npm install` locally to check for errors
- Check Vercel build logs

**API Not Connecting:**
- Verify `VITE_API_URL` environment variable is set correctly
- Check that backend is deployed and healthy
- Use browser DevTools Network tab to debug requests

**Routing Issues:**
- `vercel.json` should have SPA fallback route
- Check that all routes are defined in `App.tsx`

### Health Check Endpoint

Test your backend health at:
```
https://your-backend.onrender.com/health
```

Should return:
```json
{"status":"healthy","version":"1.0"}
```

## Environment Variables Summary

### Render (Backend)
- Automatically set: `PORT`
- May need to add manually: None currently

### Vercel (Frontend)
- Required: `VITE_API_URL` = `https://your-backend.onrender.com`

## Monitoring

### Render
- View logs: Dashboard → Your Service → Logs
- Metrics: CPU, Memory, Network
- Auto-scaling: Disabled by default (free tier)

### Vercel
- View logs: Dashboard → Your Project → Deployments → Logs
- Analytics: Available on Pro plan
- Preview deployments: Automatic for each PR

## Cost Estimates

### Render
- Free tier: 750 hours/month
- Paid: $7/month for always-on service

### Vercel
- Free tier: Unlimited deployments
- Bandwidth: 100GB/month on free tier
- Paid: Starting at $20/month

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update CORS settings
4. ✅ Test the deployed application
5. ✅ Monitor logs and performance
6. ✅ Set up custom domains (optional)

## Useful Commands

### Local Development
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run frontend only
npm run dev

# Run backend only
uvicorn backend.app:app --reload

# Run both (if configured)
npm run dev
```

### Build and Test Locally
```bash
# Build frontend
npm run build
npm run preview

# Test backend
python -m uvicorn backend.app:app
```

## Support

For issues specific to:
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Render**: [render.com/docs](https://render.com/docs)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React**: [react.dev](https://react.dev)

