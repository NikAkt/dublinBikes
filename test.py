import requests

def fetch_weather_data(city_name, api_key):
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}")
        response.raise_for_status()  # Raise an error for bad status codes
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Example usage
city_name = 'Dublin'  # Replace with the city name you want to fetch data for
api_key = '43aeecf5b252d71ca98d7f4dd8aaee24'  # Replace with your OpenWeather API key

weather_data = fetch_weather_data(city_name, api_key)
if weather_data:
    # Handle the data
    print(weather_data)
else:
    # Handle any errors
    print("Failed to fetch weather data.")
