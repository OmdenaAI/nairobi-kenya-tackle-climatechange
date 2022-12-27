# Guide to extract CO2 the data and merge the same with the other relevant datasets

## 1. Data Download
### 1.1 XCO2 data 
Download the XCO2 data from the NASA website.
Click on this [link](https://disc.gsfc.nasa.gov/). 
In search box type Level2 (L2) data OCO2_Lite_V11r

Download the data in nc4 format and move the same to folder "/nc4_data" in the folder. 

### 1.2 City data 
[World Cities Database](https://simplemaps.com/data/world-cities) is proud to offer a simple, accurate and up-to-date database of the world's cities and towns under a creative commons license. Commercial use is allowed and is built from the ground up using authoritative sources such as the NGIA, US Geological Survey, US Census Bureau, and NASA.

The database is:
- Up-to-date: It was last refreshed in March 2022.
- Comprehensive: Over 4 million unique cities and towns from every country in the world.
- Accurate: Cleaned and aggregated from official sources. 
- Includes latitude and longitude coordinates.

A single CSV file is downloaded and then saved into the "/City_data" folder.

### 1.3 Cement data 

[Cement dataset](https://www.cgfi.ac.uk/spatial-finance-initiative/geoasset-project/geoasset-databases/) was downloaded. 
Relevant data was then extracted and then saved to the "/Cement_data" directory.

### 1.4 Fire data 

World fire dataset can be found [Fire Information for Resource Management System](https://firms.modaps.eosdis.nasa.gov/country/).

Download the csv file year wise and then save the same to the "/fire_data" directory. 

### 1.5 Population data 

[WorldPop Hub](https://hub.worldpop.org/geodata/listing?id=75) is the collection of world population year wise

The dataset is available to download in Geotiff and ASCII XYZ format at a resolution of 30 arc (approximately 1km at the equator). 
The projection is Geographic Coordinate System, WGS84. 
The units are number of people per pixel. 
The mapping approach is Random Forest-based dasymetric redistribution.

Dataset has been downloaded from the above website year wise and combined into the single csv file. 
Then saved into the "/Population" folder  
### 1.6 Power Plant data

The [Global Power Plant Database](https://datasets.wri.org/dataset/globalpowerplantdatabase) is a comprehensive, open source database of power plants around the world. 
It centralizes power plant data to make it easier to navigate, compare and draw insights for one’s own analysis. 
The database covers approximately 35,000 power plants from 167 countries and includes thermal plants (e.g. coal, gas, oil, nuclear, biomass, waste, geothermal) and renewables (e.g. hydro, wind, solar). 
Each power plant is geolocated and entries contain information on plant capacity, generation, ownership, and fuel type.

Dataset is downloaded and the saved onto the "/PowerPlant" folder.

# 2. Dependent Libraries
All the dependent libraries can be found in the "/requirements.txt" file. 
The same can be installed via code ```pip install -r requirements.txt```

# 3. Final Data
Run "/main.py" file and the final data will be extracted. 
Data is processed, filtered and merged. 
Final dataset is saved in the path "artifact/date__time/data_ingestion/feature_store"

# 4. Logs
Every instance is logged. Logs can be found in "/logs"

