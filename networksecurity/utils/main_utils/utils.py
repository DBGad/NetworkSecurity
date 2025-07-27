import os 
import sys
import yaml
import pickle
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.base import clone
import optuna 



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

def load_object(file_path:str) :
    try :
        if not os.path.exists(file_path) :
            raise Exception(f'the file {file_path} is not exist')
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e :
        raise NetworkSecurityException(e,sys)
    
def load_array_data(file_path:str) -> np.array :
    try :
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e :
        raise NetworkSecurityException(e,sys)
    



def evaluate_models(X_train, y_train, X_test, y_test, models, param, n_trials=20):
    try:
        model_report = {}

        for model_name, model in models.items():
            def objective(trial):
                params = {}
                for key, values in param.get(model_name, {}).items():
                    if isinstance(values[0], float):
                        params[key] = trial.suggest_float(key, min(values), max(values), log=True)
                    elif isinstance(values[0],int) :
                        if len(set(values)) > 5 and max(values) - min(values) > 10:
                            params[key] = trial.suggest_int(key, min(values), max(values), step=1)
                        else:
                            params[key] = trial.suggest_categorical(key, values)
                    else:
                        params[key] = trial.suggest_categorical(key, values)

                trial_model = clone(model).set_params(**params)
                trial_model.fit(X_train, y_train)
                preds = trial_model.predict(X_test)
                metric = get_classification_score(y_test, preds)
                return metric.f1_score  # F1 Score هو الهدف الأساسي

            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=n_trials)

            # Train the best model again
            best_model = clone(model).set_params(**study.best_params)
            best_model.fit(X_train, y_train)
            y_pred = best_model.predict(X_test)
            metric = get_classification_score(y_test, y_pred)

            model_report[model_name] = {
                "f1": metric.f1_score,
                "precision": metric.precision_score,
                "recall": metric.recall_score,
                "best_params": study.best_params,
            }

        return model_report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
