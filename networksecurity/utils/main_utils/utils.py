import os 
import sys
import yaml
import pickle
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(File_path:str) -> dict:
    try:
        with open(File_path , 'rb') as file_obj :
            content = yaml.safe_load(file_obj)
            return content
    except Exception as e :
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(File_path:str , content:str , replace = False):
    try:
        if replace:
            if os.path.exists(File_path):
                os.remove(File_path)
        os.makedirs(os.path.dirname(File_path), exist_ok=True)
        with open(File_path , 'w') as file_obj :
            yaml.dump(content,file_obj)
    except Exception as e :
        raise NetworkSecurityException(e,sys)
    
def save_array_data (file_path:str,array:np.array):
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e :
        raise NetworkSecurityException(e,sys)
    

def save_object (file_path:str, obj:object) :
    try:
        logging.info("Entered the save_object method of MainUtils class")
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e :
        raise NetworkSecurityException(e,sys)