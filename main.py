import json
import os
import requests
from sqlalchemy import create_engine
import datetime
import time
import pytz
import pymysql

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
    
def stations_to_db(text,engine):
    #only needs to run once
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    print("stations_to_db")
    try:
        connection = pymysql.connect(host=host,user=user,password=password,db=db)
        # Execute a simple query to test connectivity
        with connection.cursor() as cursor:
            cursor.execute("SHOW VARIABLES;")
            for row in cursor:
                print(row)
    except Exception as e:
        print(f"Error connecting to the database: {e}")

        # Close the connection
        connection.close()

    stations=json.loads(text)
    print(type(stations),len(stations))
    for station in stations:
        print(station)
        vals=(station.get('address'),int(station.get('banking')),station.get('bike_stands'),int(station.get('bonus')),station.get('contract_name'),station.get('name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'))
        engine.execute("insert into station values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",vals)
    return


def get_db_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def main():
    city_name = 'Dublin'
    weather_api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    lat='53.2734' #Dublin's latitude
    lon='-7.77832031' #Dublin's longitude
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    time = int(datetime.datetime.now().timestamp())

    #only needs to run once
    db_url = 'mysql://admin:widzEh-kuwriz-0menki@se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com:3306/dbikes'
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'


    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host,port,db), echo=True)

    r = requests.get(website, params={"apiKey": bike_api_key, "contract": city_name})
    stations_to_db(r.text, engine)

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