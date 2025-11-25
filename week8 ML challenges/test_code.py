"""
W8D2 Challenge 4: ML Pipeline - Starter Code

TASK: Fix pipeline issues for production ML
Goal: Proper sklearn Pipeline, no data leakage, save/load functionality

ISSUES:
- Not using sklearn Pipeline (manual preprocessing)
- Data leakage (fitting on full dataset before split)
- No pipeline persistence (can't use on new data)
- Preprocessing not reproducible
- Transformations done in wrong order

HINTS:
- Use sklearn.pipeline.Pipeline
- Fit scalers/encoders only on training data
- Save pipeline with joblib or pickle
- Chain transformations in correct order
- Use ColumnTransformer for different column types
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def create_pipeline():
    '''
    Create ML pipeline.

    ISSUES TO FIX:
    - Not using sklearn Pipeline
    - Manual preprocessing instead of pipeline steps
    - No ColumnTransformer for different column types
    - Doesn't return a pipeline object
    '''
    # ISSUE: Should use Pipeline, not just return model
    # from sklearn.pipeline import Pipeline
    # pipeline = Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('model', LogisticRegression())
    # ])

    model = LogisticRegression()
    return model

def preprocess_and_train(X, y):
    '''
    Preprocess data and train model.

    ISSUES TO FIX:
    - DATA LEAKAGE: Fitting scaler on all data before split!
    - Should only fit on training data
    - No pipeline to ensure same preprocessing on test data
    - Preprocessing not reproducible for new data
    '''
    # ISSUE: Fitting scaler on ALL data (before train/test split)
    # This is DATA LEAKAGE - test data info leaks into training!
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split AFTER scaling (wrong order!)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # ISSUE: We lost the scaler! Can't use it on new data
    # Should save both scaler and model together in pipeline

    # Test
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy

def apply_to_new_data(model, X_new):
    '''
    Apply trained model to new data.

    ISSUES TO FIX:
    - No access to scaler used during training
    - Can't reproduce preprocessing steps
    - Will fail because model expects scaled data but we can't scale it!
    - No pipeline to ensure consistent preprocessing
    '''
    # ISSUE: How do we scale X_new? We don't have the scaler!
    # This will give wrong predictions because data is not scaled

    try:
        predictions = model.predict(X_new)
        return predictions
    except Exception as e:
        print(f"Error: {e}")
        print("Can't apply model - don't have preprocessing pipeline!")
        return None

def save_model(model, filepath):
    '''
    Save model to file.

    ISSUES TO FIX:
    - Only saves model, not the scaler
    - Should save entire pipeline
    - New data can't be preprocessed the same way
    '''
    import pickle

    # ISSUE: Only saving model, not scaler or preprocessing steps
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

    # Should save entire pipeline including preprocessing

def load_and_predict(filepath, X_new):
    '''
    Load model and make predictions.

    ISSUES TO FIX:
    - Loads model but not preprocessing
    - Can't preprocess new data correctly
    - Will make incorrect predictions
    '''
    import pickle

    # ISSUE: Loading model but no preprocessing
    with open(filepath, 'rb') as f:
        model = pickle.load(f)

    # ISSUE: X_new is not preprocessed!
    # Should load pipeline that includes preprocessing
    predictions = model.predict(X_new)
    return predictions

def handle_mixed_types(X):
    '''
    Handle mixed numeric and categorical data.

    ISSUES TO FIX:
    - No ColumnTransformer to handle different types
    - Manually processing each type separately
    - Not integrated into pipeline
    - Hard to maintain and reproduce
    '''
    # ISSUE: Manual preprocessing instead of ColumnTransformer
    numeric_cols = X.select_dtypes(include=[np.number]).columns
    categorical_cols = X.select_dtypes(include=['object']).columns

    # Process numeric
    scaler = StandardScaler()
    X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

    # ISSUE: No encoding for categorical!
    # Should use OneHotEncoder in ColumnTransformer

    return X

# Test data
if __name__ == '__main__':
    # Generate sample data
    np.random.seed(42)
    n_samples = 1000

    X = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.randint(20000, 150000, n_samples),
        'credit_score': np.random.randint(300, 850, n_samples),
        'category': np.random.choice(['A', 'B', 'C'], n_samples)
    })

    y = (X['income'] > 75000).astype(int)

    print("Training with data leakage...")
    model, accuracy = preprocess_and_train(X[['age', 'income', 'credit_score']].values, y.values)
    print(f"Accuracy: {accuracy:.3f}")
    print("⚠️  But we have DATA LEAKAGE - scaler fit on all data!")

    print("\nTrying to apply to new data...")
    X_new = np.array([[25, 50000, 700], [45, 120000, 800]])
    predictions = apply_to_new_data(model, X_new)
    print(f"Predictions: {predictions}")
    print("⚠️  These predictions are wrong - data not scaled!")

    print("\nTrying to save model...")
    save_model(model, 'model.pkl')
    print("Saved model (but not scaler - can't use on new data!)")

    print("\n⚠️  Issues:")
    print("- DATA LEAKAGE: Scaler fit on all data before split")
    print("- No pipeline - can't reproduce preprocessing")
    print("- Can't apply to new data correctly")
    print("- Only model saved, not preprocessing steps")
    print("- No handling of categorical variables")
    print("\n✅ After fixing:")
    print("- Use sklearn Pipeline with all preprocessing steps")
    print("- Fit scaler only on training data")
    print("- Save entire pipeline with joblib")
    print("- Use ColumnTransformer for numeric and categorical")
    print("- Reproducible preprocessing for new data")