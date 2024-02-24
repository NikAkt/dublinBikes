import json
import os
import requests
from sqlalchemy import create_engine
import datetime
import time
import pytz
import pymysql

#not sure if this whole thing runs. We might have to remove it
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
    
def main():
    city_name = 'Dublin'
    weather_api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    lat='53.2734' #Dublin's latitude
    lon='-7.77832031' #Dublin's longitude
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    time = int(datetime.datetime.now().timestamp())

    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'


    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host,port,db), echo=True)

    r = requests.get(website, params={"apiKey": bike_api_key, "contract": city_name})
    # weather_data = fetch_weather_data(city_name, weather_api_key,lat,lon)
    # bike_data=fetch_bike_data(city_name, bike_api_key)
    
    # if weather_data:
    #     with open('weather_data.json', 'w') as outfileweather:
    #         json.dump(weather_data, outfileweather)
    # else:
    #     print("Failed to fetch weather data.")

    # if bike_data:
    #     with open('bike_data.json', 'w') as outfilebikes:
    #         json.dump(bike_data, outfilebikes)
    # else:
    #     print("Failed to fetch bike data.")

if __name__== "__main__":
    main()