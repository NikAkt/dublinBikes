import json
import requests
import traceback
import datetime
import pymysql
import pytz


def availability_to_db(text):
    """
    Add availability data to the database
    Should run every 5 minutes
    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    host = config["dburl"]
    user = config["dbuser"]
    password = config["dbpass"]
    db = config["db"]
    print("availability_to_db")

    tz = pytz.timezone("Europe/Dublin")
    stations = json.loads(text)
    curr = datetime.datetime.now(tz=tz)
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    with connection:
        with connection.cursor() as cursor:
            try:
                # sql='ALTER TABLE availability DROP PRIMARY KEY, ADD PRIMARY KEY (`curr_time`, `number`);'
                # cursor.execute(sql)
                # connection.commit()
                # cursor.execute("ALTER TABLE availability ADD COLUMN curr_time VARCHAR(255);")
                # connection.commit()
                # commented out to avoid overwriting the database with primary keys
                for station in stations:
                    try:
                        last_update = datetime.datetime.fromtimestamp(
                            int(station.get("last_update")) / 1000
                        ).astimezone(tz)
                    except TypeError:
                        print(station)
                        last_update = "0000-00-00 00:00:00"
                    vals = (
                        int(station.get("number")),
                        int(station.get("available_bikes")),
                        int(station.get("available_bike_stands")),
                        last_update,
                        str(curr.strftime("%Y-%m-%d %H:%M:%S")),
                    )
                    cursor.execute(
                        "INSERT INTO `dbikes`.`availability` values(%s,%s,%s,%s,%s)",
                        vals,
                    )
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                connection.rollback()
        connection.commit()
    return


def main():
    """
    bike API info.
    """
    city_name = "Dublin"
    with open("config.json") as config_file:
        config = json.load(config_file)

    bike_api_key = config["bike_api_key"]
    website_bike = "https://api.jcdecaux.com/vls/v1/stations/"

    try:
        r = requests.get(
            website_bike, params={"apiKey": bike_api_key, "contract": city_name}
        )
        availability_to_db(r.text)
    except Exception as event:
        print(traceback.format_exc() + "\n ERROR: An error has occured")
        event_log(event)


def event_log(event):
    curr = datetime.datetime.utcnow()
    event_str = (
        "Event \t"
        + str(event)
        + "\t captured at \t"
        + str(curr.strftime("%Y-%m-%d %H:%M:%S"))
        + "\n"
    )
    with open("event_log.txt", "a") as file:
        file.write(event_str)


if __name__ == "__main__":
    main()
