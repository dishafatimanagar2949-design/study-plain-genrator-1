# Deployment Guide

This guide explains how to deploy the AI Study Planner to GitHub and Vercel.

## Prerequisites
- GitHub account
- Vercel account (free tier available)
- Git installed on your system

## Step 1: Prepare for GitHub

### 1.1 Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: AI Study Planner"
```

### 1.2 Create GitHub Repository
1. Go to GitHub.com and create a new repository
2. Name it `study-planner-generator` (or your preferred name)
3. Copy the HTTPS or SSH URL

### 1.3 Push to GitHub
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## Step 2: Configure Environment Variables

### 2.1 Local Development
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-random-secret-key-here
```

Generate a secure SECRET_KEY:
```python
import secrets
print(secrets.token_hex(32))
```

### 2.2 Vercel Environment Variables
You'll set these in Vercel dashboard during deployment (see Step 3).

## Step 3: Deploy to Vercel

### 3.1 Connect GitHub Repository
1. Go to https://vercel.com
2. Click "New Project"
3. Click "Import Git Repository"
4. Select your GitHub account and the `study-planner-generator` repo
5. Click "Import"

### 3.2 Configure Build Settings
1. Framework Preset: Select "Other"
2. Build Command: Leave empty (Vercel auto-detects)
3. Output Directory: Leave empty
4. Root Directory: `./`

### 3.3 Set Environment Variables
In Vercel dashboard for your project:
1. Go to Settings → Environment Variables
2. Add the following variables:
   - `FLASK_ENV` = `production`
   - `FLASK_DEBUG` = `False`
   - `SECRET_KEY` = (generate secure key from above)
3. Click "Save"

### 3.4 Deploy
1. Click "Deploy"
2. Wait for the deployment to complete (usually 2-3 minutes)
3. Once successful, you'll get a live URL

## Step 4: Post-Deployment

### 4.1 Test the Application
1. Visit your Vercel URL
2. Create a new account
3. Add subjects and generate a study plan
4. Test all features (export CSV, PDF, etc.)

### 4.2 Database Persistence Note
⚠️ **Important**: Vercel's serverless environment has ephemeral storage. Your SQLite database will be recreated on each deployment.

**Solution Options:**
- Use PostgreSQL/MySQL instead of SQLite (recommended for production)
- Use MongoDB Atlas (free tier available)
- Use AWS RDS

For now, the app works but data will reset on deployment. To upgrade:
1. Replace SQLite with PostgreSQL
2. Update `requirements.txt` to include `psycopg2-binary`
3. Update database connection in `app.py`

### 4.3 Custom Domain (Optional)
1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## Troubleshooting

### Build Fails
- Check Vercel build logs
- Ensure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt`

### Models Not Loading
- ML models must be trained locally first:
  ```bash
  python train_models.py
  ```
- Commit `/models/*.pkl` to GitHub

### Database Issues
- SQLite won't persist on Vercel
- Consider upgrading to PostgreSQL

### 403 or 502 Errors
- Check Environment Variables are set correctly
- Verify `SECRET_KEY` is not empty
- Check Vercel logs for Python errors

## Local Development

### Install Dependencies
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Train Models
```bash
python train_models.py
```

### Run Development Server
```bash
python app.py
```
Visit `http://127.0.0.1:5000/`

## Production Improvements

For a production-ready app, consider:

1. **Database**: Switch from SQLite to PostgreSQL
2. **Authentication**: Add OAuth (Google, GitHub login)
3. **Security**: 
   - Use HTTPS only
   - Add CSRF protection
   - Hash passwords properly (use werkzeug.security)
4. **Monitoring**: Add error tracking (Sentry)
5. **Analytics**: Add user analytics
6. **Email**: Add email notifications
7. **API**: Create REST API for mobile apps

## Support

For issues:
1. Check Vercel documentation: https://vercel.com/docs
2. Check Flask documentation: https://flask.palletsprojects.com/
3. Review error logs in Vercel dashboard

## Additional Resources

- Vercel Python Runtime: https://vercel.com/docs/concepts/runtimes/python
- Flask on Vercel: https://vercel.com/templates/python/flask
- GitHub Pages: https://pages.github.com/
