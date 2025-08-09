# 🛡️ NetworkSecurity

A complete system for malicious website (phishing) detection using **Machine Learning**, built with **FastAPI** and a full data processing pipeline from ingestion to deployment.  
The project supports automated model training with **Optuna** to select the best-performing model, and can sync artifacts/models to **AWS S3**.

---

## 🚀 Features
- Full Data Pipeline: Ingestion → Validation → Transformation.
- Automated Model Selection: Trains multiple models and uses Optuna for hyperparameter tuning.
- AWS S3 Integration: Automatically uploads models and artifacts.
- FastAPI Service: Real-time predictions via REST API.
- Custom Logging: Centralized logging system.
- Custom Exception Handling: Easier error tracing.
- Clean Modular Structure: Components / Utils / Entities separation.
- CI/CD Ready: GitHub Actions workflows included.
- AWS Deployment: Dockerized application deployed to AWS ECR & EC2 for production-ready hosting.


---
## 📊 Model Training & Pipeline Overview
1. **Data Ingestion** → Load raw dataset and split into train/test sets.  
2. **Data Validation** → Ensure data matches `schema.yaml` before processing.  
3. **Data Transformation** → Feature engineering, encoding, and scaling.  
4. **Model Training** → Multiple ML models are trained, with hyperparameters tuned via **Optuna**.  
5. **Model Evaluation** → Best model selected based on classification metrics.  
6. **Deployment** → Final model is stored in AWS S3, Dockerized, and deployed to AWS EC2.
---
## 📂 Project Structure
```bash
NetworkSecurity/
│   .env
│   .gitignore
│   app.py
│   Dockerfile
│   main.py
│   push_data.py
│   requirements.txt
│   setup.py
│
├───.github
│   └───workflows
│           main.yml                # CI/CD pipeline with GitHub Actions
│
├───data_schema
│       schema.yaml                 # Data validation schema
│
├───networksecurity
│   │   __init__.py
│   │
│   ├───cloud
│   │       s3_syncer.py            # AWS S3 sync utilities
│   │
│   ├───components
│   │       data_ingestion.py       # Load and split raw data
│   │       data_transformation.py  # Preprocess and engineer features
│   │       data_validation.py      # Validate against schema
│   │       model_trainer.py        # Train and optimize model
│   │
│   ├───constant
│   │       __init__.py             # Constants and configs
│   │
│   ├───entity
│   │       artifacts_entity.py     # Artifact data classes
│   │       config_entity.py        # Config data classes
│   │
│   ├───exception
│   │       exception.py            # Custom exception handling
│   │
│   ├───logging
│   │       logger.py               # Logging setup
│   │
│   ├───pipeline
│   │       batch_prediction.py     # Batch prediction pipeline
│   │       training_pipeine.py     # Model training pipeline
│   │
│   ├───utils
│   │   ├───main_utils
│   │   │       utils.py            # General helper functions
│   │   ├───ml_utils
│   │   │   ├───metric
│   │   │   │       classification_metric.py # Model evaluation metrics
│   │   │   ├───model
│   │   │   │       estimator.py    # ML model wrapper and persistence
│
├───Network_Data
│       phisingData.csv
│
├───prediction_output
│       output.csv
│
├───templates
│       table.html
│
├───valid_data
│       test.csv
│
└───README.md
```

## ⚙️ Installation 
# Clone the repository
```bash
git clone https://github.com/DBGad/NetworkSecurity.git
cd NetworkSecurity
```

# Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
# Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage 

# Run FastAPI Server
```bash
uvicorn app:app --reload
```
# Server will be available at:
```bash
http://127.0.0.1:8000/docs
```
