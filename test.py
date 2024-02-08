import requests

def fetch_weather_data(city_name, weather_api_key):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}")
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

weather_data = fetch_weather_data(city_name, weather_api_key)
bike_data=fetch_bike_data(city_name, bike_api_key)

if weather_data:
    # Handle the data
    print(weather_data)
else:
    # Handle any errors
    print("Failed to fetch weather data.")

if bike_data:
    # Handle the data
    print(bike_data)
else:
    # Handle any errors
    print("Failed to fetch weather data.")
