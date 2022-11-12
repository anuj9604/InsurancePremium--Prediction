from premium.exception import PremiumException
from premium.logger import logging
from premium.entity.config_entity import DataTransformationConfig
from premium.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from premium.util.util import *
from premium.constant import *

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import os, sys

class DataTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, columns=None):
        try:
            self.columns=columns
        except Exception as e:
            raise PremiumException(e,sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
           X=X.drop(self.columns, axis=1)
           generated_data=X.to_numpy()
           logging.info(f"Returning dataframe without trivial columns: {X.columns}")
           return generated_data

        except Exception as e:
            raise PremiumException(e,sys) from e


class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact):
        logging.info(f"{'='*20}Data Transformation log started{'='*20}")
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_data_transformation_object(self):
        try:
            
            schema_file_path=self.data_validation_artifact.schema_file_path

            dataset_schema=read_yaml_file(file_path=schema_file_path)

            input_columns=dataset_schema[INPUT_COLUMNS]
            trivial_columns=dataset_schema[TRIVIAL_COLUMNS]
            categorical_columns=dataset_schema[CATEGORICAL_COLUMNS]

            omit_pipeline=Pipeline(steps=[('data_transformer', DataTransformer(columns=trivial_columns))])

            cat_pipeline=Pipeline(steps=[('one_hot_encoder', OneHotEncoder())])

            preprocessing = ColumnTransformer([
                ('omit_pipeline', omit_pipeline, input_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns)
            ])

            logging.info("Running Data Transformation Pipelines.")

            return preprocessing

        except Exception as e:
            raise PremiumException(e,sys) from e

    def initiate_data_transformation(self):

        try:
            preprocessing_obj=self.get_data_transformation_object()

            logging.info("preprocessing object loaded")

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            schema_file_path=self.data_validation_artifact.schema_file_path

            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            schema=read_yaml_file(file_path=schema_file_path)

            target_column_name=schema[TARGET_COLUMNS]

            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Loading train-test data in transformation pipeline")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            logging.info("Loading train-test data successful")

            train_arr=np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            train_arr=np.delete(train_arr, [2,3], axis=1)
            test_arr=np.delete(test_arr, [2,3], axis=1)

            train_file_name=os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name=os.path.basename(test_file_path).replace(".csv", ".npz")

            transformed_train_file_path=os.path.join(self.data_transformation_config.transformed_train_dir, train_file_name)
            transformed_test_file_path=os.path.join(self.data_transformation_config.transformed_test_dir, test_file_name)

            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            logging.info(f"transformed train file saved")
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)
            logging.info(f"transformed test file saved")

            preprocessing_obj_file_path=self.data_transformation_config.preprocessed_object_file_path

            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)

            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=transformed_train_file_path, transformed_test_file_path=transformed_test_file_path, preprocessed_object_file_path=preprocessing_obj_file_path, is_transformed=True, message= "Data Transformation complete.")

            logging.info(f"Data Transformation Artifact: {data_transformation_artifact}")
            
            return data_transformation_artifact

        except Exception as e:
            raise PremiumException(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Transformation log completed.{'='*20}\n\n")



