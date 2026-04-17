import os
import sqlite3
import csv
import io
import secrets
import tempfile
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_file, make_response
from ml_models import load_models, predict_study_estimate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
app = Flask(__name__)

secret_key = os.getenv('SECRET_KEY')
if not secret_key and FLASK_ENV == 'production':
    raise RuntimeError('SECRET_KEY must be set in production')

app.secret_key = secret_key or secrets.token_hex(32)

if os.getenv('DATABASE_PATH'):
    DATABASE = os.getenv('DATABASE_PATH')
elif os.getenv('VERCEL') or os.getenv('NOW_REGION'):
    DATABASE = os.path.join(tempfile.gettempdir(), 'database.db')
else:
    DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=(FLASK_ENV == 'production'),
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

LR_MODEL = None
DT_MODEL = None


# Database helper functions

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.cursor().executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        day DATE NOT NULL,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        deadline DATE NOT NULL,
        hours REAL NOT NULL,
        start_time TEXT,
        end_time TEXT,
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    ''')

    # Backward-compatible upgrades (add columns if missing)
    cur = db.cursor()
    cur.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cur.fetchall()]
    if 'start_time' not in columns:
        cur.execute('ALTER TABLE tasks ADD COLUMN start_time TEXT')
    if 'end_time' not in columns:
        cur.execute('ALTER TABLE tasks ADD COLUMN end_time TEXT')

    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    return cur.lastrowid


def init_ml_models():
    global LR_MODEL, DT_MODEL
    try:
        LR_MODEL, DT_MODEL = load_models()
        print("✅ ML models loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not load ML models: {e}")
        print("App will continue but plan generation may not work optimally")


# Initialize database and models on app startup
with app.app_context():
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    try:
        init_ml_models()
    except Exception as e:
        print(f"⚠️ Model initialization warning: {e}")


# Route definitions

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return redirect(url_for('register'))

        try:
            execute_db('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            flash('Register successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Choose another.', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', (username, password), one=True)
        if user:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


def login_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    tasks = query_db('SELECT * FROM tasks WHERE user_id = ? ORDER BY day, difficulty DESC', (user_id,))

    # Group tasks by day for display
    plan_by_day = {}
    for t in tasks:
        day = t['day']
        plan_by_day.setdefault(day, []).append(t)

    # Always show a full range from least to greatest day
    if tasks:
        all_days = [datetime.strptime(row['day'], '%Y-%m-%d').date() for row in tasks]
        start = min(all_days)
        end = max(all_days)
        current = start
        while current <= end:
            day_str = current.strftime('%Y-%m-%d')
            plan_by_day.setdefault(day_str, [])
            current += timedelta(days=1)

    return render_template('dashboard.html', plan_by_day=plan_by_day)


@app.route('/generate_plan', methods=['POST'])
@login_required
def generate_plan():
    user_id = session['user_id']

    subjects = request.form.getlist('subject[]')
    topics = request.form.getlist('topic[]')
    difficulties = request.form.getlist('difficulty[]')
    performance_levels = request.form.getlist('performance[]')
    deadlines = request.form.getlist('deadline[]')
    hours_per_subject = request.form.getlist('hours[]')
    available_hours_per_day = float(request.form.get('available_hours_per_day', 3) or 3)

    user_tasks = []
    today = datetime.today().date()

    for subj, top, diff, perf, dl, hrs in zip(subjects, topics, difficulties, performance_levels, deadlines, hours_per_subject):
        if not subj.strip() or not top.strip() or not diff or not perf or not dl or not hrs:
            continue

        try:
            diff_i = int(diff)
            perf_i = int(perf)
            hrs_f = float(hrs)
            deadline_date = datetime.strptime(dl, '%Y-%m-%d').date()
        except ValueError:
            continue

        if hrs_f <= 0:
            continue

        # Determine ML predicted values
        days_left = max((deadline_date - today).days, 0) + 1
        pred_hours, priority_metric = predict_study_estimate(diff_i, days_left, perf_i, LR_MODEL, DT_MODEL)

        user_tasks.append({
            'subject': subj.strip(),
            'topic': top.strip(),
            'difficulty': max(1, min(diff_i, 5)),
            'performance': max(1, min(perf_i, 5)),
            'deadline': deadline_date,
            'user_hours': hrs_f,
            'pred_hours': pred_hours,
            'priority': priority_metric,
            'days_left': days_left
        })

    if not user_tasks:
        flash('Please add valid subjects and details to generate a plan.', 'danger')
        return redirect(url_for('dashboard'))

    execute_db('DELETE FROM tasks WHERE user_id = ?', (user_id,))

    # Sort by priority, deadline, ML predicted estimated hours
    user_tasks.sort(key=lambda t: (-t['priority'], t['deadline'], -t['difficulty']))

    # Day logic
    last_deadline = max(task['deadline'] for task in user_tasks)
    total_days = max((last_deadline - today).days + 1, 1)
    schedule_end = last_deadline

    # Add 2 revision days before the deadline, maintaining no overlaps
    revision_days = []
    for i in range(2, 0, -1):
        revision_day = last_deadline - timedelta(days=i)
        if revision_day >= today:
            revision_days.append(revision_day)

    plan_days = []
    for n in range((schedule_end - today).days + 1):
        day = today + timedelta(days=n)
        plan_days.append({'day': day, 'remaining': available_hours_per_day, 'tasks': []})

    # Allocate predicted hours across days respecting per-day cap and deadline
    for task in user_tasks:
        remaining = task['pred_hours']

        for day_slot in plan_days:
            # allow scheduling until and including the deadline day
            if day_slot['day'] > task['deadline']:
                continue
            if remaining <= 0:
                break
            if day_slot['remaining'] <= 0:
                continue

            assign = min(remaining, day_slot['remaining'])
            day_slot['tasks'].append({
                'subject': task['subject'],
                'topic': task['topic'],
                'difficulty': task['difficulty'],
                'deadline': task['deadline'],
                'hours': round(assign, 1),
                'completed': 0
            })
            day_slot['remaining'] -= assign
            remaining -= assign

        if remaining > 0:
            for day_slot in plan_days:
                if day_slot['remaining'] <= 0:
                    continue
                assign = min(remaining, day_slot['remaining'])
                day_slot['tasks'].append({
                    'subject': task['subject'] + ' (overflow)',
                    'topic': task['topic'],
                    'difficulty': task['difficulty'],
                    'deadline': task['deadline'],
                    'hours': round(assign, 1),
                    'completed': 0
                })
                day_slot['remaining'] -= assign
                remaining -= assign
                if remaining <= 0:
                    break

    # Add revision tasks at the end of schedule
    if revision_days:
        subjects_to_review = [t['subject'] for t in user_tasks][:3]
        for rday in revision_days:
            day_slot = next((d for d in plan_days if d['day'] == rday), None)
            if day_slot:
                for subject in subjects_to_review:
                    if day_slot['remaining'] <= 0:
                        break
                    review_hours = min(1.0, day_slot['remaining'])
                    day_slot['tasks'].append({
                        'subject': f'Review: {subject}',
                        'topic': 'Revision',
                        'difficulty': 1,
                        'deadline': last_deadline,
                        'hours': round(review_hours, 1),
                        'completed': 0
                    })
                    day_slot['remaining'] -= review_hours

    # Ensure timeline includes all days up to deadline even if empty
    all_days_dict = {slot['day'].strftime('%Y-%m-%d'): slot for slot in plan_days}
    for day_iter in range((schedule_end - today).days + 1):
        day_str = (today + timedelta(days=day_iter)).strftime('%Y-%m-%d')
        if day_str not in all_days_dict:
            all_days_dict[day_str] = {'day': today + timedelta(days=day_iter), 'remaining': available_hours_per_day, 'tasks': []}

    # Save into tasks table and show result in dashboard
    for day_key in sorted(all_days_dict):
        day_slot = all_days_dict[day_key]
        for entry in day_slot['tasks']:
            execute_db(
                'INSERT INTO tasks (user_id, day, subject, topic, difficulty, deadline, hours, start_time, end_time, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, day_slot['day'].strftime('%Y-%m-%d'), entry['subject'], entry['topic'], entry['difficulty'], entry['deadline'].strftime('%Y-%m-%d'), entry['hours'], entry.get('start_time', ''), entry.get('end_time', ''), entry['completed'])
            )

    flash('Personalized ML-backed study plan generated and saved!', 'success')
    return redirect(url_for('dashboard'))

    # Assign exact times (e.g., 08:00–09:30) per day
    for day_slot in plan_days:
        start_hour = 8.0
        for entry in day_slot['tasks']:
            entry['start_time'] = f"{int(start_hour):02d}:{int((start_hour-int(start_hour)) * 60):02d}"
            capacity = entry['hours']
            end_hour = start_hour + capacity
            end_h = int(end_hour)
            end_m = int(round((end_hour - end_h) * 60))
            if end_m == 60:
                end_h += 1
                end_m = 0
            entry['end_time'] = f"{end_h:02d}:{end_m:02d}"
            start_hour = end_hour

            # Bound at 23:59
            if start_hour >= 24:
                break

    # Persist into DB
    for day_slot in plan_days:
        for entry in day_slot['tasks']:
            execute_db(
                'INSERT INTO tasks (user_id, day, subject, topic, difficulty, deadline, hours, start_time, end_time, completed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, day_slot['day'].strftime('%Y-%m-%d'), entry['subject'], entry['topic'], entry['difficulty'], entry['deadline'].strftime('%Y-%m-%d'), entry['hours'], entry.get('start_time', ''), entry.get('end_time', ''), entry['completed'])
            )

    flash('Personalized ML-backed study plan generated and saved!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    user_id = session['user_id']
    task = query_db('SELECT * FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id), one=True)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('dashboard'))

    new_state = 0 if task['completed'] else 1
    execute_db('UPDATE tasks SET completed = ? WHERE id = ?', (new_state, task_id))
    return redirect(url_for('dashboard'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    user_id = session['user_id']
    task = query_db('SELECT * FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id), one=True)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('dashboard'))

    execute_db('DELETE FROM tasks WHERE id = ?', (task_id,))
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/export/csv')
@login_required
def export_csv():
    user_id = session['user_id']
    tasks = query_db('SELECT * FROM tasks WHERE user_id = ? ORDER BY day', (user_id,))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Day', 'Subject', 'Topic', 'Difficulty', 'Deadline', 'Hours', 'Completed'])

    for t in tasks:
        writer.writerow([t['day'], t['subject'], t['topic'], t['difficulty'], t['deadline'], t['hours'], 'Yes' if t['completed'] else 'No'])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=study_plan.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/export/pdf')
@login_required
def export_pdf():
    try:
        from fpdf import FPDF
    except ImportError:
        flash('FPDF package not installed. Install via pip install fpdf', 'danger')
        return redirect(url_for('dashboard'))

    user_id = session['user_id']
    tasks = query_db('SELECT * FROM tasks WHERE user_id = ? ORDER BY day', (user_id,))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'AI Study Planner - Exported Plan', ln=True, align='C')
    pdf.ln(4)

    pdf.set_font('Arial', '', 11)
    line_height = 7
    col_widths = [25, 30, 45, 20, 25, 15, 20]

    # header
    headers = ['Day', 'Subject', 'Topic', 'Diff', 'Deadline', 'Hrs', 'Done']
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], line_height, header, border=1)
    pdf.ln(line_height)

    for t in tasks:
        row = [t['day'], t['subject'], t['topic'], str(t['difficulty']), t['deadline'], str(t['hours']), 'Yes' if t['completed'] else 'No']
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], line_height, str(item)[:20], border=1)
        pdf.ln(line_height)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='study_plan.pdf', mimetype='application/pdf')


if __name__ == '__main__':
    with app.app_context():
        init_db()
        init_ml_models()

    # Production: Use gunicorn, or run with debug=False
    debug_mode = FLASK_ENV == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
