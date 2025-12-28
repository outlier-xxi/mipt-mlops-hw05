"""
Таск обучения модели для классификации качества вина
"""

from pathlib import Path
import joblib
import pandas as pd
from loguru import logger
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.common.settings import settings


def main():
    # Configuration from environment variables
    
    logger.info(" ML Model Training")
    logger.info(f"Model Version: {settings.model_version}")
    logger.info(f"Random State: {settings.random_state}")
    logger.info(f"Test Size: {settings.test_size}")
    
    # Load wine dataset from sklearn (similar to WineQT)
    logger.info("Loading wine dataset...")
    wine = load_wine()
    X = pd.DataFrame(wine.data, columns=wine.feature_names)
    y = pd.Series(wine.target, name="quality")
    
    logger.info(f"Dataset shape: {X.shape}")
    logger.info(f"Features: {list(X.columns)}")
    logger.info(f"Target classes: {list(wine.target_names)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.test_size, random_state=settings.random_state, stratify=y
    )
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train model (same configuration as ml-ops-hw01)
    logger.info("Training LogisticRegression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=settings.random_state,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train_scaled, y_train)
    
    # Save model artifacts
    Path(settings.model_path).parent.mkdir(parents=True, exist_ok=True)
    
    artifacts = {
        'model': model,
        'scaler': scaler,
        'feature_names': list(X.columns),
        'target_names': list(wine.target_names),
        'version': settings.model_version,
        'X_test': X_test,
        'y_test': y_test,
    }
    
    joblib.dump(artifacts, settings.model_path)
    logger.info(f"Model saved to: {settings.model_path}")
    logger.info(f"Model version: {settings.model_version}")
    
    return {
        'model_version': settings.model_version,
        'model_path': settings.model_path,
    }


if __name__ == "__main__":
    main()
