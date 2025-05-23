import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initial_model_trainer(self, train_array, test_array):
        try:
            logging.info("Spliting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regressor": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBoost Regressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),                        
                }
            
            params = {
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features': ['sqrt', log2',None],
                    'n_estimators': [8,16, 32, 64, 128, 256]
                },
                "Decision Tree": {
                    'criterion':['squared_error','friedman_mse', 'absolute_error','poisson'],
                    # 'splitter': ['best','random'],
                    # 'max_features': ['sqrt','log2'],
                },
                "Gradient Boosting":{
                    # 'loss': ['squared_error','huber', 'absolute_error','quantile'],
                    'learning_rate': [0.6, 0.7, 0.75, 0.8, 0.9],
                    # 'criterion': ['squared_error', 'friedman_mse'],
                    # 'max_features' : ['auto', 'sqrt', 'log2'],
                    'n_estimators': [8, 16, 32, 64, 128, 256],
                },
                "Linear Regressor": {},
                "K-Neighbors Regressor": {
                    'n_neighbors':[5,7,9,11],
                    # 'weights' : ['uniform', 'distance'],
                    # 'algorithm' : ['ball_tree', 'kd_tree', 'brute']
                },
                "XGBoost Regressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth':[6,8,10],
                    'learning_rate':[0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1, .01, 0.5, .001],
                    # 'loss' : ['linear','square','exponential'],
                    'n_estimators':[8,16,32,64,128,256]
                },
                
            }

            model_report:dict=evaluate_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset is {best_model_name} with score of {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2Score = r2_score(y_test, predicted)

            return r2Score
        
        except Exception as e:
            raise CustomException(e, sys)