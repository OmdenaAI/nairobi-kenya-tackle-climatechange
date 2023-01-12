import os, sys
from CO2.exception import CO2_Exception
from CO2.logger import logging
from datetime import datetime

FILE_NAME = 'OCO2_kenya.csv'
TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'


class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact",
                                             f"{datetime.now().strftime('%m-%d-%Y__%H;%M;%S')}")
        except Exception as e:
            raise CO2_Exception(e, sys)


class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.nc4_data_file_path = os.path.join(os.getcwd(), "nc4_data")
            self.power_plant_file_path = os.path.join(os.getcwd(), 'PowerPlant')
            self.population_file_path = os.path.join(os.getcwd(), 'Population')
            self.city_data_file_path = os.path.join(os.getcwd(), 'City_data')
            self.fire_data_file_path = os.path.join(os.getcwd(), 'fire_data')
            self.cement_data_file_path = os.path.join(os.getcwd(), 'Cement_data')
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise CO2_Exception(e, sys)

    def to_dict(self) -> dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CO2_Exception(e, sys)


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold: float = .1
        self.base_file_path = os.path.join('XCO2_kenya.csv')


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, 'data_transformation')
        self.transform_object_path = os.path.join(self.data_validation_dir, 'transformer')
        self.transform_train_path = os.path.join(self.data_validation_dir, 'transformed', 'train_file_name')
        self.transform_test_path = os.path.join(self.data_validation_dir, 'transformed', 'test_file_name')

    pass


class ModelTrainerConfig: ...


class ModelEvaluationConfig: ...


class ModelPusherConfig: ...
