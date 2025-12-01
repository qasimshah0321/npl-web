# NPL Cricket Tournament - Deployment Guide

## Option 1: Deploy to Render.com (Recommended - Easiest)

Render.com is perfect for full-stack Python apps like this one.

### Steps:

1. **Create a GitHub Repository**
   ```bash
   cd "E:\Personal-projects\CludeCode\NPL Web"
   git init
   git add .
   git commit -m "Initial commit: NPL Cricket Tournament"
   ```

2. **Push to GitHub**
   - Create a new repository on GitHub (e.g., `npl-cricket-tournament`)
   - Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/npl-cricket-tournament.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Render.com**
   - Go to https://render.com and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure everything
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

4. **Access Your Site**
   - Your site will be live at: `https://npl-cricket-tournament.onrender.com`
   - Default admin login:
     - Username: `admin`
     - Password: `admin123`

### Notes:
- ✅ Free tier available (app sleeps after inactivity, takes 30s to wake up)
- ✅ Both frontend and backend deployed together
- ✅ Database persists across deployments
- ✅ Automatic HTTPS

---

## Option 2: Deploy to Railway.app

Railway is another great option for full-stack Python apps.

### Steps:

1. **Create GitHub Repository** (same as above)

2. **Deploy on Railway**
   - Go to https://railway.app and sign up
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy
   - Add environment variable: `FLASK_ENV=production`

3. **Access Your Site**
   - Railway will provide a URL like: `https://npl-cricket-tournament.railway.app`

### Notes:
- ✅ $5 free credit per month
- ✅ No cold starts (stays warm)
- ✅ Easy to use

---

## Option 3: Deploy to Netlify (Frontend) + Render (Backend)

If you specifically want to use Netlify for the frontend:

### Step 1: Deploy Backend to Render

1. Follow "Option 1" steps above for backend
2. Note your backend URL (e.g., `https://npl-cricket-tournament.onrender.com`)

### Step 2: Update Frontend for Netlify

1. Create `netlify.toml`:
   ```toml
   [build]
     publish = "frontend"

   [[redirects]]
     from = "/api/*"
     to = "https://YOUR-BACKEND-URL.onrender.com/api/:splat"
     status = 200
     force = true

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. Update API calls in frontend JS files to use relative URLs (already done)

### Step 3: Deploy Frontend to Netlify

1. Go to https://netlify.com
2. Drag and drop the `frontend` folder
3. Or connect to GitHub and deploy

### Notes:
- ⚠️ More complex setup
- ⚠️ Need to manage CORS properly
- ✅ Frontend loads very fast

---

## Option 4: Deploy to Heroku

### Steps:

1. **Create `Procfile`**
   ```
   web: gunicorn --bind 0.0.0.0:$PORT backend.app:create_app()
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create npl-cricket-tournament
   git push heroku main
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

### Notes:
- ⚠️ No free tier anymore (starts at $5/month)
- ✅ Very reliable
- ✅ Good documentation

---

## Post-Deployment Checklist

After deploying to any platform:

1. ✅ Test login with admin/admin123
2. ✅ Verify all pages load (Home, Schedule, Teams, Players, Bracket)
3. ✅ Check if matches display correctly
4. ✅ Test admin functionality (add/edit/delete)
5. ✅ Change default admin password in production!

---

## Database Persistence

- **SQLite** is used by default (good for small/medium apps)
- Database file (`cricket_tournament.db`) persists on Render/Railway
- For production with high traffic, consider upgrading to PostgreSQL

---

## Environment Variables

Set these on your hosting platform:

| Variable | Value | Required |
|----------|-------|----------|
| `FLASK_ENV` | `production` | Yes |
| `PORT` | Auto-set by platform | No |
| `SECRET_KEY` | Your secret key | Recommended |

---

## Troubleshooting

### Database not persisting
- Make sure `cricket_tournament.db` is in your deployment
- Check if hosting platform supports persistent disk storage

### Images not loading
- Ensure `uploads/` folder is created
- Check file permissions

### API errors
- Check CORS settings in `backend/app.py`
- Verify backend URL in frontend API calls

### Cold starts (Render free tier)
- First request after inactivity takes ~30 seconds
- Upgrade to paid plan ($7/month) for instant wake-up

---

## Recommended: Render.com

For this project, **Render.com** is the best choice because:
1. ✅ Free tier available
2. ✅ No configuration needed (uses `render.yaml`)
3. ✅ Both frontend + backend in one service
4. ✅ Automatic HTTPS and deployments
5. ✅ Easy to scale later

---

## Need Help?

If you encounter issues:
1. Check Render/Railway/Netlify logs
2. Verify all environment variables are set
3. Test locally first with `python backend/app.py`
4. Check `requirements.txt` has all dependencies
