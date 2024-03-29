from collections import namedtuple

DataIngestionArtifact = namedtuple(
    "DataIngestionArtifact",
    ["csv_file_path", "train_file_path", "test_file_path", "is_ingested", "message"],
)

DataValidationArtifact = namedtuple(
    "DataValidationArtifact",
    [
        "schema_file_path",
        "report_file_path",
        "report_page_file_path",
        "is_validated",
        "message",
    ],
)

DataTransformationArtifact = namedtuple(
    "DataTransformationArtifact",
    [
        "transformed_train_file_path",
        "transformed_test_file_path",
        "preprocessed_object_file_path",
        "is_transformed",
        "message",
    ],
)

ModelTrainerArtifact = namedtuple(
    "ModelTrainerArtifact",
    [
        "trained_model_file_path",
        "train_rmse",
        "test_rmse",
        "train_accuracy",
        "test_accuracy",
        "model_accuracy",
        "is_trained",
        "message",
    ],
)

ModelEvaluationArtifact = namedtuple(
    "ModelEvaluationArtifact", ["evaluated_model_path", "is_model_accepted"]
)

ModelPusherArtifact = namedtuple(
    "ModelPusherArtifact", ["export_model_file_path", "is_model_pusher"]
)
