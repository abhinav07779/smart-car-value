# 🚀 Free Deployment Guide

## Option 1: Vercel + Railway (Recommended)

### Frontend Deployment (Vercel)

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository
   - Vercel will auto-detect it's a Vite app
   - Click "Deploy"

3. **Get your Vercel URL** (e.g., `https://your-app.vercel.app`)

### Backend Deployment (Railway)

1. **Go to Railway**:
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Railway**:
   - Railway will auto-detect Python
   - Set the root directory to `/` (not `/backend`)
   - Railway will use the `Procfile` and `railway.json`

4. **Get your Railway URL** (e.g., `https://your-backend.railway.app`)

### Update Frontend with Backend URL

1. **In Vercel Dashboard**:
   - Go to your project settings
   - Add environment variable:
     - Key: `VITE_API_URL`
     - Value: `https://your-backend.railway.app`

2. **Redeploy**:
   - Trigger a new deployment in Vercel

## Option 2: Netlify + Railway

### Frontend (Netlify)

1. **Build locally**:
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop your `dist` folder
   - Or connect your GitHub repo

3. **Set environment variable**:
   - In Netlify dashboard → Site settings → Environment variables
   - Add `VITE_API_URL` = `https://your-backend.railway.app`

## Option 3: GitHub Pages + Render

### Frontend (GitHub Pages)

1. **Update vite.config.ts**:
   ```typescript
   export default defineConfig({
     base: '/your-repo-name/',
     // ... rest of config
   })
   ```

2. **Enable GitHub Pages**:
   - Go to repository settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose `gh-pages` branch

3. **Deploy**:
   ```bash
   npm run build
   npm install -g gh-pages
   gh-pages -d dist
   ```

### Backend (Render)

1. **Go to Render**:
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**:
   - Connect your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

## 🎯 Recommended: Vercel + Railway

This combination offers:
- ✅ **100% Free** (generous limits)
- ✅ **Easy setup** (5 minutes)
- ✅ **Automatic deployments** (Git push = deploy)
- ✅ **Custom domains** (free)
- ✅ **Great performance**
- ✅ **No credit card required**

## 📝 Final Steps

1. **Test your deployed app**
2. **Share the Vercel URL** with others
3. **Monitor usage** in both dashboards
4. **Set up custom domain** (optional)

Your car price prediction app will be live and accessible worldwide! 🌍
