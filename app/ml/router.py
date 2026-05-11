from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from data.training_data import TRAINING_DATA

MODEL_PATH = "models/router_model.pkl"

def train_model():
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.15, random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf", LogisticRegression(max_iter=1000, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("\n=== Model Training Complete ===")
    print(classification_report(y_test, y_pred, zero_division=0))

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    print(f"Model saved to {MODEL_PATH}")
    return pipeline


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("No model found, training now...")
        return train_model()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def route_task(text: str) -> dict:
    model = load_model()
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    classes = model.classes_
    confidence = max(probabilities)
    all_scores = {cls: round(float(prob), 3) for cls, prob in zip(classes, probabilities)}

    return {
        "routed_to": prediction,
        "confidence": round(float(confidence), 3),
        "all_scores": all_scores
    }