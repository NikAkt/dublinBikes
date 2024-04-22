# dublinBikes

This application provides real-time information about Dublin Bikes stations, including the availability of bikes and stands, and weather forecasts. It uses a K-Nearest Neighbors (KNN) machine learning model to provide predictions for bike availability per station.

## Structure

The application is structured as follows:

- `app.py`: The main Flask application file.
- `add_availability.py`, `add_stations.py`, `add_weather.py`: Scripts to add data to the database.
- `get_weather_forecast.py`: Script to get weather forecast data.
- `data_analytics/`: Directory containing data analytics notebooks and scripts.
- `models_availability/`, `models_bike_stands/`: Directories containing machine learning models for predicting bike availability and bike stand availability.
- `static/`, `templates/`: Directories containing static files and HTML templates for the Flask application.

## Setup

1. Clone the repository.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run `python add_stations.py`, `python add_availability.py`, and `python add_weather.py` to populate the database.
4. Run `python app.py` to start the Flask application.

## Usage

- Visit `http://localhost:8080` to view the application.
- Use the Journey Planner to plan your bike journey.
- Click on a station to view real-time availability and prediction for the next hour.

## Contributing

Contributions are welcome. Please open an issue to discuss your idea or submit a pull request.
