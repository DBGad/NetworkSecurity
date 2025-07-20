from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifacts_entity import DataValidationArtifact
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import DataTransformationArtifact

import sys 


if __name__ == "__main__" : 
    try:
        Training_Pipeline_Config = TrainingPipelineConfig()
        Data_Ingestion_Config =DataIngestionConfig(Training_Pipeline_Config)
        Data_Ingestion = DataIngestion(Data_Ingestion_Config)
        Data_Ingestion_Artifact:DataIngestionArtifact = Data_Ingestion.initiate_data_ingestion()
        print(Data_Ingestion_Artifact.train_data_path)
        print(Data_Ingestion_Artifact.test_data_path)
        Data_Validation_Config = DataValidationConfig(Training_Pipeline_Config)
        Data_Validation =DataValidation(Data_Ingestion_Artifact,Data_Validation_Config)
        Data_Validation_Artifact:DataValidationArtifact = Data_Validation.initiate_data_validation()
        print(Data_Validation_Artifact)
        Data_Transformation_Config = DataTransformationConfig(Training_Pipeline_Config)
        Data_Transformation=DataTransformation(Data_Transformation_Config,Data_Validation_Artifact)
        Data_Transformation_Artifact:DataTransformationArtifact =Data_Transformation.initiate_data_transformation()
        print(Data_Transformation_Artifact) 

    except Exception as e :
        raise NetworkSecurityException(e,sys)