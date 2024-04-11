import json
import requests
import traceback
import datetime
import pymysql
from sqlalchemy import create_engine
import pytz


def weather_to_db(text, engine):
    """
    Add weather data to the database
    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    host = config["dburl"]
    user = config["dbuser"]
    password = config["dbpass"]
    db = config["db"]
    print("weather_to_db")

    weather = json.loads(text)

    # set up timezone
    tz = pytz.timezone("Europe/Dublin")
    curr = datetime.datetime.now(tz=tz)

    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    with connection:
        with connection.cursor() as cursor:
            try:
                vals = (
                    float(weather["coord"]["lon"]),
                    float(weather["coord"]["lat"]),
                    int(weather["weather"][0]["id"]),
                    float(weather["main"]["temp"]),
                    float(weather["main"]["feels_like"]),
                    weather["weather"][0]["description"],
                    float(weather["wind"]["speed"]),
                    int(weather["main"]["humidity"]),
                    str(curr.strftime("%Y-%m-%d %H:%M:%S")),
                )
                cursor.execute(
                    "INSERT INTO `dbikes`.`weather` values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    vals,
                )
            except Exception as e:
                print(f"Error executing SQL query: {e}")
                connection.rollback()
        connection.commit()
    return


def main():
    """
    SQL login info.
    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    host = config["dburl"]
    user = config["dbuser"]
    password = config["dbpass"]
    db = config["db"]
    port = config["dbport"]

    """
    weather API info.
    """
    website_weather = "https://api.openweathermap.org/data/2.5/weather/"
    lat = "53.2734"  # Dublin's latitude
    lon = "-7.77832031"  # Dublin's longitude
    with open("config.json") as config_file:
        config = json.load(config_file)
    weather_api_key = config["weather_api_key"]

    engine = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, db),
        echo=True,
    )

    try:
        r_weather = requests.get(
            website_weather, params={"lat": lat, "lon": lon, "appid": weather_api_key}
        )
        weather_to_db(r_weather.text, engine)

    except AttributeError as event:
        print(
            traceback.format_exc()
            + "\n ERROR:The GET request has not been generated correctly"
        )
        event_log(event)
        print("got to here")
    except Exception as event:
        print(traceback.format_exc() + "\n ERROR: An unknown error has occured")
        event_log(event)


def event_log(event):
    """
    Event log for errors etc.
    """
    curr = datetime.datetime.utcnow()

    try:
        file = open("event_log.txt", "w")
    except FileExistsError:
        file = open("event_log.txt", "a")

    # Corrected the string formatting and write operation
    event_str = (
        "Event \t"
        + str(event)
        + "\t captured at \t"
        + str(curr.strftime("%Y-%m-%d %H:%M:%S"))
        + "\n"
    )
    file.write(event_str)
    file.close()


if __name__ == "__main__":
    main()
