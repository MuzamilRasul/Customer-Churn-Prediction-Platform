import joblib
import pandas as pd
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Model artifacts
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.joblib"
MODEL_PATH = BASE_DIR / "models" / "lightgbm_churn_model.joblib"
THRESHOLD_PATH = BASE_DIR / "models" / "churn_threshold.joblib"


# Load artifacts
preprocessor = joblib.load(PREPROCESSOR_PATH)
model = joblib.load(MODEL_PATH)
threshold = joblib.load(THRESHOLD_PATH)


def predict_churn(customer_data: dict) -> dict:
    """
    Predict customer churn probability and class.
    """

    # Convert input dictionary to DataFrame
    df = pd.DataFrame([customer_data])

    # Transform input using the same preprocessor
    X_processed = preprocessor.transform(df)

    # Get churn probability
    churn_probability = model.predict_proba(X_processed)[0, 1]

    # Apply selected threshold
    churn_prediction = int(churn_probability >= threshold)

    return {
        "churn_prediction": churn_prediction,
        "churn_label": "Yes" if churn_prediction == 1 else "No",
        "churn_probability": round(float(churn_probability), 4),
        "threshold": threshold
    }