import pymongo
import pandas as pd
import json
import os
from dataclasses import dataclass


# provide the mongo DB local host url to connect with python

@dataclass
class EnvironmentVariable:
    mongo_db_url: str = os.getenv('Mongo_db_url')


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)


@dataclass
class KenyaDetail:
    kenya_lat_min = -5
    kenya_lat_max = 5
    kenya_lon_min = 33.5
    kenya_lon_max = 42


kenya = KenyaDetail()
kenya_lon_lat = [kenya.kenya_lon_min, kenya.kenya_lon_max,kenya.kenya_lat_min, kenya.kenya_lat_max]