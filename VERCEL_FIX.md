# Vercel Deployment Fix - 500 Error Solution

## ✅ Changes Made to Fix the Error

### 1. **Updated vercel.json**
- Added Python runtime specification
- Added maxLambdaSize configuration
- Added PYTHONUNBUFFERED for logging

### 2. **Updated app.py**
- Added `secrets` module for better SECRET_KEY generation
- Added session cookie configuration
- Added error handling for model loading
- Added database initialization at startup (not just in __main__)
- Models now auto-train if missing

### 3. **Updated ml_models.py**
- Added directory creation for models
- Added try-except error handling
- Models will gracefully create if missing

### 4. **Environment Variables to Set on Vercel**

Go to: https://vercel.com/dashboard → Your Project → Settings → Environment Variables

Add these:
```
FLASK_ENV = production
FLASK_DEBUG = False
SECRET_KEY = (generate: python -c "import secrets; print(secrets.token_hex(32))")
```

## 🚀 How to Redeploy

### Option 1: Quick Redeploy from Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click your `study-planner-generator` project
3. Go to "Deployments" tab
4. Click three dots (•••) on latest deployment
5. Click "Redeploy"
6. Wait 3-5 minutes

### Option 2: Push Updates to GitHub & Auto-Deploy
```bash
git add .
git commit -m "Fix Vercel 500 error - add error handling and better initialization"
git push origin main
```
(Vercel auto-deplooys when you push)

## ✅ If Still Getting 500 Error

1. **Check Vercel Logs**:
   - Go to Deployments → Click latest
   - Click "Logs" tab
   - Read the error message
   - Share the error with me

2. **Verify Environment Variables**:
   - Settings → Environment Variables
   - FLASK_ENV = production ✓
   - FLASK_DEBUG = False ✓
   - SECRET_KEY = (long random string) ✓

3. **Check Build Logs**:
   - Deployments → Latest → "Build Logs"
   - Look for any Python errors

## 📝 Troubleshooting

| Error | Solution |
|-------|----------|
| 500 error | Check environment variables, check logs |
| Models not found | Models auto-train on first run |
| Database error | SQLite works but data resets on deploy |
| Timeout | Large models may take time to train |

## 🎯 Next Steps

1. Set environment variables in Vercel
2. Redeploy from Vercel dashboard
3. Visit your app URL
4. Try to login
5. If error: Share Vercel logs with me

---

**Once redeployed, test at**: https://study-planner-generator-xxx.vercel.app/
