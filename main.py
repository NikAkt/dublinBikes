import json
import os
import requests
from sqlalchemy import create_engine
import datetime
import time
import pytz


def fetch_weather_data(city_name, weather_api_key,lat,lon):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}")
        response.raise_for_status()  # Raise an error for bad status codes
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def fetch_bike_data(city_name, bike_api_key):
    try:
        response = requests.get(f"https://api.jcdecaux.com/vls/v1/stations?contract={city_name}&apiKey={bike_api_key}")
        response.raise_for_status()  # Raise an error for bad status codes
        bike_data = response.json()
        return bike_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
def fetch_stations(website,bike_api_key,city_name,engine):
    #only needs to run once
    #Read in stations to json object
    r = requests.get(website, params={"apiKey": bike_api_key, "contract": city_name})
    stations = json.loads(r.text)

    # Loop through stations, adding each one to the database
    for station in stations:
        values = (station.get("address"),int(station.get("banking")), int(station.get("bike_stands")),station.get("contract_name"), station.get("name"), int.station.get("number"), station.get("position").get("lat"), station.get("position").get("lng"),station.get("status"))
        engine.execute("INSERT INTO `dbikes`.`station` values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
    return


def get_db_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config



# Now you can use these variables in your database connection code

def main():
    city_name = 'Dublin'
    weather_api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    time=1707388263 #used Thu Feb 08 2024 10:31:03 GMT+0000 as a placeholder timestamp. Go to https://www.unixtimestamp.com for more info. This uses UNIX timestamp
    lat='53.2734' #Dublin's latitude
    lon='-7.77832031' #Dublin's longitude
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    
    config = get_db_config()
    dbuser = config["dbuser"]
    dbpass = config["dbpass"]
    dburl = config["dburl"]
    dbport = config["dbport"]

    engine = create_engine("mysql+pymysql://{0}:{1}@{2}".format(dbuser, dbpass, dburl), echo=True)


    stations=fetch_stations(website,bike_api_key,city_name,engine)
    weather_data = fetch_weather_data(city_name, weather_api_key,lat,lon)
    bike_data=fetch_bike_data(city_name, bike_api_key)
    if weather_data:
        with open('weather_data.json', 'w') as outfileweather:
            json.dump(weather_data, outfileweather)
    else:
        print("Failed to fetch weather data.")

    if bike_data:
        with open('bike_data.json', 'w') as outfilebikes:
            json.dump(bike_data, outfilebikes)
    else:
        print("Failed to fetch bike data.")