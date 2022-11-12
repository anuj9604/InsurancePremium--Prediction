from premium.config.configuration import *
from premium.logger import logging
from premium.exception import PremiumException

from premium.entity.artifact_entity import *
from premium.entity.config_entity import *

from premium.component.data_ingestion import *
from premium.component.data_validation import *
from premium.component.data_transformation import *

import os, sys

class Pipeline:

    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config=config

        except Exception as e:
            raise PremiumException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_data_validation(self, data_ingestion_artifact) -> DataValidationArtifact:
        try:
            data_validation=DataValidation(data_validation_config=self.config.get_data_validation_config(), data_ingestion_artifact=data_ingestion_artifact)
            
            return data_validation.initiate_data_validation()

        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(data_transformation_config=self.config.get_data_transformation_config(), data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)

            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_model_training(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_model_push(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e,sys) from e
    
    def run_pipeline(self):
        try:
            #data ingestion
            data_ingestion_artifact=self.start_data_ingestion()
            #data validation
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            #data transformation
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)


            return None

        except Exception as e:
            raise PremiumException(e, sys) from e
