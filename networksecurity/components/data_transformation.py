import os 
import sys 
import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import DataValidationArtifact
from networksecurity.entity.artifacts_entity import DataTransformationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.utils.main_utils.utils import save_array_data
from networksecurity.utils.main_utils.utils import save_object



class DataTransformation:
    def __init__(self,Data_Transformation_Config:DataTransformationConfig,
                 Data_Validation_Artifact:DataValidationArtifact):
        try:
            self.Data_Transformation_Config =Data_Transformation_Config
            self.Data_Validation_Artifact = Data_Validation_Artifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame :
        try:
            return pd.read_csv(file_path)
        except Exception as e :
            raise NetworkSecurityException(e,sys)

    def get_transformed_obj(self) -> Pipeline:
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline(steps=[('imputer',imputer)])
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            return pipeline
        except Exception as e :
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact :
        logging.info('enter initiate data transformation')
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.Data_Validation_Artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.Data_Validation_Artifact.valid_test_file_path)

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_transformed_obj()
            transformed_input_feature_train_df=preprocessor.fit_transform(input_feature_train_df)
            transformed_input_feature_test_df = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_feature_train_df,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_test_df,np.array(target_feature_test_df)]

            save_array_data(self.Data_Transformation_Config.transformed_train_file_path,train_arr)
            save_array_data(self.Data_Transformation_Config.transformed_test_file_path,test_arr)
            save_object(self.Data_Transformation_Config.transformed_object_file_path,preprocessor)

            data_transformation_artifact=DataTransformationArtifact(self.Data_Transformation_Config.transformed_train_file_path,
                                                                    self.Data_Transformation_Config.transformed_test_file_path,
                                                                   self.Data_Transformation_Config.transformed_object_file_path )
            return data_transformation_artifact
        
        except Exception as e :
            raise NetworkSecurityException(e,sys)