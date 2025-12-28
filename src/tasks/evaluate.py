import joblib
from loguru import logger
from sklearn.datasets import load_wine
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
)

from src.common.settings import settings


def main():
    logger.info(f"Loading model artifacts from: {settings.model_path}")
    model_artifacts = joblib.load(settings.model_path)
    model = model_artifacts['model']
    scaler = model_artifacts['scaler']
    feature_names = model_artifacts['feature_names']
    target_names = model_artifacts['target_names']
    model_version = model_artifacts['version']
    # Load test data 
    X_test = model_artifacts['X_test']
    y_test = model_artifacts['y_test']
    
    logger.info(f"Model version: {model_version}")
    logger.info(f"Features: {feature_names}")
    logger.info(f"Target classes: {target_names}")
    logger.info(f"Test size: {len(X_test)}")
    
    # Load wine dataset for target_names in classification report
    wine = load_wine()
    
    # Scale features
    logger.info(f"Scaling features...")
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
    logger.info(classification_report(y_test, y_pred, target_names=wine.target_names, zero_division=0))


if __name__ == "__main__":
    main()
    