import os 
import sys
import json
import certifi
import pandas as pd 
import numpy as np 
import pymongo

from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging



load_dotenv() 

MONGO_DB_URL = os.getenv('MONGO_DB_URL')

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path:str) :
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            records = list(json.loads(data.T.to_json()).values()) 

            return records 
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        
    def insert_to_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records =records 

            self.mongo = pymongo.MongoClient(MONGO_DB_URL)  

            self.database = self.mongo[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records) 
        except Exception as e :
            raise NetworkSecurityException(e,sys)
        

if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="GADELHAQAI"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_to_mongo(records,DATABASE,Collection)
    print(no_of_records)