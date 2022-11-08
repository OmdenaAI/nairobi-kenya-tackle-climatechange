import netCDF4
import pandas as pd
import numpy as np
from datetime import datetime
import os
import traceback

cwd = os.getcwd()
files = os.listdir(f'{cwd}/Data/OCO2/Raw_data')

final_df = pd.DataFrame()

for file in files:
    data0 = netCDF4.Dataset(f'{cwd}/Data/OCO2/Raw_data/{file}')
    latitude_values = list(data0.variables['lat'][:])
    longitude_values = list(data0.variables['lon'][:])

    XCO2_values = list(data0.variables['XCO2'][:])[0]
    try:
        XCO2PREC_values = list(data0.variables['XCO2PREC'][:])[0]
    except:
        pass

    latitude_values_for_df = np.repeat(latitude_values, len(longitude_values))
    longitude_values_for_df = np.array(longitude_values * len(latitude_values))

    XCO2_values_for_df = XCO2_values.flatten()
    try:
        XCO2PREC_values_for_df = XCO2PREC_values.flatten()
    except:
        XCO2PREC_values_for_df = np.NaN

    date_format = '%Y-%m-%d'
    month_year = datetime.strptime(data0.RangeBeginningDate, date_format)

    XCO2_df = pd.DataFrame({'lat': latitude_values_for_df,
                            'lon': longitude_values_for_df,
                            'XCO2 (mol CO2/mol dry)': XCO2_values_for_df,
                            'XCO2PREC (mol CO2/mol dry)': XCO2PREC_values_for_df,
                            'Month': month_year.month,
                            'Year': month_year.year})

    XCO2_df = XCO2_df[(XCO2_df['lat'] >= -5) & (XCO2_df['lat'] <= 5)]
    XCO2_df = XCO2_df[(XCO2_df['lon'] >= 33.5) & (XCO2_df['lon'] <= 42 )].reset_index(drop=True)
    final_df = pd.concat([final_df,XCO2_df])

final_df['DATE'] = pd.to_datetime(final_df[['Year', 'Month']].assign(DAY=1))
final_df.to_csv(f'{cwd}/Data/OCO2/Final_data/oco2_GEOS_L3_final.csv', index = False)

