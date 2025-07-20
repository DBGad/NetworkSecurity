import os 
import sys 
import numpy as np 
import pandas as pd 

"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")



""" 
Data Ingestion Related Constant like -> DATA_INGESTION VAR NAME
"""

DATA_INGESTION_DATABASE_NAME = "GADELHAQAI"
DATA_INGESTION_COLLECTION_NAME ="NetworkData"
DATA_INGESTION_DIR_NAME :str = "data_ingestion"
DATA_INGESTION_FEATURE_STRORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR :str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2 


""" 
Data Validation Related Constant like -> DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME :str = 'data_validation'
DATA_VALIDATION_VALID_DATA_DIR :str = 'validated'
DATA_VALIDATION_INVALID_DATA_DIR :str = 'invalidated'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str = 'report.yaml'


""" 
Data Transformation Related Constant like -> DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str = 'data_transformation'
DATA_TRANSFORMATION_DATA_TRANSFORMED_DIR:str = 'transformed'
DATA_TRANSFORMATION_MODEL_DIR:str = 'transformed_object'
DATA_TRANSFORMATION_MODEL_FILE_NAME:str = 'preporocessor.pkl'
DATA_TRANSFORMATION_TRAIN_FILE_NAME: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_NAME: str = "test.npy"
## Knn imputer to replace nan vlaues
DATA_TRANSFORMATION_IMPUTER_PARAMS :dict ={
    'missing_values' : np.nan,
    'n_neighbors':3,
    'weights' : 'uniform'
} 