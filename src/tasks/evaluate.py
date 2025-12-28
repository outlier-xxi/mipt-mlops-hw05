import os
import joblib
import pandas as pd
from loguru import logger
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
)

from src.common.settings import settings


def main():
    # Load wine dataset from sklearn (similar to WineQT)
    logger.info("\nLoading wine dataset...")
    wine = load_wine()
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = pd.Series(wine.target, name="quality")

    logger.info(f"Loading model atrifacts from: {settings.model_path}")
    model_artifacts = joblib.load(settings.model_path)
    model = model_artifacts['model']
    scaler = model_artifacts['scaler']
    feature_names = model_artifacts['feature_names']
    target_names = model_artifacts['target_names']
    model_version = model_artifacts['version']
    logger.info(f"Model version: {model_version}")
    logger.info(f"Features: {feature_names}")
    logger.info(f"Target classes: {target_names}")

    # Split data
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=settings.test_size, random_state=settings.random_state, stratify=y
    )
    logger.info(f"Test size: {len(X_test)}")
    
    # Scale features
    logger.info(f"Scaling features...")
    X_test_scaled = scaler.transform(X_test)

    # Evaluate
    logger.info(f"Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    
    logger.info("\n Model Evaluation")  # pyright: ignore[reportUndefinedVariable]
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Balanced Accuracy: {balanced_acc:.4f}")
    logger.info("\nClassification Report:")
    logger.info(classification_report(y_test, y_pred, target_names=wine.target_names, zero_division=0))


if __name__ == "__main__":
    main()
    