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

        
class DataValidationConfig :
    def __init__(self,Training_Pipeline_Config:TrainingPipelineConfig):

        self.data_validation_dir :str = os.path.join(
            Training_Pipeline_Config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME
        ) 
        self.valid_data_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DATA_DIR)
        self.invalid_data_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DATA_DIR)
        self.valid_train_file_path :str = os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path :str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path :str = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path :str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR) 
        self.drift_report_file_path:str = os.path.join(self.drift_report_dir ,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

        
class DataTransformationConfig :
    def __init__(self,Training_Pipeline_Config : TrainingPipelineConfig):
        self.data_transformation_dir :str = os.path.join(Training_Pipeline_Config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.data_transformed_dir :str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_DATA_TRANSFORMED_DIR)
        self.transformed_train_file_path :str = os.path.join(self.data_transformed_dir,training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_NAME)
        self.transformed_test_file_path: str  = os.path.join(self.data_transformed_dir,training_pipeline.DATA_TRANSFORMATION_TEST_FILE_NAME)
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_MODEL_DIR,training_pipeline.DATA_TRANSFORMATION_MODEL_FILE_NAME)