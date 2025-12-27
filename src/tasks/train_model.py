"""
Model training task for ML retraining pipeline.

This script trains a LogisticRegression model on the wine quality dataset
and saves it using joblib. Based on the training approach from ml-ops-hw01.
"""

import os
import joblib
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
)


def main():
    """Train and save a wine quality classification model."""
    
    # Configuration from environment variables
    model_version = os.getenv("MODEL_VERSION", "v1.0.0")
    random_state = int(os.getenv("RANDOM_STATE", "42"))
    test_size = float(os.getenv("TEST_SIZE", "0.2"))
    model_path = os.getenv("MODEL_PATH", "/app/models/model.pkl")
    
    print("=== ML Model Training ===")
    print(f"Model Version: {model_version}")
    print(f"Random State: {random_state}")
    print(f"Test Size: {test_size}")
    
    # Load wine dataset from sklearn (similar to WineQT)
    print("\nLoading wine dataset...")
    wine = load_wine()
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = pd.Series(wine.target, name="quality")
    
    print(f"Dataset shape: {X.shape}")
    print(f"Features: {list(X.columns)}")
    print(f"Target classes: {list(wine.target_names)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model (same configuration as ml-ops-hw01)
    print("\nTraining LogisticRegression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=random_state,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    
    print("\n=== Model Evaluation ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Balanced Accuracy: {balanced_acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=wine.target_names, zero_division=0))
    
    # Save model artifacts
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    artifacts = {
        'model': model,
        'scaler': scaler,
        'feature_names': list(X.columns),
        'target_names': list(wine.target_names),
        'version': model_version,
        'metrics': {
            'accuracy': accuracy,
            'balanced_accuracy': balanced_acc,
        }
    }
    
    joblib.dump(artifacts, model_path)
    print("\n=== Model Saved ===")
    print(f"Model saved to: {model_path}")
    print(f"Model version: {model_version}")
    
    return {
        'model_version': model_version,
        'accuracy': accuracy,
        'balanced_accuracy': balanced_acc,
        'model_path': model_path,
    }


if __name__ == "__main__":
    main()
