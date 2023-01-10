import netCDF4
import pandas as pd
from CO2.config import kenya_lon_lat
from CO2.logger import logging
from CO2.exception import CO2_Exception
import yaml
import os, sys
import numpy as np
from math import radians, cos, sin, asin, sqrt
import math
from datetime import datetime


def convert_nc4_to_csv(complete_folder_path: str):
    """
    Description: This method will convert the cdf4 file format to the csv file format.
    Also, it will extract the data of Kenya.
    :param complete_folder_path: Path of directory containing nc4 file
    :return: pandas Data frame that combines all the data
    """
    try:
        logging.info('>>>>>>>>>>>>> inside the class Utils <<<<<<<<<<<')
        logging.info(f'Folder path is: {complete_folder_path}')
        list_of_files = os.listdir(complete_folder_path)
        df = pd.DataFrame()
        for file in list_of_files:
            logging.info(f'=======>Processing of File : {file} started')
            path = os.path.join(complete_folder_path, file)
            data0 = netCDF4.Dataset(path)
            latitude_values = list(data0.variables['lat'][:])
            longitude_values = list(data0.variables['lon'][:])
            logging.info('Latitude and longitude value extracted')

            XCO2_values = list(data0.variables['XCO2'][:])[0]
            try:
                XCO2PREC_values = list(data0.variables['XCO2PREC'][:])[0]
            except:
                XCO2PREC_values = np.NaN
            logging.info('CO2 values extracted')

            latitude_values_for_df = np.repeat(latitude_values, len(longitude_values))
            longitude_values_for_df = np.array(longitude_values * len(latitude_values))

            XCO2_values_for_df = XCO2_values.flatten()
            try:
                XCO2PREC_values_for_df = XCO2PREC_values.flatten()
            except:
                XCO2PREC_values_for_df = np.NaN
            logging.info('CO2_precision values extracted')

            format = '%Y-%m-%d'
            month_year = datetime.strptime(data0.RangeBeginningDate, format)
            XCO2_df = pd.DataFrame({'lat': latitude_values_for_df,
                                    'lon': longitude_values_for_df,
                                    'XCO2': XCO2_values_for_df,
                                    'XCO2PREC': XCO2PREC_values_for_df,
                                    'Month': month_year.month,
                                    'Year': month_year.year})
            logging.info('Data Frame Created')

            XCO2_df['DATE'] = pd.to_datetime(XCO2_df[['Year', 'Month']].assign(DAY=1))

            XCO2_df = XCO2_df[(XCO2_df['lat'] >= kenya_lon_lat[2]) & (XCO2_df['lat'] <= kenya_lon_lat[3])]
            XCO2_df = XCO2_df[(XCO2_df['lon'] >= kenya_lon_lat[0]) & (XCO2_df['lon'] <= kenya_lon_lat[1])].reset_index(
                drop=True)
            logging.info('Filtered the latitude and longitude for kenya')

            df = pd.concat([df, XCO2_df])
            df.reset_index(drop=True, inplace=True)
            logging.info(f'=======>Processing of File: {file} finished')

        df['lat'] = df['lat'].apply(lambda x: round(x, 2))
        cwd = os.getcwd()
        raw_data_path = os.path.join(cwd, 'Raw_data_to_csv_data')
        os.makedirs(raw_data_path, exist_ok=True)
        df.to_csv(rf'{raw_data_path}\XCO2_kenya.csv', index=False)
        logging.info('''XCO2_kenya.csv file created''')
        return df

    except Exception as e:
        raise CO2_Exception(e, sys)


def write_ymal_file(file_path, data: dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'w') as file_writer:
            yaml.dump(data, file_writer)

    except Exception as e:
        raise CO2_Exception(e, sys)


def create_bins(lower_bound, width, quantity):
    """ create_bins returns an equal-width (distance) partitioning.
        It returns an ascending list of tuples, representing the intervals.
        A tuple bins[i], i.e. (bins[i][0], bins[i][1])  with i > 0
        and i < quantity, satisfies the following conditions:
            (1) bins[i][0] + width == bins[i][1]
            (2) bins[i-1][0] + width == bins[i][0] and
                bins[i-1][1] + width == bins[i][1]
    """
    try:
        bins = []
        for low in range(lower_bound,
                         lower_bound + quantity * width + 1, width):
            bins.append((low, low + width))
        return bins
    except Exception as e:
        raise CO2_Exception(e, sys)


def single_pt_haversine(lat, lng, degrees=True):
    """
    'Single-point' Haversine: Calculates the great circle distance
    between a point on Earth and the (0, 0) lat-long coordinates
    """
    try:
        r = 6371  # Earth's radius (km). Have r = 3956 if you want miles

        # Convert decimal degrees to radians
        if degrees:
            lat, lng = map(radians, [lat, lng])

        # 'Single-point' Haversine formula
        a = sin(lat / 2) ** 2 + cos(lat) * sin(lng / 2) ** 2
        d = 2 * r * asin(sqrt(a))

        return d

    except Exception as e:
        raise CO2_Exception(e, sys)


def power_plant_dataset(complete_folder_path):
    try:
        files = os.listdir(complete_folder_path)
        power_plant_df = pd.DataFrame()
        for file in files:
            file_path = os.path.join(complete_folder_path, file)
            a = pd.read_csv(file_path)
            power_plant_df = pd.concat([power_plant_df, a])
            power_plant_df.reset_index(drop=True, inplace=True)

        power_plant_df['harvesine_distance'] = [single_pt_haversine(latitude, longitude) for latitude, longitude in
                                                zip(power_plant_df['latitude'], power_plant_df['longitude'])]
        power_plant_df['lat_long'] = list(zip(power_plant_df['latitude'], power_plant_df['longitude']))

        width = 5
        no_bins = int(
            round((power_plant_df['harvesine_distance'].max() - power_plant_df['harvesine_distance'].min()) / width, 0))

        lower_bound = math.floor(power_plant_df['harvesine_distance'].min())
        bins = create_bins(lower_bound=lower_bound,
                           width=width,
                           quantity=no_bins)
        bins2 = pd.IntervalIndex.from_tuples(bins, closed="left")
        power_plant_df['bins'] = pd.cut(power_plant_df['harvesine_distance'], bins=bins2)
        # Bin
        step_long = 0.625
        to_bin_long = lambda x: np.floor(x / step_long) * step_long
        power_plant_df["lonBin"] = to_bin_long(power_plant_df['longitude'])

        step_lat = 0.5
        to_bin_lat = lambda x: np.floor(x / step_lat) * step_lat
        power_plant_df["latBin"] = to_bin_lat(power_plant_df['latitude'])

        kenya_bins = power_plant_df.groupby(
            ["latBin", "lonBin", 'primary_fuel', 'commissioning_year']).sum(numeric_only=True).reset_index()
        kenya_bins.drop(labels=['latitude', 'longitude', 'harvesine_distance'], axis=1, inplace=True)
        kenya_bins.rename(columns={'latBin': 'latitude', 'lonBin': 'longitude'}, inplace=True)

        return kenya_bins

    except Exception as e:
        raise CO2_Exception(e, sys)


def population_dataset(complete_folder_path: str) -> pd.DataFrame:
    try:
        files = os.listdir(complete_folder_path)
        population_df = pd.DataFrame()
        for file in files:
            path = os.path.join(complete_folder_path, file)
            a = pd.read_csv(path)
            population_df = pd.concat([population_df, a])
            population_df.reset_index(drop=True, inplace=True)
        return population_df

    except Exception as e:
        raise CO2_Exception(e, sys)


def city_dataset(complete_folder_path: str) -> pd.DataFrame:
    try:
        files = os.listdir(complete_folder_path)
        city_df = pd.DataFrame()
        for file in files:
            path = os.path.join(complete_folder_path, file)
            a = pd.read_csv(path)
            city_df = pd.concat([city_df, a])
            city_df.reset_index(drop=True, inplace=True)
        city_df = city_df.loc[:, ['city_ascii', 'lat', 'lng', 'capital', 'population']]
        city_df = city_df.rename(columns={'population': 'city_pop_2022',
                                          'lat': 'latitude',
                                          'lng': 'longitude'})

        # Bin
        step_long = 0.625
        to_bin_long = lambda x: np.floor(x / step_long) * step_long
        city_df["lonBin"] = to_bin_long(city_df.longitude)

        step_lat = 0.5
        to_bin_lat = lambda x: np.floor(x / step_lat) * step_lat
        city_df["latBin"] = to_bin_lat(city_df.latitude)

        city_df.drop(labels=['latitude', 'longitude'], axis=1, inplace=True)
        city_df.rename(columns={'latBin': 'latitude', 'lonBin': 'longitude'}, inplace=True)

        return city_df

    except Exception as e:
        raise CO2_Exception(e, sys)


def fire_dataset(complete_folder_path: str) -> pd.DataFrame:
    try:
        a = pd.DataFrame()
        files = os.listdir(complete_folder_path)
        for file in files:
            path = os.path.join(complete_folder_path, file)
            kenya_fire = pd.read_csv(path)

            # Bin
            step_long = 0.625
            to_bin_long = lambda x: np.floor(x / step_long) * step_long
            kenya_fire["lonBin"] = to_bin_long(kenya_fire.longitude)

            step_lat = 0.5
            to_bin_lat = lambda x: np.floor(x / step_lat) * step_lat
            kenya_fire["latBin"] = to_bin_lat(kenya_fire.latitude)

            kenya_fire['acq_date'] = pd.to_datetime(kenya_fire['acq_date'])
            kenya_fire['year'] = kenya_fire['acq_date'].dt.year
            kenya_fire['month'] = kenya_fire['acq_date'].dt.month

            kenya_fire.drop(
                columns=['latitude', 'longitude', 'acq_time', 'satellite', 'instrument', 'confidence', 'version',
                         'type',
                         'daynight'], inplace=True)

            kenya_fire_data = kenya_fire.groupby(["latBin", "lonBin", 'year', 'month']).mean(numeric_only=True).round(
                2).reset_index()
            kenya_fire_data.rename(columns={'latBin': 'latitude', 'lonBin': 'longitude'}, inplace=True)

            a = pd.concat([a, kenya_fire_data])

        return a
    except Exception as e:
        raise CO2_Exception(e, sys)


def cement_dataset(complete_folder_path: str) -> pd.DataFrame:
    try:
        cement_df = pd.DataFrame()
        files = os.listdir(complete_folder_path)
        for file in files:
            path = os.path.join(complete_folder_path, file)
            a = pd.read_csv(path)
            step_long = 0.625
            to_bin_long = lambda x: np.floor(x / step_long) * step_long
            a["lonBin"] = to_bin_long(a.longitude)

            step_lat = 0.5
            to_bin_lat = lambda x: np.floor(x / step_lat) * step_lat
            a["latBin"] = to_bin_lat(a.latitude)
            a.drop(columns=['latitude', 'longitude', 'accuracy', 'capacity'], inplace=True)
            a.rename(columns={'latBin': 'latitude', 'lonBin': 'longitude'}, inplace=True)
            cement_df = pd.concat([cement_df, a])

        return cement_df
    except Exception as e:
        raise CO2_Exception(e, sys)
