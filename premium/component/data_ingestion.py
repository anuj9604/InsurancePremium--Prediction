from premium.entity.config_entity import DataIngestionConfig
from premium.entity.artifact_entity import DataIngestionArtifact
from premium.exception import PremiumException
import requests
from premium.logger import logging
import os,sys
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f'{"="*20} Data Ingestion log started {"="*20}')
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def download_insurance_data(self):
        try:
            csv_url=self.data_ingestion_config.dataset_download_url

            csv_data_dir=self.data_ingestion_config.csv_download_dir

            os.makedirs(csv_data_dir, exist_ok=True)

            insurance_file_name=os.path.basename(csv_url)

            csv_file_path=os.path.join(csv_data_dir, insurance_file_name)

            logging.info(f"CSV data download starting from the source {csv_url}")
            req=requests.get(csv_url)
            content=req.content
            with open(csv_file_path, "w") as filo:
                filo.write(content.decode("utf-8"))
            logging.info(f"csv_file {insurance_file_name} has been downloaded successfullt to: {csv_file_path}")

            return csv_file_path
            
        except Exception as e:
            raise PremiumException(e,sys) from e

    def train_test_split(self):
        try:
            csv_file_path=self.download_insurance_data()

            file_name=os.path.basename(csv_file_path)

            logging.info("Reading the downloaded csv file")
            premium_df=pd.read_csv(csv_file_path)

            premium_df['category']=pd.cut(premium_df['expenses'], bins=[0, 11563.5, 22005, 32446.5, 42888, 53329.5, np.inf], labels=[0,1,2,3,4,5])

            strat_train_set= None
            strat_test_set= None

            split=StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            logging.info("Splitting Data into Train and Test")
            for train_index, test_index in split.split(premium_df, premium_df["category"]):
                strat_train_set = premium_df.loc[train_index].drop(["category"], axis=1)
                strat_test_set=premium_df.loc[test_index].drop(["category"], axis=1)

            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)

            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            """if os.path.exists(self.data_ingestion_config.ingested_train_dir):
                os.remove(self.data_ingestion_config.ingested_train_dir)

            if os.path.exists(self.data_ingestion_config.ingested_test_dir):
                os.remove(self.data_ingestion_config.ingested_test_dir)"""

            logging.info("Making Train Directory and loading the train data")
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path)

            logging.info("Making Test Directory and loading the test data")
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                strat_test_set.to_csv(test_file_path)

            data_ingestion_artifact=DataIngestionArtifact(csv_file_path=csv_file_path, train_file_path=train_file_path, test_file_path=test_file_path, is_ingested=True, message="Data Ingested Successfully")
            logging.info("Data Ingestion Completed successfully")
            return data_ingestion_artifact

        except Exception as e:
            raise PremiumException(e,sys) from e

    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating Data Ingestion Process")
            return self.train_test_split()

        except Exception as e:
            raise PremiumException(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log complete.{'='*20} \n\n")
