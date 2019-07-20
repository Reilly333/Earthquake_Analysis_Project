import json
import requests
from datetime import datetime
from datetime import timedelta
from pandas import DataFrame
from sqlalchemy import create_engine
"""
CREATE DATABASE earthquake_project2
   WITH
   OWNER = postgres
   ENCODING = 'UTF8'
   CONNECTION LIMIT = -1;"""

"""
CREATE TABLE earthquake_project2.earthquake_project2
(
   mag numeric(2, 2) NOT NULL,
   lon numeric(4, 4) NOT NULL,
   lat numeric(4, 4) NOT NULL,
   "time" timestamp without time zone NOT NULL
)
WITH (
   OIDS = FALSE
);

ALTER TABLE earthquatke_project2.earthquake_project2
   OWNER to postgres;
"""

connection_string = "postgres://postgres:12345@localhost:5432/earthquake_project2"
engine = create_engine(f'postgresql://{connection_string}')

def get_last_100_year_data():
   #results = [['lat','lon','mag','time']]
   results = []
   for year in range(1919, 2019):
       url = "https://earthquake.usgs.gov/fdsnws/event/1/" \
             "query?format=geojson&starttime={}-01-01&endtime={}-12-31&minmagnitude=3".format(year, year)
       try:
           response = requests.get(url)
       except requests.ConnectionError or requests.HTTPError:
           print('Error while contacting {}'.format(url))
           continue
       try:
           features = response.json()['features']
       except json.decoder.JSONDecodeError:
           continue

       for feature in features:
           lat, lon, _ = feature['geometry']['coordinates']
           magnitude = feature['properties']['mag']
           epoch_time_milli = float(feature['properties']['time'])
           if epoch_time_milli < 0:
               # Hack to handle negative EPOCH times on shitty windows implementation of GCC
               seconds_since = timedelta(seconds=abs(epoch_time_milli/1000))
               datetime_object = datetime(1970, 1, 1) - seconds_since
           else:
               datetime_object = datetime.fromtimestamp(epoch_time_milli/1000)
           print([lat, lon, magnitude, str(datetime_object)])
           results.append([lat, lon, magnitude, str(datetime_object)])

   df = DataFrame(results)
   df.columns=["lat","lon","mag","time"]
   print(results)
   print(df)
   return df




def insert_df(df):
   df.to_sql(name = 'earthquake', con =connection_string, if_exists='append', index=False)

df = get_last_100_year_data()

insert_df(df)