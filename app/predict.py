from pathlib import Path
import sys

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_features import add_engineered_features


MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "random_forest_undersampling_ensemble_threshold_060.joblib"
)

setattr(sys.modules["__main__"], "add_engineered_features", add_engineered_features)

artifact = joblib.load(MODEL_PATH)
ensemble = artifact["ensemble"]
estimators = ensemble["estimators"]
threshold = ensemble["threshold"]
feature_columns = artifact["feature_columns"]
class_mapping = ensemble["class_mapping"]


def predict_diabetes(input_data):
    input_df = pd.DataFrame([input_data])
    input_df = input_df[feature_columns]

    probabilities = [
        estimator.predict_proba(input_df)[:, 1]
        for estimator in estimators
    ]
    diabetes_probability = sum(probabilities) / len(probabilities)
    prediction = (diabetes_probability >= threshold).astype(int)
    prediction_value = int(prediction[0])

    return {
        "prediction": prediction_value,
        "prediction_label": class_mapping[prediction_value],
        "diabetes_probability": float(diabetes_probability[0]),
        "threshold": float(threshold),
    }


if __name__ == "__main__":
    sample_input = {
        "HighBP": 1,
        "HighChol": 1,
        "CholCheck": 1,
        "BMI": 30,
        "Smoker": 0,
        "Stroke": 0,
        "HeartDiseaseorAttack": 0,
        "PhysActivity": 1,
        "Fruits": 1,
        "Veggies": 1,
        "HvyAlcoholConsump": 0,
        "AnyHealthcare": 1,
        "NoDocbcCost": 0,
        "GenHlth": 3,
        "MentHlth": 0,
        "PhysHlth": 0,
        "DiffWalk": 0,
        "Sex": 0,
        "Age": 9,
        "Education": 5,
        "Income": 6,
    }

    print(predict_diabetes(sample_input))
