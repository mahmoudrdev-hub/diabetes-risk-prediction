import os

from huggingface_hub import hf_hub_download


MODEL_REPO_ID = "MahmoudRamadanDev/diabetes-risk-prediction-rf"
MODEL_FILENAME = "diabetes_risk_model.joblib"
MODEL_DIR = "models"


os.makedirs(MODEL_DIR, exist_ok=True)

model_path = hf_hub_download(
    repo_id=MODEL_REPO_ID,
    filename=MODEL_FILENAME,
    local_dir=MODEL_DIR,
)

print(f"Model downloaded to {model_path}")
