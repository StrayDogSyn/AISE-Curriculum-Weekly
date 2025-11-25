"""
W8D2 Challenge 3: Model Training - Starter Code

TASK: Fix model training issues for better performance
Goal: Proper train/test split, cross-validation, and hyperparameter tuning

ISSUES:
- No train/test split (trains and tests on same data!)
- No cross-validation
- No hyperparameter tuning
- Hardcoded random state (not reproducible across runs)
- No model evaluation metrics beyond accuracy

HINTS:
- Use train_test_split from sklearn
- Implement k-fold cross-validation
- Use GridSearchCV or RandomizedSearchCV
- Set random_state consistently
- Calculate precision, recall, F1-score
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_model(X, y):
    '''
    Train a classification model.

    ISSUES TO FIX:
    - No train/test split - overfitting!
    - No cross-validation
    - No hyperparameter tuning
    - Only using accuracy (poor for imbalanced data)
    - No random state consistency
    '''
    # ISSUE: Training on ALL data, no holdout set
    model = LogisticRegression()
    model.fit(X, y)

    # ISSUE: Testing on same data used for training!
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)

    # ISSUE: Only reporting accuracy, no other metrics
    return model, accuracy

def tune_hyperparameters(X, y):
    '''
    Find best hyperparameters.

    ISSUES TO FIX:
    - No actual tuning, just uses defaults
    - No grid search or random search
    - No cross-validation during tuning
    - Doesn't try different parameter combinations
    '''
    # ISSUE: Just returns default model, no tuning!
    model = LogisticRegression()

    # ISSUE: No GridSearchCV or RandomizedSearchCV
    # Should try different C values, solvers, etc.

    return model

def evaluate_model(model, X, y):
    '''
    Evaluate model performance.

    ISSUES TO FIX:
    - Only calculates accuracy
    - No precision, recall, F1-score
    - No confusion matrix
    - No ROC curve or AUC
    - Tests on training data (data leakage!)
    '''
    # ISSUE: Evaluating on training data
    predictions = model.predict(X)

    # ISSUE: Only accuracy metric
    accuracy = accuracy_score(y, predictions)

    # Should also calculate:
    # - Precision and Recall
    # - F1-score
    # - Confusion matrix
    # - ROC-AUC score

    return {'accuracy': accuracy}

def cross_validate_model(X, y, k=5):
    '''
    Perform k-fold cross-validation.

    ISSUES TO FIX:
    - No actual cross-validation implemented
    - Just trains once and returns
    - No k-fold splitting
    - No averaging of results across folds
    '''
    # ISSUE: Not doing actual cross-validation!
    model = LogisticRegression()
    model.fit(X, y)
    score = accuracy_score(y, model.predict(X))

    # ISSUE: Should split into k folds and average results
    # Should use KFold or cross_val_score from sklearn

    return score

# Test data
if __name__ == '__main__':
    # Generate sample classification data
    np.random.seed(42)
    n_samples = 1000

    X = pd.DataFrame({
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.randn(n_samples),
        'feature4': np.random.randn(n_samples)
    })

    # Create imbalanced target (30% positive class)
    y = (X['feature1'] + X['feature2'] * 0.5 + np.random.randn(n_samples) * 0.5 > 0).astype(int)

    print("Original data:")
    print(f"Shape: {X.shape}")
    print(f"Class distribution: {y.value_counts().to_dict()}")

    print("\nTraining model...")
    model, accuracy = train_model(X.values, y.values)
    print(f"Accuracy: {accuracy:.3f}")

    print("\nTuning hyperparameters...")
    tuned_model = tune_hyperparameters(X.values, y.values)
    print("Tuned model (no actual tuning done!)")

    print("\nEvaluating model...")
    metrics = evaluate_model(model, X.values, y.values)
    print(f"Metrics: {metrics}")

    print("\nCross-validating...")
    cv_score = cross_validate_model(X.values, y.values)
    print(f"CV Score: {cv_score:.3f}")

    print("\n⚠️  Issues:")
    print("- Training and testing on same data (100% accuracy is suspicious!)")
    print("- No cross-validation implemented")
    print("- No hyperparameter tuning")
    print("- Only using accuracy metric")
    print("- No train/test split")
    print("\n✅ After fixing:")
    print("- Proper train/test split (e.g., 80/20)")
    print("- K-fold cross-validation")
    print("- GridSearchCV for hyperparameter tuning")
    print("- Multiple evaluation metrics (precision, recall, F1)")
    print("- Realistic accuracy scores on holdout set")