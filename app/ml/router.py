"""ML Router for intent classification."""

import logging
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from app.config import get_settings
from app.constants import TF_IDF_MAX_FEATURES, TF_IDF_NGRAM_RANGE, MODEL_TEST_SIZE, MODEL_RANDOM_STATE
from app.ml.model_manager import MissingSignatureError, ModelManager
from app.schemas import RouterResult
from data.training_data import TRAINING_DATA

logger = logging.getLogger(__name__)

settings = get_settings()
model_manager = ModelManager(
    Path(settings.model_path),
    Path(settings.model_signature_path)
)


def train_model() -> Pipeline:
    """
    Train ML router model.

    Returns:
        Trained sklearn pipeline
    """
    logger.info("Starting model training...")
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=MODEL_TEST_SIZE, random_state=MODEL_RANDOM_STATE
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=TF_IDF_NGRAM_RANGE,
            max_features=TF_IDF_MAX_FEATURES
        )),
        ("clf", LogisticRegression(max_iter=1000, random_state=MODEL_RANDOM_STATE))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    logger.info("=== Model Training Complete ===")
    logger.info(f"\n{classification_report(y_test, y_pred, zero_division=0)}")

    model_manager.save(pipeline, create_signature=True)
    logger.info(f"Model saved to {settings.model_path}")
    return pipeline


def load_model() -> Pipeline:
    """
    Load trained model.

    Returns:
        Loaded sklearn pipeline
    """
    try:
        return model_manager.load()
    except FileNotFoundError:
        logger.warning("No model found, training new model...")
        return train_model()
    except MissingSignatureError:
        logger.warning("Model signature missing, retraining model from trusted training data...")
        return train_model()


def route_task(text: str) -> RouterResult:
    """
    Route task to appropriate agent.

    Args:
        text: Task text to classify

    Returns:
        RouterResult with routing decision and confidence scores

    Raises:
        ValueError: If model prediction fails
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Task text must be a non-empty string")

    try:
        model = load_model()
        prediction = model.predict([text])[0]
        probabilities = model.predict_proba([text])[0]
        classes = model.classes_
        confidence = max(probabilities)
        all_scores = {
            cls: round(float(prob), 3)
            for cls, prob in zip(classes, probabilities)
        }

        result = RouterResult(
            routed_to=prediction,
            confidence=round(float(confidence), 3),
            all_scores=all_scores
        )
        logger.debug(f"Task routed to {prediction} with confidence {confidence:.3f}")
        return result
    except Exception as e:
        logger.error(f"Failed to route task: {e}", exc_info=True)
        raise ValueError(f"Routing failed: {e}") from e
