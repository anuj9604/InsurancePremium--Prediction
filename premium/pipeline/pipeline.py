from premium.config.configuration import *
from premium.component.data_ingestion import *
from premium.logger import logging
from premium.exception import PremiumException

from premium.entity.artifact_entity import DataIngestionArtifact
from premium.entity.config_entity import DataIngestionConfig

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

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_data_transformation(self):
        try:
            pass
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

        except Exception as e:
            raise PremiumException(e, sys) from e
