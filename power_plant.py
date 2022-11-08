import os

import pandas as pd
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt
import traceback

cwd = os.getcwd()
power_plant_df = pd.read_csv(f'{cwd}/Data/global_power_plant_database.csv')
XCO2_df = pd.read_csv(f'{cwd}/Data/OCO2/Final_data/oco2_GEOS_L3_final.csv')


def single_pt_haversine(lat, lng, degrees=True):
    """
    'Single-point' Haversine: Calculates the great circle distance
    between a point on Earth and the (0, 0) lat-long coordinates
    """
    r = 6371  # Earth's radius (km). Have r = 3956 if you want miles

    # Convert decimal degrees to radians
    if degrees:
        lat, lng = map(radians, [lat, lng])

    # 'Single-point' Haversine formula
    a = sin(lat / 2) ** 2 + cos(lat) * sin(lng / 2) ** 2
    d = 2 * r * asin(sqrt(a))

    return d


power_plant_df['harvesine_distance'] = [single_pt_haversine(latitude, longitude) for latitude, longitude in
                                        zip(power_plant_df['latitude'], power_plant_df['longitude'])]
power_plant_df['lat_long'] = list(zip(power_plant_df['latitude'], power_plant_df['longitude']))


def create_bins(lower_bound, width, quantity):
    """ create_bins returns an equal-width (distance) partitioning.
        It returns an ascending list of tuples, representing the intervals.
        A tuple bins[i], i.e. (bins[i][0], bins[i][1])  with i > 0
        and i < quantity, satisfies the following conditions:
            (1) bins[i][0] + width == bins[i][1]
            (2) bins[i-1][0] + width == bins[i][0] and
                bins[i-1][1] + width == bins[i][1]
    """

    bins = []
    for low in range(lower_bound,
                     lower_bound + quantity * width + 1, width):
        bins.append((low, low + width))
    return bins


# Bin by 5km Harvestine distance
width = 5
no_bins = int(
    round((power_plant_df['harvesine_distance'].max() - power_plant_df['harvesine_distance'].min()) / width, 0))

math.ceil(power_plant_df['harvesine_distance'].max()), math.floor(power_plant_df['harvesine_distance'].min())

lower_bound = math.floor(power_plant_df['harvesine_distance'].min())

bins = create_bins(lower_bound=lower_bound,
                   width=width,
                   quantity=no_bins)

harvestine_distance = power_plant_df['harvesine_distance']
bins2 = pd.IntervalIndex.from_tuples(bins, closed="left")
categorical_object = pd.cut(harvestine_distance, bins2)
power_plant_df['bins'] = pd.cut(power_plant_df['harvesine_distance'], bins=bins2)
power_plant = power_plant_df[['capacity_mw', 'primary_fuel', 'commissioning_year', 'bins']]
## Bin
step_long = 0.625
to_bin_long = lambda x: np.floor(x / step_long) * step_long
power_plant_df["lonBin"] = to_bin_long(power_plant_df['longitude'])

step_lat = 0.5
to_bin_lat = lambda x: np.floor(x / step_lat) * step_lat
power_plant_df["latBin"] = to_bin_lat(power_plant_df['latitude'])

kenya_bins = power_plant_df.groupby(["latBin", "lonBin", 'primary_fuel', 'commissioning_year']).sum().reset_index()
kenya_bins.drop(labels=['latitude', 'longitude', 'harvesine_distance'], axis=1, inplace=True)
kenya_bins.rename(columns={'latBin': 'latitude', 'lonBin': 'longitude'}, inplace=True)

a = pd.merge(XCO2_df, kenya_bins, how='outer', left_on=['lat', 'lon'], right_on=['latitude', 'longitude'])
for i in a[a['Year'] < a['commissioning_year']].index:
    a.at[i, 'primary_fuel' ] = np.NaN
    a.at[i, 'commissioning_year'] = np.NaN
    a.at[i, 'capacity_mw'] = np.NaN

a.to_csv(f'{cwd}/Data/OCO2/Final_data/oco2_power_plant.csv', index = False)

