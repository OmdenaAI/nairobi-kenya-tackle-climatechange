import pandas as pd
import numpy as np
from CO2 import utils
from CO2.entity import config_entity
from CO2.entity import artifact_entity
from CO2.exception import CO2_Exception
import sys, os
from CO2.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            logging.info('================== Data Ingestion Class =========================')
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CO2_Exception(e, sys)

    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            # Exporting the data as pandas DataFrame
            logging.info('================== Initiate Data Ingestion =========================')

            logging.info('Converting the all the CDF4 data to a single csv file')
            # Converting the all the CDF4 data to a single csv file
            logging.info(f'Folder path is {self.data_ingestion_config.nc4_data_file_path}')
            df_co2: pd.DataFrame = utils.convert_nc4_to_csv(complete_folder_path=self.data_ingestion_config.nc4_data_file_path)
            logging.info('XCO2 Data Frame created')

            # Extracting the power plant data
            logging.info('Extracting Power plant dataset')
            df_power_plant: pd.DataFrame = utils.power_plant_dataset(complete_folder_path=self.data_ingestion_config.power_plant_file_path)
            logging.info('Power plant dataframe created')
            logging.info('Master DataFrame created')
            df = pd.merge(df_co2, df_power_plant, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])
            logging.info('XCO2 dataset and power plant dataset merged')
            df.drop(columns=['latitude', 'longitude'], inplace=True)

            for i in df[df['Year'] < df['commissioning_year']].index:
                df.at[i, 'primary_fuel'] = np.NaN
                df.at[i, 'commissioning_year'] = np.NaN
                df.at[i, 'capacity_mw'] = np.NaN
            logging.info('Power plant data extracted and merged')

            # extracting the cement data
            logging.info('Extracting cement dataset')
            df_cement: pd.DataFrame = utils.cement_dataset(complete_folder_path=self.data_ingestion_config.cement_data_file_path)
            logging.info('Cement data frame created')
            df = pd.merge(df,df_cement, how='outer', left_on=['lat','lon'], right_on= ['latitude','longitude'])
            logging.info('Cement dataset merged with the master dataset')
            df.drop(columns=['latitude', 'longitude'], inplace=True)
            logging.info('Cement dataset extraction completed')

            # extracting the city data
            logging.info('Extracting the city dataset')
            df_city: pd.DataFrame = utils.city_dataset(complete_folder_path=self.data_ingestion_config.city_data_file_path)
            logging.info('City data frame created')
            df = pd.merge(df,df_city, how='outer', left_on=['lat','lon'], right_on=['latitude','longitude'])
            logging.info('City dataset merged with the master dataset')
            df.drop(columns=['latitude', 'longitude', 'capital'], inplace=True)
            logging.info('City dataset extraction completed')

            # Extracting the fire data
            logging.info('Extracting the Fire dataset')
            df_fire: pd.DataFrame = utils.fire_dataset(complete_folder_path=self.data_ingestion_config.fire_data_file_path)
            logging.info('Fire data frame created')
            df = pd.merge(df, df_fire, how='left',
                          left_on=['lat', 'lon', 'Year', 'Month'],
                          right_on=['latitude', 'longitude', 'year', 'month'])
            logging.info('Fire dataset merged with the master dataset')
            df.drop(columns=['latitude', 'longitude', 'year', 'month'], inplace=True)
            logging.info('Fire dataset extraction completed')

            # extracting Population data
            logging.info('Extracting the Population dataset')
            df_population: pd.DataFrame = utils.population_dataset(complete_folder_path= self.data_ingestion_config.population_file_path)
            logging.info('Population data frame created')
            df = pd.merge(df, df_population, how='left',
                          left_on=['lat', 'lon', 'Year'],
                          right_on=['latitude', 'longitude', 'year'])
            logging.info('Population dataset merged with the master dataset')
            df.drop(columns=['latitude', 'longitude', 'year', 'city', 'state'], inplace=True)
            logging.info('Population dataset extraction completed')

            # Create a feature store folder
            logging.info('Create a feature store folder')
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info(f'Created folder {feature_store_dir}')

            # Save data to the feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index = False)
            logging.info(f'Data compiled and stored to {self.data_ingestion_config.feature_store_file_path} ')

            # prepare the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                                                    feature_store_file_path=self.data_ingestion_config.feature_store_file_path)
            logging.info('============= Data Ingestion completed =========================')

            return data_ingestion_artifact

        except Exception as e:
            logging.info(e)
            raise CO2_Exception(e, sys)


