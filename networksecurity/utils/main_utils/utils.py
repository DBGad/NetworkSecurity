import os 
import sys
import yaml

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