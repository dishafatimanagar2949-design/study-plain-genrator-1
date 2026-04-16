# Quick Start Checklist

Complete this checklist before deploying to GitHub & Vercel:

## 🔐 Security Setup
- [ ] Generate a secure SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Update `.env.example` with your settings
- [ ] Never commit `.env` file (already in `.gitignore`)
- [ ] Review `app.py` for any hardcoded secrets

## 🧪 Local Testing
- [ ] Create virtual environment: `python -m venv .venv`
- [ ] Activate virtual env: `.venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Train models: `python train_models.py`
- [ ] Run app locally: `python app.py`
- [ ] Test all pages:
  - [ ] Homepage (`/`)
  - [ ] Register (`/register`)
  - [ ] Login (`/login`)
  - [ ] Dashboard (`/dashboard`)
  - [ ] Generate Plan
  - [ ] Export CSV
  - [ ] Export PDF
  - [ ] Toggle tasks
  - [ ] Logout

## 📦 GitHub Preparation
- [ ] All files committed to git
- [ ] `.gitignore` contains `database.db`, `.env`, `__pycache__/`, `.venv/`, `models/*.pkl`
- [ ] `requirements.txt` updated with all dependencies
- [ ] `README.md` contains setup and deployment instructions
- [ ] Create GitHub account at github.com
- [ ] Create new public repository (no README, no gitignore, no license)

## 🚀 GitHub Push
- [ ] Configure git: `git config --global user.name "Name"`, `git config --global user.email "email@example.com"`
- [ ] Initialize if needed: `git init`
- [ ] Add remote: `git remote add origin <your-repo-url>`
- [ ] Push to GitHub: `git push -u origin main`
- [ ] Verify on GitHub.com that files are visible

## 🌐 Vercel Deployment
- [ ] Create Vercel account at vercel.com
- [ ] Connect GitHub account to Vercel
- [ ] Import repository from GitHub
- [ ] Set Framework: "Other" or leave default (auto-detects Python)
- [ ] Configure Environment Variables:
  - [ ] `FLASK_ENV=production`
  - [ ] `FLASK_DEBUG=False`
  - [ ] `SECRET_KEY=<your-generated-key>`
- [ ] Click Deploy
- [ ] Wait for deployment (2-3 minutes)
- [ ] Visit your live URL

## ✅ Post-Deployment Testing
- [ ] Access home page
- [ ] Create new account
- [ ] Login
- [ ] Add subjects and generate plan
- [ ] Export CSV
- [ ] Export PDF
- [ ] Check for any errors in Vercel logs

## 📋 Important Notes

### Database Considerations
- ⚠️ SQLite database is **ephemeral** on Vercel
- Data will be lost after each deployment or after 24 hours of inactivity
- **Solution**: Upgrade to PostgreSQL or MongoDB for production

### Models
- ML models are included in repository
- Generated models (`/models/*.pkl`) are automatically trained on first run
- If models aren't loading, run: `python train_models.py`

### Troubleshooting
- If build fails: Check Vercel logs in dashboard
- If app shows "502 Bad Gateway": Check environment variables
- If models don't load: Commit trained models to git first
- If database errors occur: Check SQL syntax in `app.py`

## 🎉 Success Indicators

You'll know everything worked if:
1. ✅ App loads on Vercel URL
2. ✅ Can register and login
3. ✅ Can generate study plans
4. ✅ Can export to CSV/PDF
5. ✅ No errors in browser console
6. ✅ All links work correctly

## 📞 Need Help?

- **GitHub Issues**: Create an issue in your repository
- **Vercel Docs**: https://vercel.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Deployment Guide**: Read `DEPLOYMENT.md` in project root

---

Good luck! 🚀
