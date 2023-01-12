from CO2.entity import artifact_entity, config_entity
from CO2.logger import logging
import sys
from typing import Optional
from CO2.exception import CO2_Exception
from scipy.stats import ks_2samp
import pandas as pd
from CO2 import utils


class DataValidation:

    def __init__(self,
                 data_validation_config: config_entity.DataValidationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'=' * 10} Data Validation Started {'=' * 10}")
            self.data_validation_config = data_validation_config
            self.validation_error = dict()
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CO2_Exception(e, sys)

    def drop_missing_values_column(self,
                                   df: pd.DataFrame,
                                   report_key_name: str) -> Optional[pd.DataFrame]:
        """
        This function will drop the column that will have missing value more than that of specified threshold
        :param report_key_name:
        :param df: Pandas dataframe
        :return: Pandas Dataframe if at least single column is available after dropping missing values columns else None
        """

        try:
            logging.info('=========> inside drop_missing_values_column')
            logging.info('')
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum() / df.shape[0]

            # selecting column names which contain null values more than a threshold
            logging.info('selecting column names which contain null values more than a threshold')
            drop_column_names = null_report[null_report > threshold].index
            df.drop(list(drop_column_names), axis=0, inplace=True)

            # Updating the dropped columns in the validation error dictionary
            logging.info('Updating the dropped columns in the validation error dictionary')
            self.validation_error[report_key_name] = drop_column_names

            # return none is no column left
            if len(df.columns == 0):
                return None
            else:
                return df

        except Exception as e:
            raise CO2_Exception(e, sys)

    def is_required_columns_exists(self,
                                   base_df: pd.DataFrame,
                                   curr_df: pd.DataFrame,
                                   report_key_name: str) -> bool:

        try:
            base_columns = base_df.columns
            curr_columns = curr_df.columns
            missing_columns = []
            for base_col in base_columns:
                if base_col not in curr_columns:
                    missing_columns.append(base_col)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = list(missing_columns)
                return False
            return True

        except Exception as e:
            raise CO2_Exception(e, sys)

    def data_drift(self,
                   base_df: pd.DataFrame,
                   curr_df: pd.DataFrame,
                   report_key_name: str) -> None:
        try:
            drift_report = dict()
            base_columns = base_df.columns
            curr_columns = curr_df.columns
            for base_column in base_columns:
                base_data, current_data = base_df[base_column], curr_df[base_column]
                same_distribution = ks_2samp(base_data, current_data)
                # Null Hypothesis: Both column has same data distribution
                if same_distribution.pvalue > .05:
                    # Null hypothesis is true
                    # same distribution
                    drift_report[base_column] = {
                        'p_values': float(same_distribution.pvalue),
                        'same_distribution': True
                    }
                else:
                    # different distribution
                    # alternate hypothesis is true
                    drift_report[base_column] = {
                        'p_values': float(same_distribution.pvalue),
                        'same_distribution': False
                    }
            self.validation_error[report_key_name] = drift_report
        except Exception as e:
            raise CO2_Exception(e, sys)

    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f'Reading base DataFrame')
            base_df = pd.read_csv(self.data_validation_config.base_file_path)

            logging.info(f'Read train dataframe')
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f'Reading the test dataframe')
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f'Checking for the existence of the all column in train dataset')
            train_df_column_status = self.is_required_columns_exists(base_df=base_df, curr_df=train_df,
                                                                     report_key_name='missing_columns_train_dataset')
            logging.info(f'Checking for the existence of the all column in test dataset')
            test_df_column_status = self.is_required_columns_exists(base_df=base_df, curr_df=test_df,
                                                                    report_key_name='missing_columns_test_dataset')

            if train_df_column_status is True:
                logging.info(f'Checking for the existence of the all column in train dataset')
                self.data_drift(base_df=base_df, curr_df=train_df, report_key_name='data_drift_within_train_dataset')
            if test_df_column_status is True:
                logging.info(f'Checking for the existence of the all column in train dataset')
                self.data_drift(base_df=base_df, curr_df=test_df, report_key_name='data_drift_within_test_dataset')

            # write the report
            utils.write_ymal_file(file_path=self.data_validation_config.report_file_path,
                                  data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(
                report_file_path=self.data_validation_config.report_file_path)
            return data_validation_artifact

        except Exception as e:
            raise CO2_Exception(e, sys)
