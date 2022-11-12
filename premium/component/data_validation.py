from premium.constant import DATA_INGESTION_ARTIFACT_DIR
from premium.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from premium.entity.config_entity import DataValidationConfig

from premium.exception import PremiumException
from premium.logger import logging

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import yaml
import pandas as pd
from yaml.loader import SafeLoader
import os,sys
import json

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Validation Stage Started{'='*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise PremiumException(e,sys) from e

    def check_split(self):
        try:
            logging.info("checking if train test split file exists.")

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_exist=os.path.exists(train_file_path)
            is_test_exist=os.path.exists(test_file_path)

            logging.info(f"Does train-test split exists -> {is_train_exist and is_test_exist}")

            if not is_train_exist and is_test_exist:
                message=f"Training file: {train_file_path} and Testing file: {test_file_path} is not present"
                logging.info(message)
                raise Exception(message)

            return is_train_exist and is_test_exist

        except Exception as e:
            raise PremiumException(e,sys) from e     

    def validate_dataset_schema(self):
        try:
            
            with open(self.data_validation_config.schema_file_path) as f:
                data = yaml.load(f, Loader=SafeLoader)
            my_df=pd.read_csv(self.data_ingestion_artifact.csv_file_path)
            

            #checking correct column names and number of columns
            if len(my_df.columns)!=len(data['columns']):
                logging.error(f"number of columns({len(my_df.columns)}) in the downloaded dataset {self.data_ingestion_artifact.csv_file_path} are incorrect. Number of columns should be {len(data['columns'])}")
                validation_status=False
                return validation_status
            

            l1=[]
            for _ in data['columns']:
                l1.append((_, data['columns'][_]))
            l2=[]
            for _ in my_df.dtypes.index:
                l2.append((_, str(my_df.dtypes[_])))
            l3=[]
            for _ in l2:
                if _ not in l1:
                    l3.append(_)

            if l3:
                validation_status=False
            else:
                validation_status=True

            logging.info(f"Columns {l3} are not part of the correct schema. Is downloaded data correct? {validation_status}")

            return validation_status

        except Exception as e:
            raise PremiumException(e,sys) from e
   
    def generate_data_drift_report(self):
        try:
            data_ingestion_artifact_dir=os.path.dirname(os.path.dirname(os.path.dirname(self.data_ingestion_artifact.csv_file_path)))
            only_csv_data_dir=os.path.join(os.path.basename(os.path.dirname(self.data_ingestion_artifact.csv_file_path)), os.path.basename(self.data_ingestion_artifact.csv_file_path))

            if len(os.listdir(data_ingestion_artifact_dir))>1:
                profile=Profile(sections=[DataDriftProfileSection()])
                new_df=pd.read_csv(self.data_ingestion_artifact.csv_file_path)
                old_df=pd.read_csv(os.path.join(data_ingestion_artifact_dir, os.listdir(data_ingestion_artifact_dir)[-2], only_csv_data_dir))

                profile.calculate(new_df, old_df)

                report=json.loads(profile.json())

                os.makedirs(os.path.dirname(self.data_validation_config.report_file_path), exist_ok=True)

                with open(self.data_validation_config.report_file_path, "w") as report_file:
                    json.dump(report, report_file)

                return self.data_validation_config.report_file_path
            
            else:
                logging.info("No prior data history is available to generate Data Drift Report")
                return "No prior data history is available to generate Data Drift Report"

        except Exception as e:
            raise PremiumException(e,sys) from e
    
    def create_data_drift_report_page(self):
        try:
            data_ingestion_artifact_dir=os.path.dirname(os.path.dirname(os.path.dirname(self.data_ingestion_artifact.csv_file_path)))
            only_csv_data_dir=os.path.join(os.path.basename(os.path.dirname(self.data_ingestion_artifact.csv_file_path)), os.path.basename(self.data_ingestion_artifact.csv_file_path))

            if len(os.listdir(data_ingestion_artifact_dir))>1:
                dashboard=Dashboard(tabs=[DataDriftTab()])

                new_df=pd.read_csv(self.data_ingestion_artifact.csv_file_path)
                old_df=pd.read_csv(os.path.join(data_ingestion_artifact_dir, os.listdir(data_ingestion_artifact_dir)[-2], only_csv_data_dir))

                dashboard.calculate(new_df, old_df)

                os.makedirs(os.path.dirname(self.data_validation_config.report_page_file_path), exist_ok=True)

                dashboard.save(self.data_validation_config.report_page_file_path)

                return self.data_validation_config.report_page_file_path

            else:
                logging.info("No prior data history is available to generate Data Drift Report Page")
                return "No prior data history is available to generate Data Drift Report Page"

        except Exception as e:
            raise PremiumException(e,sys) from e

    def is_data_drift(self, report_file_path):
        try:
            dataset_data_drift_report= report_file_path
            try:
                f=open(dataset_data_drift_report)

                drift_report=json.load(f)

                return drift_report['data_drift']["data"]["metrics"]["dataset_drift"]
            
            except:
                logging.info("No prior data history is available to calculate data drift")
                return "No Data History Found"

        except Exception as e:
            raise PremiumException(e,sys) from e

    def initiate_data_validation(self):
        try:
            self.check_split()
            is_validated=self.validate_dataset_schema()
            report_file_path=self.generate_data_drift_report()
            report_page_file_path=self.create_data_drift_report_page()
            data_drift=self.is_data_drift(report_file_path)
            message=f"Data Performed Successfully. Data Drift found? {data_drift}"
            data_validation_artifact=DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path, report_file_path=report_file_path, report_page_file_path=report_page_file_path, is_validated=is_validated, message=message)
            logging.info(message)
            logging.info(f"{'='*20}Data Validation Stage Completed{'='*20}\n\n")

            return data_validation_artifact

        except Exception as e:
            raise PremiumException(e,sys) from e