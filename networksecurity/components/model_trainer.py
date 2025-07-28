import os
import sys
import joblib
import mlflow
import dagshub

from urllib.parse import urlparse

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

from networksecurity.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

# Initialize dagshub tracking
dagshub.init(repo_owner='DBGad', repo_name='NetworkSecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,Model_Trainer_Config:ModelTrainerConfig,Data_Transformation_Artifact:DataTransformationArtifact):
        try:
            self.Model_Trainer_Config =Model_Trainer_Config
            self.Data_Transformation_Artifact =Data_Transformation_Artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classificationmetric,run_name):
        try:
            with mlflow.start_run(run_name=run_name):
                f1_score=classificationmetric.f1_score
                precision_score=classificationmetric.precision_score
                recall_score=classificationmetric.recall_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision",precision_score)
                mlflow.log_metric("recall_score",recall_score)

                mlflow.log_artifact("final_model/model.pkl", artifact_path="model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_model(self,x_train,x_test,y_train,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    'splitter':['best','random'],
                    'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    'criterion':['gini', 'entropy', 'log_loss'],
                    'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    'criterion':['squared_error', 'friedman_mse'],
                    'max_features':['sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                } 
            }

            model_report:dict = evaluate_models(
                X_train=x_train, y_train=y_train,
                X_test=x_test, y_test=y_test,
                models=models, param=params
            )
            
            best_model_name = max(model_report, key=lambda x: model_report[x]['f1'])
            best_model_score = model_report[best_model_name]['f1']
            best_model_params = model_report[best_model_name]['best_params']
            best_model = models[best_model_name]

            best_model.set_params(**best_model_params)
            best_model.fit(x_train, y_train)
            save_object("final_model/model.pkl", best_model)
            # Train metrics
            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            self.track_mlflow(best_model, classification_train_metric, run_name=f"{best_model_name}_train")

            # Test metrics
            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            self.track_mlflow(best_model, classification_test_metric, run_name=f"{best_model_name}_test")

            # Save the final model
            preprocessor = load_object(file_path=self.Data_Transformation_Artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.Model_Trainer_Config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(self.Model_Trainer_Config.trained_model_file_path, obj=Network_Model)
            

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.Model_Trainer_Config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
         
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.Data_Transformation_Artifact.transformed_train_data_file_path
            test_file_path = self.Data_Transformation_Artifact.transformed_test_data_file_path

            train_arr = load_array_data(train_file_path)
            test_arr = load_array_data(test_file_path)

            x_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            return self.train_model(x_train, x_test, y_train, y_test)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
