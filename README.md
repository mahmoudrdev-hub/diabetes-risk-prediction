# Diabetes Risk Prediction API

A machine learning project that predicts whether a person is at risk of diabetes using survey-style health indicators.

The project includes a trained classification workflow, a FastAPI backend, and Docker support for running the API in a reproducible environment.

## Project Overview

This project was built as an end-to-end machine learning workflow:

- Data exploration and preprocessing
- Model training and evaluation
- Handling class imbalance
- Saving the final trained model
- Building an API with FastAPI
- Dockerizing the API
- Preparing the project for GitHub and portfolio use

The API accepts health-related input features and returns:

- The predicted class
- The diabetes risk probability
- A readable prediction label

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- PyArrow
- Hugging Face Hub
- FastAPI
- Uvicorn
- Docker
- Git / GitHub

## Project Structure

```text
diabetes-risk-prediction/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- predict.py
|   `-- schemas.py
|-- models/
|   `-- diabetes_risk_model.joblib  (downloaded locally, not included in GitHub)
|-- notebooks/
|   `-- 01_eda.ipynb
|-- reports/
|   `-- screenshots/
|       |-- swagger-overview.png
|       `-- swagger-predict-expanded.png
|-- src/
|   `-- model_features.py
|-- Dockerfile
|-- .dockerignore
|-- .gitignore
|-- download_model.py
|-- requirements.txt
`-- README.md
```

## Model

The trained model file is hosted on Hugging Face Hub and is not included directly in this GitHub repository because it is too large for GitHub.

Model repository:

```text
https://huggingface.co/MahmoudRamadanDev/diabetes-risk-prediction-rf
```

The API expects the model file to exist locally at:

```text
models/diabetes_risk_model.joblib
```

Install the project requirements and download the model before starting the API:

```powershell
pip install -r requirements.txt
python download_model.py
```

The model file is ignored by Git using `.gitignore`, so it can remain available locally without being pushed to GitHub.

## API Endpoint

### `POST /predict`

This endpoint receives patient health features and returns a diabetes risk prediction.

## Example Request

```json
{
  "HighBP": 1,
  "HighChol": 1,
  "CholCheck": 1,
  "BMI": 28.5,
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
  "PhysHlth": 2,
  "DiffWalk": 0,
  "Sex": 1,
  "Age": 8,
  "Education": 5,
  "Income": 6
}
```

## Example Response

```json
{
  "prediction": 1,
  "diabetes_probability": 0.7935,
  "prediction_label": "Prediabetes or diabetes"
}
```

## How to Run Locally Without Docker

Open PowerShell inside the project folder:

```powershell
cd "C:\Users\cs\Desktop\diabetes-risk-prediction"
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

Download the model from Hugging Face:

```powershell
python download_model.py
```

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## How to Run With Docker

Make sure Docker Desktop is running.

From the project folder, build the Docker image:

```powershell
docker build -t diabetes-risk-api .
```

Download the model if it is not already available locally:

```powershell
python download_model.py
```

Run the container and mount the local `models` folder:

```powershell
docker run -d --name diabetes-risk-api-test -p 8000:8000 -v "${PWD}\models:/app/models:ro" diabetes-risk-api
```

Then open the Swagger UI:

```text
http://127.0.0.1:8000/docs
```

The `-v "${PWD}\models:/app/models:ro"` part mounts the local `models` folder into the Docker container as read-only, allowing the API to access the model without copying the large model file into the Docker image.

## Stop and Remove the Docker Container

After testing, stop and remove the container:

```powershell
docker rm -f diabetes-risk-api-test
```

## Verification Commands

These commands can be used to verify that the repository and Docker setup are working correctly.

Check Git status:

```powershell
git status
```

Expected result:

```text
nothing to commit, working tree clean
```

Check that the model file is not tracked by Git:

```powershell
git ls-files models
```

Expected result: no output.

Check that the Python files compile correctly:

```powershell
python -m py_compile app/main.py app/schemas.py
```

Expected result: no output.

Build the Docker image:

```powershell
docker build -t diabetes-risk-api .
```

Expected result: build succeeds.

## Swagger API Docs

After running the API, Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Screenshots:

![Swagger overview](reports/screenshots/swagger-overview.png)

![Predict endpoint expanded](reports/screenshots/swagger-predict-expanded.png)

## Notes

This project is intended for machine learning portfolio demonstration and experimentation.

It is not intended for real medical diagnosis or clinical decision-making.
