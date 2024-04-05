import json
import os
import requests
from datetime import datetime

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

    with open('weather_data.json','w') as f:
        json.dump(forecast, f)
    return

def process_weather_json():
    # Open the weather_data.json file
    with open('weather_data.json', 'r') as f:
        weather_data = json.load(f)

    # Iterate over the items in the weather_data dictionary
    for item in weather_data['list']:
        # Convert the timestamp to a readable date and time
        timestamp = datetime.fromtimestamp(item['dt'])
        item['dt'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # Write the modified weather_data to a new file
    with open('processed_weather_data.json', 'w') as f:
        json.dump(weather_data, f)

get_weather_forecast()
# process_weather_json()