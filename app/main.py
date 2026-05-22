from pathlib import Path
from functools import lru_cache
import sys

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.schemas import PatientData, PredictionResponse


app = FastAPI()

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "diabetes_risk_model.joblib"
)


@app.get("/health")
def health():
    return {"status": "ok"}


@lru_cache(maxsize=1)
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except ModuleNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model needs a missing Python module: {exc.name}",
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model file was not found: {MODEL_PATH}",
        ) from exc


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PatientData):
    try:
        model_artifact = load_model()
        input_df = pd.DataFrame([data.dict()])

        if isinstance(model_artifact, dict) and "ensemble" in model_artifact:
            ensemble = model_artifact["ensemble"]
            feature_columns = model_artifact.get("feature_columns", input_df.columns)
            input_df = input_df[list(feature_columns)]

            estimators = ensemble["estimators"]
            threshold = ensemble.get("threshold", 0.5)
            class_mapping = ensemble.get("class_mapping", {})

            probabilities = [
                estimator.predict_proba(input_df)[0][1] for estimator in estimators
            ]
            probability = sum(probabilities) / len(probabilities)
            prediction = int(probability >= threshold)
            prediction_label = class_mapping.get(prediction)
        else:
            prediction = model_artifact.predict(input_df)[0]
            probability = model_artifact.predict_proba(input_df)[0][1]
            prediction_label = None
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {type(exc).__name__}: {exc}",
        ) from exc

    response = {
        "prediction": int(prediction),
        "diabetes_probability": round(float(probability), 4),
    }

    if prediction_label:
        response["prediction_label"] = prediction_label

    return response


if __name__ == "__main__":
    import threading
    import webbrowser

    import uvicorn

    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000/docs")).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
