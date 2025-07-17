from datetime import datetime 
import os 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        self.timestamp = timestamp.strftime("%d_%m_%y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name ,self.timestamp )


class DataIngestionConfig:
    def __init__(self,Training_Pipeline_Config : TrainingPipelineConfig):
        self.data_ingestio_dir:str = os.path.join (
            Training_Pipeline_Config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path :str = os.path.join(
            self.data_ingestio_dir,training_pipeline.DATA_INGESTION_FEATURE_STRORE_DIR,training_pipeline.FILE_NAME
        )
        self.training_file_path:str = os.path.join(
            self.data_ingestio_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME
        )
        self.test_file_path : str = os.path.join(
            self.data_ingestio_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME
        )
        self.train_test_ratio :float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name :str =training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name :str = training_pipeline.DATA_INGESTION_DATABASE_NAME

        
