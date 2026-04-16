import os
import pickle
import random
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier


def build_dummy_dataset(n_samples=300):
    data = []
    targets_hours = []
    targets_priority = []

    for i in range(n_samples):
        difficulty = random.choice([1, 2, 3, 4, 5])
        days_left = random.randint(1, 30)
        performance = random.choice([1, 2, 3, 4, 5])

        # Hours needed: more difficult + less time + lower performance => more hours
        hours = max(0.5, 0.5 * difficulty + 0.5 * (6 - performance) + 1.5 * max(0, (15 - days_left) / 10) + random.uniform(-0.5, 0.5))

        # Priority classification heuristic
        if difficulty >= 4 or days_left <= 3:
            priority = 2  # high
        elif difficulty >= 3 or days_left <= 7:
            priority = 1  # medium
        else:
            priority = 0  # low

        data.append([difficulty, days_left, performance])
        targets_hours.append(hours)
        targets_priority.append(priority)

    return np.array(data), np.array(targets_hours), np.array(targets_priority)


def train_and_save_models(models_dir='models'):
    os.makedirs(models_dir, exist_ok=True)

    X, y_hours, y_priority = build_dummy_dataset(500)

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
    lr_path = os.path.join(models_dir, 'lr_model.pkl')
    dt_path = os.path.join(models_dir, 'dt_model.pkl')

    if not os.path.exists(lr_path) or not os.path.exists(dt_path):
        lr, dt = train_and_save_models(models_dir)
        return lr, dt

    with open(lr_path, 'rb') as f:
        lr = pickle.load(f)
    with open(dt_path, 'rb') as f:
        dt = pickle.load(f)

    return lr, dt


def predict_study_estimate(difficulty, days_until_deadline, performance, lr_model, dt_model):
    X = [[difficulty, max(days_until_deadline, 1), performance]]
    hours = float(lr_model.predict(X)[0])
    priority_label = int(dt_model.predict(X)[0])

    # Clamp prediction
    hours = max(0.5, min(hours, 10.0))

    priority_score = {2: 3, 1: 2, 0: 1}.get(priority_label, 1)

    # This mix: high number means more urgent
    return round(hours, 1), priority_score
