# 🚀 Quick Start - Deploy to Render.com

## Step 1: Initialize Git Repository

```bash
cd "E:\Personal-projects\CludeCode\NPL Web"
git init
git add .
git commit -m "Initial commit: NPL Cricket Tournament Management System"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `npl-cricket-tournament` (or any name you like)
3. Keep it **Public** or **Private**
4. **DO NOT** initialize with README (we already have files)
5. Click "Create repository"

## Step 3: Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/npl-cricket-tournament.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Render.com

1. Go to https://render.com
2. Sign up (free) or login
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect account"** to connect GitHub
5. Find and select your `npl-cricket-tournament` repository
6. Render will auto-detect everything from `render.yaml`
7. Click **"Create Web Service"**
8. Wait 2-3 minutes for deployment ⏳

## Step 5: Access Your Live Site! 🎉

Your site will be live at:
```
https://npl-cricket-tournament.onrender.com
```

**Default Admin Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT:** Change the admin password after first login!

---

## Alternative: Deploy to Netlify (Frontend Only)

If you prefer Netlify for frontend:

1. Deploy backend to Render first (follow steps above)
2. Get your backend URL (e.g., `https://npl-cricket-backend.onrender.com`)
3. Update `netlify.toml` file - replace `YOUR-BACKEND-URL` with your actual backend URL
4. Go to https://netlify.com
5. Drag and drop the **`frontend`** folder OR connect to GitHub
6. Done! Your frontend will be on Netlify, backend on Render

---

## What's Included?

✅ All files configured for deployment
✅ `render.yaml` - Render configuration
✅ `netlify.toml` - Netlify configuration (if needed)
✅ `.gitignore` - Excludes sensitive files
✅ `requirements.txt` - Python dependencies
✅ Production-ready Flask app

---

## Free Tier Limitations

**Render.com Free Tier:**
- ✅ Free forever
- ⚠️ App sleeps after 15 min of inactivity
- ⚠️ First request after sleep takes ~30 seconds
- ✅ 750 hours/month (enough for most projects)

**Upgrade ($7/month):**
- No sleep/cold starts
- Better performance
- More resources

---

## Troubleshooting

### Git Issues?
```bash
# If you already have a git repo
git remote -v  # Check existing remotes
git remote remove origin  # Remove if needed
git remote add origin YOUR_NEW_URL
```

### Build Failed on Render?
- Check logs in Render dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility

### Database Empty After Deploy?
- The database starts fresh on first deploy
- Login with admin/admin123
- Add your teams and matches via admin panel
- Or run your import scripts after deployment

---

## Need to Update Your Site?

After making changes:

```bash
git add .
git commit -m "Your update message"
git push
```

Render will automatically redeploy! 🚀

---

## 🎯 Recommended Path

**Easiest:** Render.com (Everything in one place)
**Fastest Frontend:** Netlify (Frontend) + Render (Backend)
**Most Features:** Railway.app

For this project, **Render.com** is the simplest option!
