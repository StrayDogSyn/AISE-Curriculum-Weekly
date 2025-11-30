import os
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

def train_and_save(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rng = np.random.RandomState(0)
    X = rng.normal(size=(200, 2))
    y = (1 / (1 + np.exp(-(1.2 * X[:, 0] + 0.8 * X[:, 1] - 0.1))) > 0.5).astype(int)
    clf = LogisticRegression()
    clf.fit(X, y)
    joblib.dump(clf, path)
    return clf

def load_model(path: str):
    return joblib.load(path)

def ensure_model(path: str):
    if os.path.exists(path):
        return load_model(path)
    return train_and_save(path)