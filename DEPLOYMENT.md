# 🚀 Deployment Guide

## Quick Deploy (Recommended: Vercel + Railway)

### 1. Frontend on Vercel
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel will auto-detect Vite React app
5. Add environment variable: `VITE_API_URL` = `https://your-backend-url.railway.app`

### 2. Backend on Railway
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub
3. Railway will auto-detect Python app
4. Copy the generated URL
5. Update `VITE_API_URL` in Vercel with Railway URL

### 3. Test Deployment
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.railway.app`
- API Docs: `https://your-app.railway.app/docs`

## Alternative: Render (All-in-One)

### Backend on Render
1. Create "Web Service" on Render
2. Connect GitHub repository
3. Build: `cd backend && pip install -r requirements.txt`
4. Start: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`

### Frontend on Render
1. Create "Static Site" on Render
2. Connect GitHub repository
3. Build: `npm install && npm run build`
4. Publish: `dist`

## Environment Variables

### Frontend (Vercel/Render)
- `VITE_API_URL`: Your backend API URL

### Backend (Railway/Render)
- No additional environment variables needed for basic deployment

## Troubleshooting

### Common Issues:
1. **CORS errors**: Backend already configured for all origins
2. **Model not found**: Ensure `backend/models/` folder is committed
3. **Build failures**: Check Python version (3.13+) and dependencies

### Health Check:
- Backend: `GET /health` should return `{"status": "ok"}`
- Frontend: Should load without console errors

## Cost Estimation
- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier (500 hours/month) or $5/month
- **Render**: Free tier (750 hours/month) or $7/month

## Custom Domain
1. Add custom domain in Vercel/Render settings
2. Update `VITE_API_URL` if needed
3. Configure DNS records as instructed
