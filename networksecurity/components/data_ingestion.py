import sys 
import os 
import numpy as np 
import pandas as pd 
import pymongo 

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifacts_entity import DataIngestionArtifact

from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

import certifi
ca = certifi.where()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,DataIngestionConfig:DataIngestionConfig):
        try:
            logging.info("Data Ingestion Config object was initiate")
            self.Data_Ingestion_Config = DataIngestionConfig
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.Data_Ingestion_Config.database_name
            collection_name = self.Data_Ingestion_Config.collection_name
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            logging.info(f"Read Data from MongoDB with {collection.count_documents({})} Records Sucssesfully")

            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df = df.drop(columns=['_id'],axis=1)
            
            df.replace({'na':np.nan},inplace=True)
            logging.info(f"Convert Collection to Pandas Data Frame")
            return df
        except Exception as e :
            raise NetworkSecurityException(e,sys)

    def export_data_to_featrue_store(self,dataframe: pd.DataFrame):
        try:
            featrue_store_file_path = self.Data_Ingestion_Config.feature_store_file_path
            dir_path = os.path.dirname(featrue_store_file_path)

            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(featrue_store_file_path,index=False,header=True)

            return dataframe
            
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,datafram: pd.DataFrame) :
        try:
            train_data, test_data =train_test_split(datafram,
                        test_size=self.Data_Ingestion_Config.train_test_ratio)
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            dir_path = os.path.dirname(self.Data_Ingestion_Config.training_file_path)
            logging.info(f"Exporting train and test file path.")
            os.makedirs(dir_path,exist_ok=True)

            train_data.to_csv(self.Data_Ingestion_Config.training_file_path,index=False,header=True)
            test_data.to_csv(self.Data_Ingestion_Config.test_file_path,index=False,header=True)
            logging.info(f"Exported train and test file path.")            
        except Exception as e :
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_featrue_store(dataframe=dataframe)
            self.split_data_as_train_test(datafram=dataframe)

            Data_Ingestion_Artifact = DataIngestionArtifact(train_data_path=self.Data_Ingestion_Config.training_file_path,
                                                test_data_path=self.Data_Ingestion_Config.test_file_path)
        
            return Data_Ingestion_Artifact
        except Exception as e :
            raise NetworkSecurityException(e,sys)

