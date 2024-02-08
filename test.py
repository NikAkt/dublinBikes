import requests
import json

def fetch_weather_data(city_name, weather_api_key):
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


city_name = 'Dublin'  # Replace with the city name you want to fetch data for
weather_api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'  # Replace with your OpenWeather API key
bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'  # Replace with your OpenWeather API key
time=1707388263 #used Thu Feb 08 2024 10:31:03 GMT+0000 as a placeholder timestamp. Go to https://www.unixtimestamp.com for more info. This uses UNIX timestamp
lat='53.2734' #Dublin's latitude
lon='-7.77832031' #Dublin's longitude

weather_data = fetch_weather_data(city_name, weather_api_key)
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