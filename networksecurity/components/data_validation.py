import os
import sys 
import numpy as np 
import pandas as pd 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig

from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from networksecurity.entity.artifacts_entity import DataValidationArtifact

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.utils.main_utils.utils import write_yaml_file
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self,Data_Ingestion_Artifact:DataIngestionArtifact,
                 Data_Validation_Config:DataValidationConfig):
        try:
            self.Data_Ingestion_Artifact =Data_Ingestion_Artifact
            self.Data_Validation_Config = Data_Validation_Config
            self._schema_config =read_yaml_file( SCHEMA_FILE_PATH)
        except Exception as e :
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(File_path:str) -> pd.DataFrame :
        try:
            return pd.read_csv(File_path)
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,df:pd.DataFrame)-> bool:
        try:
            number_of_columns =len(self._schema_config['columns'])
            logging.info(f'Required number of columns: {number_of_columns}') 
            logging.info(f"Data has {len(df.columns)} columns")
            if len(df.columns) == number_of_columns :
                return True
            return False
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_columns(self,df:pd.DataFrame)-> bool :
        try:
            list_of_numerical_columns_name_schema = set(self._schema_config['numerical_columns'])
            list_of_numerical_columns_name_df = set(df.select_dtypes(include=np.number).columns)

            if list_of_numerical_columns_name_schema != list_of_numerical_columns_name_df:
                missing_in_df = list_of_numerical_columns_name_schema - list_of_numerical_columns_name_df
                extra_in_df = list_of_numerical_columns_name_df - list_of_numerical_columns_name_schema
                logging.info(f"Missing columns in DataFrame: {missing_in_df}")
                logging.info(f"Extra numerical columns in DataFrame: {extra_in_df}")
                return False
            
            logging.info('All Numerical Columns are Okay ')
            return True
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self,df1_base:pd.DataFrame ,df2_base:pd.DataFrame,threshold = 0.05)-> bool:
        try:
            status = True
            report ={}
            for col in df1_base.columns:
                df1 = df1_base[col]
                df2 = df2_base[col]

                is_same_dist = ks_2samp(df1,df2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    logging.info('the distribution is not the same')
                    is_found = True
                    status = False
                report.update({col : {'P-Value': float(is_same_dist.pvalue),
                                      "drift_status" : is_found}})
            write_yaml_file(self.Data_Validation_Config.drift_report_file_path,report)
            return status
        except Exception as e :
            raise NetworkSecurityException(e,sys)


    def write_validation_status(self,path:str,train:pd.DataFrame,test:pd.DataFrame,status:bool) -> DataValidationArtifact:
        try:
            os.makedirs(os.path.dirname(path),exist_ok=True)
            if status:
                train.to_csv(
                    self.Data_Validation_Config.valid_train_file_path,index=False,header=True
                )
                test.to_csv(
                    self.Data_Validation_Config.valid_test_file_path,index=False,header=True
                )
                data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.Data_Ingestion_Artifact.train_data_path,
                valid_test_file_path=self.Data_Ingestion_Artifact.test_data_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.Data_Validation_Config.drift_report_file_path,
                )
            else :
                train.to_csv(
                    self.Data_Validation_Config.invalid_train_file_path,index=False,header=True
                )
                test.to_csv(
                    self.Data_Validation_Config.invalid_test_file_path,index=False,header=True
                )
                data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=None,
                valid_test_file_path=None,
                invalid_train_file_path=self.Data_Validation_Config.invalid_train_file_path,
                invalid_test_file_path=self.Data_Validation_Config.invalid_test_file_path,
                drift_report_file_path=self.Data_Validation_Config.drift_report_file_path,
                )

            return data_validation_artifact

        except Exception as e :
            raise NetworkSecurityException(e,sys)


    def initiate_data_validation(self) ->DataValidationArtifact :
        try:
            logging.info('initiate data validation ')
            error_message :list =[]
            train_df = DataValidation.read_data(self.Data_Ingestion_Artifact.train_data_path)
            test_df = DataValidation.read_data(self.Data_Ingestion_Artifact.test_data_path)

            # validate number of columns 
            status1_check = self.validate_number_of_columns(train_df)
            if not status1_check:
                error_mess = "Train dataframe does not contain all columns.\n"
                error_message.append(error_mess)

            status1_check = self.validate_number_of_columns(test_df)
            if not status1_check:
                error_mess = "Test dataframe does not contain all columns.\n"
                error_message.append(error_mess)

            # vaidate numerical columns 
            status2_check = self.validate_numerical_columns(train_df)
            if not status2_check:
                error_mess = "Train dataframe does not contain all Numerical columns.\n"
                error_message.append(error_mess)

            status2_check = self.validate_numerical_columns(test_df)
            if not status2_check:
                error_mess = "Test dataframe does not contain all Numerical columns.\n"
                error_message.append(error_mess)

            status3_check = self.detect_dataset_drift(train_df,test_df)
            if not status3_check:
                error_mess = "the distribution is not the same.\n"
                error_message.append(error_mess)

            if status1_check and status2_check and status3_check:
                data_validation_artifact = self.write_validation_status(
                    self.Data_Validation_Config.valid_train_file_path,
                    train_df,test_df,True
                )
                logging.info('Everything is okay')

            else :
                data_validation_artifact = self.write_validation_status(
                    self.Data_Validation_Config.invalid_train_file_path,
                    train_df,test_df,False
                )
                logging.info(f'there is issue with this info {error_message}')


            return data_validation_artifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)