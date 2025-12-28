import joblib
import pandas as pd
from loguru import logger
from sklearn.datasets import load_wine
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
)
from sklearn.model_selection import train_test_split

from src.common.settings import settings


def main():
    # Load model artifacts
    logger.info(f"Loading model artifacts from: {settings.model_path}")
    model_artifacts = joblib.load(settings.model_path)
    model = model_artifacts['model']
    scaler = model_artifacts['scaler']
    feature_names = model_artifacts['feature_names']
    target_names = model_artifacts['target_names']
    model_version = model_artifacts['version']

    logger.info(f"Model version: {model_version}")
    logger.info(f"Features: {feature_names}")
    logger.info(f"Target classes: {target_names}")

    # Load wine dataset independently
    logger.info("Loading wine dataset for evaluation...")
    wine = load_wine()
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = pd.Series(wine.target, name="quality")

    # Perform same split as training
    _, X_test, _, y_test = train_test_split(
        X, y,
        test_size=settings.test_size,
        random_state=settings.random_state,
        stratify=y
    )

    logger.info(f"Test set loaded independently: {len(X_test)} samples")

    # Validate split parameters match training
    if 'random_state' in model_artifacts and 'test_size' in model_artifacts:
        assert model_artifacts['random_state'] == settings.random_state, \
            "Random state mismatch between training and evaluation!"
        assert model_artifacts['test_size'] == settings.test_size, \
            "Test size mismatch between training and evaluation!"
        logger.info("Split parameters validated against training artifacts")

    # Scale features
    logger.info("Scaling features...")
    X_test_scaled = scaler.transform(X_test)

    # Evaluate
    logger.info(f"Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    
    logger.info("Model Evaluation")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Balanced Accuracy: {balanced_acc:.4f}")
    logger.info("Classification Report:")
    logger.info(
        classification_report(y_test, y_pred, target_names=wine.target_names, zero_division=0)
    )


if __name__ == "__main__":
    main()
    