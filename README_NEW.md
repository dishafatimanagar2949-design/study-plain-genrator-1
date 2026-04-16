# AI Study Planner Generator

A comprehensive web application that automatically generates personalized study plans using machine learning. Input your subjects, topics, difficulty levels, and deadlines, and get an AI-optimized daily schedule.

## Features

✅ **User Authentication**
- Secure registration and login system
- SQLite-based user management
- Session-based authentication

✅ **Intelligent Planning**
- Auto-generate study plans based on priority and deadlines
- Machine learning models for study time estimation
- Smart scheduling algorithm

✅ **Study Management**
- Add multiple subjects with topics and difficulty levels
- Set deadlines and target study hours
- Track progress with completion markers
- Day-wise schedule view (table format)

✅ **Export Functionality**
- Export schedules to CSV
- Export schedules to PDF format

✅ **Responsive UI**
- Modern, clean interface
- Mobile-friendly design
- Real-time updates

## Tech Stack

- **Backend**: Flask 2.3.2
- **Database**: SQLite3
- **Machine Learning**: scikit-learn (Linear Regression, Decision Tree)
- **PDF Generation**: fpdf
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Project Structure

```
Study planner generator/
├── app.py                  # Main Flask application
├── ml_models.py            # ML model loading and prediction
├── train_models.py         # Model training script
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── .gitignore              # Git ignore rules
├── models/                 # ML models (auto-generated)
│   ├── lr_model.pkl
│   └── dt_model.pkl
├── templates/              # HTML templates
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
└── static/                 # Frontend assets
    ├── css/
    │   └── style.css
    └── js/
        └── planner.js
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Windows/macOS/Linux OS

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/study-planner-generator.git
cd study-planner-generator
```

### 2. Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train ML Models (First Time Only)
```bash
python train_models.py
```

This will generate:
- `models/lr_model.pkl` - Linear Regression model
- `models/dt_model.pkl` - Decision Tree model

### 5. Run the Application
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000/`

## Usage Guide

### First Time Users

1. **Register Account**
   - Click "Register" on the login page
   - Create username and password
   - Account is saved to SQLite database

2. **Log In**
   - Use your credentials to log in
   - Access the control panel

3. **Add Study Data**
   - Click "Add Subject" in the control panel
   - Fill in:
     - Subject name
     - Topic (what you're studying)
     - Difficulty level (1-10 scale)
     - Performance metric
     - Deadline date
     - Target study hours
   - Click "Add" to save

4. **Generate Study Plan**
   - Click "Generate Plan" button
   - The AI creates an optimized schedule
   - Plan considers deadlines and difficulty

5. **View Dashboard**
   - See your day-wise schedule
   - Monitor study tasks
   - Mark tasks as complete
   - Undo completion if needed

6. **Export Schedule**
   - Export to CSV for spreadsheet applications
   - Export to PDF for sharing/printing

### Admin/Development

**Reset Database:**
- Delete `database.db` file
- Restart the app to reinitialize

**Check ML Models:**
- Look in `models/` folder
- If missing, run `python train_models.py`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home/login page |
| POST | `/register` | Create new user |
| POST | `/login` | User authentication |
| GET | `/logout` | End user session |
| GET | `/dashboard` | View study schedule |
| POST | `/add_subject` | Add new subject |
| POST | `/generate_plan` | Generate study plan |
| POST | `/mark_done` | Mark task complete |
| POST | `/undo_task` | Undo task completion |
| GET | `/export_csv` | Export to CSV |
| GET | `/export_pdf` | Export to PDF |

## Configuration

### Environment Variables
Create a `.env` file (optional for production):
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Production Deployment
For production, use a WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Set `debug=False` in `app.py` before deploying.

## Troubleshooting

### Issue: ML Models Not Found
**Solution:** Run `python train_models.py` to generate models

### Issue: Database Locked Error
**Solution:** 
- Ensure only one instance of the app is running
- Delete `database.db` and restart

### Issue: Port 5000 Already in Use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Issue: Module Not Found
**Solution:** Ensure virtual environment is activated and requirements installed:
```bash
pip install -r requirements.txt
```

## Development

### Model Training Details
Edit `train_models.py` to:
- Adjust training features
- Modify model parameters
- Add new ML models

### Frontend Customization
Edit `static/css/style.css` and `static/js/planner.js`

### Backend Extension
Modify `app.py` and `ml_models.py` to:
- Add new routes
- Enhance ML predictions
- Implement new features

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- [ ] Cloud database support (PostgreSQL)
- [ ] User profiles and study statistics
- [ ] Notifications and reminders
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics and insights
- [ ] Collaborative study groups
- [ ] Integration with calendar apps
- [ ] Real-time AI chat assistant

## Support

For issues, questions, or suggestions:
1. Check existing issues in GitHub
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## Author

Created as an AI Study Planning Solution

## Acknowledgments

- Built with Flask
- Machine Learning powered by scikit-learn
- PDF generation by fpdf
