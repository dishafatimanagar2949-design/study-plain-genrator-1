import os
import pickle
import random
from datetime import datetime


def build_dummy_dataset(n_samples=300):
    data = []
    targets_hours = []
    targets_priority = []

    for i in range(n_samples):
        difficulty = random.choice([1, 2, 3, 4, 5])
        days_left = random.randint(1, 30)
        performance = random.choice([1, 2, 3, 4, 5])

        hours = max(0.5, 0.5 * difficulty + 0.5 * (6 - performance) + 1.5 * max(0, (15 - days_left) / 10) + random.uniform(-0.5, 0.5))

        if difficulty >= 4 or days_left <= 3:
            priority = 2
        elif difficulty >= 3 or days_left <= 7:
            priority = 1
        else:
            priority = 0

        data.append([difficulty, days_left, performance])
        targets_hours.append(hours)
        targets_priority.append(priority)

    return data, targets_hours, targets_priority


def train_and_save_models(models_dir='models'):
    try:
        import numpy as np
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeClassifier
    except ImportError as exc:
        raise RuntimeError('Training requires numpy and scikit-learn.') from exc

    os.makedirs(models_dir, exist_ok=True)
    X, y_hours, y_priority = build_dummy_dataset(500)
    X = np.array(X)
    y_hours = np.array(y_hours)
    y_priority = np.array(y_priority)

    lr = LinearRegression()
    lr.fit(X, y_hours)

    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    dt.fit(X, y_priority)

    lr_path = os.path.join(models_dir, 'lr_model.pkl')
    dt_path = os.path.join(models_dir, 'dt_model.pkl')

    with open(lr_path, 'wb') as f:
        pickle.dump(lr, f)
    with open(dt_path, 'wb') as f:
        pickle.dump(dt, f)

    return lr, dt


def load_models(models_dir='models'):
    os.makedirs(models_dir, exist_ok=True)
    lr_path = os.path.join(models_dir, 'lr_model.pkl')
    dt_path = os.path.join(models_dir, 'dt_model.pkl')

    if os.path.exists(lr_path) and os.path.exists(dt_path):
        try:
            with open(lr_path, 'rb') as f:
                lr = pickle.load(f)
            with open(dt_path, 'rb') as f:
                dt = pickle.load(f)
            return lr, dt
        except Exception:
            return None, None

    return None, None


def predict_study_estimate(difficulty, days_until_deadline, performance, lr_model, dt_model):
    if lr_model is not None and dt_model is not None:
        try:
            X = [[difficulty, max(days_until_deadline, 1), performance]]
            hours = float(lr_model.predict(X)[0])
            priority_label = int(dt_model.predict(X)[0])
            return round(max(0.5, min(hours, 10.0)), 1), priority_label
        except Exception:
            pass

    difficulty = max(1, min(int(difficulty), 5))
    performance = max(1, min(int(performance), 5))
    days = max(int(days_until_deadline), 1)
    hours = max(0.5, 0.5 * difficulty + 0.5 * (6 - performance) + 1.5 * max(0, (15 - days) / 10))

    if difficulty >= 4 or days <= 3:
        priority_label = 2
    elif difficulty >= 3 or days <= 7:
        priority_label = 1
    else:
        priority_label = 0

    return round(hours, 1), priority_label
