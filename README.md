# AI Study Planner Generator

A complete web app to generate personalized study plans from subjects, topics, difficulty, deadlines, and available time using AI and machine learning.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 Features

- **User Authentication**: Secure registration and login with SQLite
- **AI-Powered Planning**: Machine learning (Linear Regression + Decision Tree) predicts study hours needed
- **Smart Scheduling**: Auto-generates day-wise, deadline-aware schedules
- **Dashboard**: View, manage, and track all your study tasks
- **Progress Tracking**: Mark tasks complete/incomplete
- **Export Options**: Export plans as CSV or PDF
- **Responsive UI**: Beautiful, modern design with Tailwind CSS
- **Revision Planning**: Automatic revision days before deadlines

## 🚀 Live Demo

**Deployed on Vercel**: [Your Vercel URL](https://your-app.vercel.app)  
**Source Code**: [GitHub Repository](https://github.com/yourusername/study-planner-generator)

> Test credentials: Create your own account! It's free and takes 10 seconds.

## 📁 Project Structure

```
study-planner-generator/
├── app.py                 # Flask backend & routes
├── ml_models.py          # ML model training & prediction
├── train_models.py       # Script to train models
├── database.db           # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version for Vercel
├── vercel.json           # Vercel deployment config
├── DEPLOYMENT.md         # Deployment guide
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # Main dashboard
└── static/               # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── planner.js
```

## 💻 Quick Start (Local Development)

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (for GitHub)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/study-planner-generator.git
   cd study-planner-generator
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate ML models**
   ```bash
   python train_models.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 🤖 How the AI Works

### 1. **Input Phase**
User provides:
- Subject names
- Topics to study
- Difficulty level (1-5)
- Performance level (1-5)
- Deadline dates
- Target study hours
- Available hours per day

### 2. **ML Prediction**
The app uses two trained models:

**Linear Regression Model**:
- Predicts realistic study hours needed
- Factors: difficulty, days until deadline, performance level
- Formula: `hours = 0.5×difficulty + 0.5×(6-performance) + ...`

**Decision Tree Classifier**:
- Classifies priority (Low, Medium, High)
- Based on: difficulty, days left, performance
- High Priority: difficult topics or urgent deadlines

### 3. **Schedule Generation**
Algorithm:
1. Sort tasks by priority and deadline
2. Allocate predicted hours across remaining days
3. Respect daily hour limit
4. Add 2 revision days before deadline
5. No overlaps or exceeding daily capacity

### 4. **Output**
- Day-wise schedule display
- Time blocks for each task
- Progress tracking interface
- Export capabilities

## 🌐 Deployment to GitHub & Vercel

### Step 1: Push to GitHub
```bash
# Initialize git (if needed)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/study-planner-generator.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Vercel

1. **Sign up at** [Vercel.com](https://vercel.com)
2. **Click "New Project"** → **"Import Git Repository"**
3. **Select** your GitHub repo
4. **Framework**: Leave as default (Vercel auto-detects Python)
5. **Environment Variables**:
   - `FLASK_ENV` = `production`
   - `FLASK_DEBUG` = `False`
   - `SECRET_KEY` = (generate: `python -c "import secrets; print(secrets.token_hex(32))"`)
6. **Click "Deploy"** → Done! 🎉

Your app is now live at: `https://your-app.vercel.app`

### Full Deployment Guide
See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions and troubleshooting.

## 📊 Usage Guide

### 1. Register & Login
- Click "Register" on homepage
- Enter username and password
- Login with your credentials

### 2. Add Subjects
Fill out the Plan Builder:
```
Subject: Mathematics
Topic: Calculus
Difficulty: 4 (out of 5)
Performance: 3 (your current level)
Deadline: 2024-05-20
Target Hours: 20
Average Hours/Day: 3
```

### 3. Generate Plan
- Click "Generate Plan"
- AI creates optimal schedule
- View results in dashboard table

### 4. Track Progress
- Mark tasks "Done" when completed
- Click "Undo" to revert
- Delete tasks as needed

### 5. Export
- **CSV**: Download as spreadsheet
- **PDF**: Print or save as document

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask 2.3 (Python) |
| **Database** | SQLite3 |
| **ML Models** | Scikit-learn |
| **Frontend** | HTML, Tailwind CSS, JavaScript |
| **Deployment** | Vercel |
| **Version Control** | Git/GitHub |

## 🔧 Advanced Configuration

### Using PostgreSQL instead of SQLite
For production, replace SQLite:

1. Install `psycopg2-binary`:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `app.py`:
   ```python
   import psycopg2
   DATABASE = os.getenv('DATABASE_URL')
   ```

3. Update `requirements.txt`

### Install Development Tools
```bash
pip install -r requirements-dev.txt
```

## 📝 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Landing page |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/dashboard` | GET | Main dashboard |
| `/generate_plan` | POST | Generate study plan |
| `/toggle_task/<id>` | POST | Mark task complete |
| `/delete_task/<id>` | POST | Delete task |
| `/export/csv` | GET | Export as CSV |
| `/export/pdf` | GET | Export as PDF |
| `/logout` | GET | User logout |

## 🧪 Testing

Run tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_auth.py
```

## 🐛 Known Issues & Solutions

| Issue | Solution |
|-------|----------|
| Database resets after Vercel deployment | Upgrade to PostgreSQL |
| Models not found | Run `python train_models.py` |
| 403 Forbidden errors | Check SECRET_KEY in environment |
| Slow performance | Clear old tasks, optimize queries |

## 🚀 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Video tutorial integration
- [ ] Flashcard generation
- [ ] Time tracking
- [ ] Analytics dashboard
- [ ] OAuth integration (Google, GitHub)
- [ ] Dark/Light theme toggle
- [ ] Notifications and reminders
- [ ] REST API for external apps

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn ML Guide](https://scikit-learn.org/)
- [Vercel Deployment](https://vercel.com/docs)
- [Tailwind CSS](https://tailwindcss.com/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

## 👨‍💻 Author

**Your Name**  
📧 Email: your.email@example.com  
🔗 GitHub: [@yourusername](https://github.com/yourusername)

## 🙋 Support & Issues

- **Report Issues**: [GitHub Issues](https://github.com/yourusername/study-planner-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/study-planner-generator/discussions)
- **Email Support**: your.email@example.com

## 💝 Show Your Support

If this project helped you, please:
- ⭐ Star this repository
- 🐛 Report bugs and issues
- 💬 Share feedback and suggestions
- 🔗 Share with friends

---

**Happy Studying! 🎓**

Last Updated: April 2024  
Made with ❤️ by Shubham Mahadik
