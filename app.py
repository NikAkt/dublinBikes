from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymysql
import json
from pymysql.cursors import DictCursor
import joblib
import requests
from datetime import datetime, timedelta
from dateutil.parser import parse

station_count=0

load_dotenv()
app = Flask("__name__", template_folder='templates', static_folder='static')
CORS(app)

models_availability={}
models_bike_stands={}
models_availability_directory="models_availability"
models_bike_stands_directory="models_bike_stands"

for filename in os.listdir(models_availability_directory):
    if filename.endswith('.joblib'):
        # Get the station number from the filename
        station_number = int(filename.split('model_availability')[1].split('.')[0])
        # Load the model and store it in the dictionary
        models_availability[station_number] = joblib.load(os.path.join(models_availability_directory, filename))

for filename in os.listdir(models_bike_stands_directory):
    if filename.endswith('.joblib'):
        # Get the station number from the filename
        station_number = int(filename.split('model_bike_stand')[1].split('.')[0])
        # Load the model and store it in the dictionary
        models_bike_stands[station_number] = joblib.load(os.path.join(models_bike_stands_directory, filename))

def get_weather_forecast():
    """
    Accesses the openweathermap API to get the weather forecast for the next 5 days.
    """
    website_weather = "https://api.openweathermap.org/data/2.5/forecast?"
    lat='53.2734' #Dublin's latitude
    lon='-7.77832031' #Dublin's longitude
    weather_api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'
    weather = requests.get(website_weather, params={"lat": lat, "lon": lon,"appid":weather_api_key })
    forecast = weather.json()

    with open('weather_forecast.json','w') as f:
        json.dump(forecast, f)
    return

def process_weather_forecast(weather_json, dateTime):
    """
    Processes the weather forecast JSON to extract the relevant weather data for the given timestamp.
    """
    print(weather_json)
    print("=====================================")
    for item in weather_json['list']:
        if item['dt_txt'] == dateTime:
            temp_k = item['main']['temp']
            feels_like_k = item['main']['feels_like']
            wind_speed = item['wind']['speed']
            humidity = item['main']['humidity']

            temp_c = temp_k - 273.15
            feels_like_c = feels_like_k - 273.15

            return temp_c, feels_like_c, wind_speed, humidity
    return None, None, None, None

@app.route("/")
def index():
    GMAP_KEY = os.getenv("GMAP_KEY")
    return render_template("index.html", GMAP_KEY=GMAP_KEY)


@app.route("/stations")
def get_stations():
    """
    Get all stations
    render template to client
    """
    global station_count

    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    stations=[]
    connection = pymysql.connect(host=host, user=user, password=password, db=db,cursorclass=DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql0 = "SELECT COUNT(*) FROM station;"
            cursor.execute(sql0)
            result = cursor.fetchone()
            count_list = list(result.values())
            station_count = int(count_list[0])

            cursor.execute("SELECT * FROM station;")
            rows = cursor.fetchall()
            for row in rows:
                stations.append(dict(row))
            return jsonify(station=stations)
        
@app.route("/availability")
def get_availability():
    """
    Get availability
    render template to client
    """
    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    availability=[]
    connection = pymysql.connect(host=host, user=user, password=password, db=db,cursorclass=DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM dbikes.availability ORDER BY curr_time DESC LIMIT {station_count};")
            rows = cursor.fetchall()
            row_count=0
            for row in rows:
                availability.append(dict(row))
                row_count+=1
            return jsonify(availability=availability)
        
@app.route("/availability_by_hour/<int:station_id>")
def get_availability_by_hour(station_id):
    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    availability = []

    connection = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=DictCursor)
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT 
                           DATE_FORMAT(hours.hour_start, '%H:00:00') AS hour_start,
                           AVG(availability.available_bikes) AS avg_bikes_available
                FROM
                           (SELECT 
                           DATE_ADD(DATE_FORMAT(NOW(), '%Y-%m-%d'), INTERVAL hour HOUR) AS hour_start
                FROM
        (SELECT 0 AS hour UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
        UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7
        UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11
        UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15
        UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19
        UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23) AS hours
        ) AS hours
                LEFT JOIN
                     dbikes.availability AS availability ON hours.hour_start = DATE_FORMAT(availability.curr_time, '%Y-%m-%d %H:00:00')
                WHERE 
                           availability.number = 3
                GROUP BY 
                           hour_start
                ORDER BY 
                           hour_start;
                           """)
            rows = cursor.fetchall()
            
            for row in rows:
                availability.append(dict(row))

    return jsonify(availability=availability)

@app.route('/predict', methods=['POST'])
def predict():
    model_inputs = request.get_json()
    get_weather_forecast()
    # proc_weather_data=process_weather_forecast(weather, data['timestamp'])
    
    # hour = (timestamp.hour // 3) * 3
    # timestamp = timestamp.replace(hour=hour, minute=0, second=0)
    # timestamp = int(timestamp.timestamp())

    temp_datetime = (model_inputs['timestamp'])

    round_times = [0, 3, 6, 9, 12, 15, 18, 21]
    hour = temp_datetime.hour
    next_hour = min((t for t in round_times if t >= hour), default=0)
    if next_hour == 0:
        temp_datetime += timedelta(days=1)

    # Replace the hour of temp_datetime with next_hour
    temp_datetime = temp_datetime.replace(hour=next_hour, minute=0, second=0, microsecond=0)

    with open('processed_weather_data.json', 'r') as f:
        weather = json.load(f)

    temp_c, feels_like_c, wind_speed, humidity = process_weather_forecast(weather, temp_datetime)

    print(temp_c, feels_like_c, wind_speed, humidity)

    station_number_start = int(data['station_number_start'])
    station_number_end = int(data['station_number_end'])

    year=data['year']
    month=data['month']
    day=data['day']
    hour=data['hour']
    minute=data['minute']
    day_of_week=data['day_of_week']

    # temp=data['temp']
    # feels_like=data['feels_like']
    # wind_speed=data['wind_speed']
    # humidity=data['humidity']

    # Get model for this station

    model_av = models_availability[station_number_start]
    model_stand=models_bike_stands[station_number_end]
    # print(model_av)
    # print(model_stand)

    input_data = [[temp_c,feels_like_c, wind_speed,humidity,year, month, day, hour, minute, day_of_week]]
    input_data = [[year, month, day, hour, minute, day_of_week]]

    prediction_availability = model_av.predict(input_data)
    prediction_bike_stands = model_stand.predict(input_data)

    return {
        'prediction_bike_availability_start': prediction_availability.tolist(),

        'prediction_bike_stands_end': prediction_bike_stands.tolist()
    }
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
    