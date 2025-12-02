# Quick Deploy to Render - Command Reference

Copy and paste these commands to quickly deploy your app to Render.

## Step 1: Commit Your Code

```bash
# Check what will be committed
git status

# Add all files
git add .

# Commit with a message
git commit -m "Initial deployment: NPL Cricket Tournament with seeded data"
```

## Step 2: Create GitHub Repository & Push

### Option A: Using GitHub CLI (if installed)
```bash
gh repo create npl-cricket-tournament --public --source=. --remote=origin
git push -u origin main
```

### Option B: Manual Setup
1. Create repo on GitHub: https://github.com/new
2. Run these commands (replace YOUR_USERNAME):

```bash
git remote add origin https://github.com/YOUR_USERNAME/npl-cricket-tournament.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render auto-detects settings from `render.yaml`
5. Click **"Create Web Service"**
6. Wait 3-5 minutes for deployment

## Step 4: Access Your App

Your app will be live at:
```
https://npl-cricket-tournament.onrender.com
```

Default admin credentials:
- **Username**: admin
- **Password**: admin123

## Future Updates

```bash
# Make your changes, then:
git add .
git commit -m "Description of changes"
git push origin main

# Render auto-deploys on push!
```

## Troubleshooting

### Make build.sh executable if needed:
```bash
git update-index --chmod=+x build.sh
git commit -m "Make build script executable"
git push origin main
```

### Check deployment logs:
- Go to your service in Render dashboard
- Click "Logs" tab
- Look for errors

---

**That's it!** Your app is live on the internet! 🚀
