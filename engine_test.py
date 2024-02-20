def weather_to_db(text, engine):
    """
    Add weather data to the database
    """
    tz = pytz.timezone('Europe/Dublin')
    curr = datetime.datetime.now(tz=tz)

    weather = json.loads(text)
    vals = (
        float(weather['coord']['lon']),
        float(weather['coord']['lat']),
        int(weather['weather'][0]['id']),
        float(weather['main']['temp']),
        float(weather['main']['feels_like']),
        weather['weather'][0]['description'],
        float(weather['wind']['speed']),
        int(weather['main']['humidity'])
    )

    insert_stmt = """
    INSERT INTO dbikes.weather 
    (lon, lat, weather_id, temp, feels_like, weather_description, wind_speed, humidity, timestamp) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    with engine.connect() as connection:
        try:
            connection.execute(insert_stmt, vals)  # Using the updated vals tuple
        except Exception as e:
            print(f"Error executing SQL query: {e}")