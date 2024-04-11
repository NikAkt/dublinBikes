import requests
import json
import pymysql


def stations_to_db(text):
    """
    Add stations to the database
    This needs to be run only once
    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    host = config["dburl"]
    user = config["dbuser"]
    password = config["dbpass"]
    db = config["db"]

    print("stations_to_db")

    try:
        stations = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    with connection:
        with connection.cursor() as cursor:
            try:
                # sql = 'TRUNCATE TABLE station;'
                # cursor.execute(sql)
                # connection.commit()
                # sql='ALTER TABLE station ADD PRIMARY KEY (number);'
                # cursor.execute(sql)
                # connection.commit()
                ## commented out to avoid overwriting the database with primary keys
                for station in stations:
                    print(station)
                    vals = (
                        station.get("address"),
                        int(station.get("banking")),
                        station.get("bike_stands"),
                        station.get("contract_name"),
                        station.get("name"),
                        station.get("number"),
                        station.get("position").get("lat"),
                        station.get("position").get("lng"),
                        station.get("status"),
                        int(station.get("bonus")),
                    )
                    cursor.execute(
                        "insert into station values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        vals,
                    )
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                connection.rollback()
        connection.commit()


def main():
    with open("config.json") as config_file:
        config = json.load(config_file)

    city_name = "Dublin"
    bike_api_key = config["bike_api_key"]
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    r = requests.get(website, params={"apiKey": bike_api_key, "contract": city_name})
    if r.status_code == 200:
        try:
            stations_to_db(r.text)
        except Exception as e:
            print(f"Error adding stations to the database: {e}")
    else:
        print(f"Error retrieving data from API. Status code: {r.status_code}")


if __name__ == "__main__":
    main()
