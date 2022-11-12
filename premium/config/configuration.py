from premium.entity.config_entity import *
from premium.util.util import read_yaml_file
from premium.constant import *
from premium.exception import PremiumException
from premium.logger import logging
import os, sys

class Configuration:

    def __init__(self,
        config_file_path=CONFIG_FILE_PATH,
        current_timestamp=CURRENT_TIMESTAMP,
        )->None:
        self.config_info=read_yaml_file(file_path=config_file_path)
        self.training_pipeline_config=self.get_training_pipeline_config()
        self.timestamp=current_timestamp

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(artifact_dir, DATA_INGESTION_ARTIFACT_DIR, self.timestamp)

            data_ingestion_config=self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url=data_ingestion_config[DATA_INGESTION_DOWNLOAD_URL_KEY]
            csv_download_dir=os.path.join(data_ingestion_artifact_dir, data_ingestion_config[DATA_INGESTION_CSV_DOWNLOAD_DIR_KEY])
            ingested_dir=os.path.join(data_ingestion_artifact_dir,data_ingestion_config[DATA_INGESTION_DIR_NAME_KEY])
            ingested_train_dir=os.path.join(ingested_dir,data_ingestion_config[DATA_INGESTION_TRAIN_DIR_KEY])
            ingested_test_dir=os.path.join(ingested_dir,data_ingestion_config[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config=DataIngestionConfig(dataset_download_url=dataset_download_url, csv_download_dir=csv_download_dir, ingested_train_dir=ingested_train_dir, ingested_test_dir=ingested_test_dir)
            logging.info("Data Ingestion Config fetched: {x}".format(x=data_ingestion_config))
            return data_ingestion_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir, DATA_VALIDATION_ARTIFACT_DIR_NAME, self.timestamp)
            data_validation_config=self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path=os.path.join(ROOT_DIR, data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY], data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])
            report_file_path=os.path.join(data_validation_artifact_dir, data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY])
            report_page_file_path=os.path.join(data_validation_artifact_dir, data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config=DataValidationConfig(schema_file_path=schema_file_path, report_file_path=report_file_path, report_page_file_path=report_page_file_path)

            logging.info("Data Validation Config fetched: {x}".format(x=data_validation_config))
            return data_validation_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_transformation_artifact_dir=os.path.join(artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR_NAME, self.timestamp)

            data_transformation_config=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_train_dir=os.path.join(data_transformation_artifact_dir, data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR], data_transformation_config[DATA_TRANSFORMATION_TRAIN_DIR])
            transformed_test_dir=os.path.join(data_transformation_artifact_dir, data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR], data_transformation_config[DATA_TRANSFORMATION_TEST_DIR])

            preprocessed_object_file_path=os.path.join(data_transformation_artifact_dir, data_transformation_config[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY], data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])

            data_transformation_config=DataTransformationConfig(transformed_train_dir=transformed_train_dir, transformed_test_dir=transformed_test_dir, preprocessed_object_file_path=preprocessed_object_file_path)

            logging.info("Data Transformation configuration fetched: {x}".format(x=data_transformation_config))

            return data_transformation_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            artifact_dir=self.get_training_pipeline_config.artifact_dir
            model_trainer_config=self.config_info[MODEL_TRAINER_CONFIG_KEY]
            model_trainer_artifact_dir=os.path.join(artifact_dir, MODEL_TRAINER_ARTIFACT_DIR_NAME, self.timestamp)

            trained_model_file_path=os.path.join(model_trainer_artifact_dir, model_trainer_config[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY], model_trainer_config[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY])
            base_accuracy=model_trainer_config[MODEL_TRAINER_BASE_ACCURACY_KEY]
            model_config_file_path=os.path.join(ROOT_DIR, model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY], model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            model_trainer_config=ModelTrainerConfig(trained_model_file_path=trained_model_file_path, base_accuracy=base_accuracy, model_config_file_path=model_config_file_path)
            logging.info("Model Trainer Configuration fetched: {x}".format(x=model_trainer_config))

            return model_trainer_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            model_evaluation_config=self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            model_evaluation_artifact_dir=os.path.join(artifact_dir, MODEL_EVALUATION_ARTIFACT_DIR_NAME, self.timestamp)

            model_evaluation_file_path=os.path.join(model_evaluation_artifact_dir, model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])

            model_evaluation_config=ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path, timestamp=self.timestamp)
            logging.info("Model Evaluation Configuration fetched {x}".format(x=model_evaluation_config))

            return model_evaluation_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            time_stamp=f"{datetime.now().strftime('%Y%m%d %H%M%S')}"
            model_pusher_config=self.config_info[MODEL_PUSHER_CONFIG_KEY]

            export_dir_path=os.path.join(ROOT_DIR, model_pusher_config[MODEL_PUSHER_MODEL_EXPORT_KEY], time_stamp)
            
            model_pusher_config=ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info("Model Pusher Configuration fetched {x}".format(x=model_pusher_config))

            return model_pusher_config

        except Exception as e:
            raise PremiumException(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f'Training pipeline config: {training_pipeline_config}\n')
            return training_pipeline_config
        except Exception as e:
            raise PremiumException(e,sys) from e