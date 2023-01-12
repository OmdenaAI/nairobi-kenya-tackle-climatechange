# Omdena Nairobi, Kenya Chapter: Using AI/ML to tackle Climate Change

This project aims to study the value of satellite observations of the column CO2 concentrations to estimate CO2 anthropogenic emissions within five years of the Orbiting Carbon Observatory-2 (OCO-2) retrievals over and around Kenya. Our focus here is on the direct observation of carbon dioxide (CO2) emissions from space and on the quantification of CO2 emissions from this observation independently. 


We use NASA’s OCO2 and OCO3 Satellite data and publicly available data on critical CO2 emitting sectors e.g. power plants, steel mills , cement plants, atmospheric “spillover” from agricultural and forest fires, traffic emissions, demographic and economic variables etc to build an AI model that predicts the contribution from each sector. 

This CO2 emissions model could be used to track progress for large and small cities, subregions or project areas within Kenya which can be used to support decarbonization efforts



<!-- 
## Contribution Guidelines
- Have a Look at the [project structure](#project-structure) and [folder overview](#folder-overview) below to understand where to store/upload your contribution
- If you're creating a task, Go to the task folder and create a new folder with the below naming convention and add a README.md with task details and goals to help other contributors understand
    - Task Folder Naming Convention : _task-n-taskname.(n is the task number)_  ex: task-1-data-analysis, task-2-model-deployment etc.
    - Create a README.md with a table containing information table about all contributions for the task.
- If you're contributing for a task, please make sure to store in relavant location and update the README.md information table with your contribution details.
- Make sure your File names(jupyter notebooks, python files, data sheet file names etc) has proper naming to help others in easily identifing them.
- Please restrict yourself from creating unnessesary folders other than in 'tasks' folder (as above mentioned naming convention) to avoid confusion. 

-->

## Project Structure

    ├── LICENSE
    ├── README.md          <- The top-level README for developers/collaborators using this project.
    ├── original           <- Original Source Code of the challenge hosted by omdena. Can be used as a reference code for the current project goal.
    │ 
    │
    ├── reports            <- Folder containing the final reports/results of this project
    │   └── README.md      <- Details about final reports and analysis
    │ 
    │   
    ├── src                <- Source code folder for this project
        │
        ├── data           <- Datasets used and collected for this project
        │   
        ├── docs           <- Folder for Task documentations, Meeting Presentations and task Workflow Documents and Diagrams.
        │
        ├── references     <- Data dictionaries, manuals, and all other explanatory references used 
        │
        ├── tasks          <- Master folder for all individual task folders
        │
        ├── visualizations <- Code and Visualization dashboards generated for the project
        │
        └── results        <- Folder to store Final analysis and modelling results and code.
--------

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

<!--

## Folder Overview

- Original          - Folder Containing old/completed Omdena challenge code.
- Reports           - Folder containing Final Reports of this project
- Data              - Folder containing all the data collected and used for this project 
- Docs              - Folder containing Task documentations, Meeting Presentations and task Workflow Documents and Diagrams.
- References        - Folder that stores any referenced code/research papers and other useful documents used for this project
- Tasks             - Master folder for all tasks
- Visualization     - Folder that stores dashboards, analysis and visualization reports
- Results           - Folder that stores final analysis and modelling results for the project.

  - All Task Folder names should follow specific naming convention
  - All Task folder names should be in chronologial order (from 1 to n)
  - All Task folders should have a README.md file with task Details and task goals along with an info table containing all code/notebook files with their links and information
  - Update the [task-table](./src/tasks/README.md#task-table) whenever a task is created and explain the purpose and goals of the task to others.
---> 
