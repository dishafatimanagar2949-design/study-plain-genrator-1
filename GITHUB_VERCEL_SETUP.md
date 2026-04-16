# Complete GitHub & Vercel Setup Guide

This is your step-by-step guide to deploy the AI Study Planner to GitHub and Vercel.

## 📋 What You Need

- GitHub account (free at github.com)
- Vercel account (free at vercel.com)
- Git installed on your computer
- This project folder open in VS Code

---

## PART 1: Prepare Your Project

### Step 1: Verify Project Files

Make sure these files exist in your project folder:
- ✅ `app.py` (main Flask app)
- ✅ `requirements.txt` (dependencies)
- ✅ `runtime.txt` (Python version)
- ✅ `vercel.json` (Vercel config)
- ✅ `Procfile` (process configuration)
- ✅ `.gitignore` (tells git what to ignore)
- ✅ `.env.example` (environment template)

### Step 2: Generate Secret Key

Open terminal/PowerShell and run:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output. You'll need it soon.

### Step 3: Test Locally

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Train ML models (if not done)
python train_models.py

# Run the app
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

Test:
- [ ] Homepage loads
- [ ] Can register
- [ ] Can login
- [ ] Can generate a plan
- [ ] Can export CSV/PDF

If all works, proceed to next section. If errors occur, check the terminal output.

---

## PART 2: GitHub Setup

### Step 1: Configure Git

Open terminal/PowerShell:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and email.

### Step 2: Verify Git Status

```bash
git status
```

You should see files listed as "untracked" or "modified".

### Step 3: Create Initial Commit

```bash
# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AI Study Planner Generator"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click "+" icon → "New repository"
3. Fill in:
   - **Repository name**: `study-planner-generator`
   - **Description**: "AI-powered study plan generator with ML"
   - **Visibility**: Public (so we can deploy to Vercel free tier)
4. Leave other options DEFAULT (do NOT initialize with README, .gitignore, or license)
5. Click "Create repository"

### Step 5: Push to GitHub

After creating repo, GitHub shows you commands. Follow these:

```bash
# Set remote URL (copy exact URL from GitHub repo page)
git remote add origin https://github.com/YOUR_USERNAME/study-planner-generator.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your project files there
3. Success! ✅

---

## PART 3: Vercel Deployment

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub" (easiest)
4. Authorize Vercel to access GitHub
5. Complete signup

### Step 2: Import Project

1. On Vercel dashboard, click "Add New..." → "Project"
2. Click "Continue with GitHub"
3. Authorize if prompted
4. Search for your repository: `study-planner-generator`
5. Click "Import" button

### Step 3: Configure Project Settings

On the "Configure Project" page:

**Project Name**: `study-planner-generator` (or custom)

**Framework Preset**: 
- Scroll down and select "Other" (Python isn't auto-detected sometimes)
- Or leave blank (Vercel auto-detects from `runtime.txt`)

**Root Directory**: `./` (default)

**Environment Variables** - Click "Add Environment Variable" and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |
| `SECRET_KEY` | (paste your generated key from Part 1, Step 2) |

Example:
```
FLASK_ENV = production
FLASK_DEBUG = False
SECRET_KEY = a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v
```

### Step 4: Deploy

Click "Deploy" button

⏳ Wait 2-5 minutes for deployment...

✅ You'll see "Congratulations! Your project has been successfully deployed!"

---

## PART 4: Test Your Live App

### Step 1: Get Your URL

On Vercel dashboard, you'll see a URL like:
```
https://study-planner-generator-1a2b3c4d5e.vercel.app
```

Click on it to visit your live app!

### Step 2: Testing Checklist

Test these in your live app:

- [ ] **Homepage** loads with landing page
- [ ] **Register** - Create a test account
- [ ] **Login** - Login with test account
- [ ] **Dashboard** - See empty plan
- [ ] **Add Subjects** - Add one subject:
  - Subject: Math
  - Topic: Algebra
  - Difficulty: 3
  - Performance: 4
  - Deadline: (pick any future date)
  - Hours: 10
- [ ] **Generate Plan** - Click and see plan generated
- [ ] **Export CSV** - Download and verify file
- [ ] **Export PDF** - Download and verify file
- [ ] **Toggle Task** - Mark as done/undo
- [ ] **Logout** - Successfully logged out

### Step 3: Share Your App

Send your live URL to friends:
```
Check out my AI Study Planner!
https://study-planner-generator-xxxx.vercel.app
```

---

## PART 5: Make Updates

### To Update Your App

1. Make code changes locally
2. Test with `python app.py`
3. Commit changes:
   ```bash
   git add .
   git commit -m "Fixed bug XYZ"
   git push
   ```
4. Vercel auto-deploys when you push!
5. Check Vercel dashboard for deployment status

---

## ⚠️ Important Notes

### Database (Critical!)

**Problem**: Your SQLite database will NOT persist between deployments on Vercel.
- Each time you deploy, you get a fresh database
- All student records will be lost
- This is fine for demos/testing

**Solution for Production**: 
- Upgrade to PostgreSQL or MongoDB
- Follow upgrade guide in [DEPLOYMENT.md](./DEPLOYMENT.md)

### Models Directory

Make sure `/models` folder with `.pkl` files are committed to GitHub:
```bash
git add models/
git commit -m "Add trained ML models"
git push
```

---

## 🆘 Troubleshooting

### "502 Bad Gateway" Error

**Cause**: Environment variables not set or Python error

**Fix**:
1. Go to Vercel dashboard
2. Check Settings → Environment Variables
3. Verify all variables are set correctly
4. Check "Deployments" → "Logs" for Python errors
5. Redeploy: "Deployments" → three dots → "Redeploy"

### "ModuleNotFoundError"

**Cause**: Package not in `requirements.txt`

**Fix**:
1. Add package: `pip install package-name`
2. Update: `pip freeze > requirements.txt`
3. Push to GitHub
4. Vercel redeploys automatically

### App works locally but not on Vercel

**Cause**: Usually environment variables or file paths

**Fix**:
1. Check Vercel logs in dashboard
2. Ensure `.env.example` has all needed vars
3. Add them to Vercel environment
4. Redeploy

### Models not loading

**Cause**: `/models/*.pkl` files not pushed to GitHub

**Fix**:
```bash
git add models/
git commit -m "Add ML models"
git push
```

Then redeploy on Vercel.

---

## 📚 Useful Resources

| Resource | URL |
|----------|-----|
| Vercel Dashboard | https://vercel.com/dashboard |
| Vercel Python Docs | https://vercel.com/docs/concepts/runtimes/python |
| GitHub Profile | https://github.com/settings/profile |
| Flask Docs | https://flask.palletsprojects.com/ |
| Python Docs | https://docs.python.org/3/ |

---

## ✅ You're Done!

Congratulations! Your AI Study Planner is now:

1. ✅ On GitHub (version control)
2. ✅ Deployed on Vercel (live online)
3. ✅ Accessible to anyone with the URL
4. ✅ Auto-updating when you push code

### Next Steps

1. **Share with friends**: Send them your Vercel URL
2. **Enhance the app**: Add more features
3. **Upgrade database**: Consider PostgreSQL for production
4. **Monitor usage**: Check Vercel analytics
5. **Add CI/CD**: Automate testing with GitHub Actions

---

## 🎉 Enjoy Your Live App!

**Project**: AI Study Planner  
**Live URL**: https://your-app.vercel.app  
**Source Code**: https://github.com/yourusername/study-planner-generator  
**Status**: Active & Deployed ✅

Made with ❤️ | Happy Coding! 🚀
