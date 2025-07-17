from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact

import sys 


if __name__ == "__main__" : 
    try:
        Training_Pipeline_Config = TrainingPipelineConfig()
        Data_Ingestion_Config =DataIngestionConfig(Training_Pipeline_Config)
        Data_Ingestion = DataIngestion(Data_Ingestion_Config)
        Data_Ingestion_Artifact:DataIngestionArtifact = Data_Ingestion.initiate_data_ingestion()
        print(Data_Ingestion_Artifact.train_data_path)
        print(Data_Ingestion_Artifact.test_data_path)
    except Exception as e :
        raise NetworkSecurityException(e,sys)