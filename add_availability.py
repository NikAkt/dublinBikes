import json
import requests
import traceback
import datetime
import pymysql
from sqlalchemy import create_engine
import pytz

def availability_to_db(text,engine):
    """
    Add availability data to the database
    Should run every 5 minutes
    """
    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    print("availability_to_db")

    tz=pytz.timezone('Europe/Dublin')
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
                        last_update=datetime.datetime.fromtimestamp(int(station.get("last_update")) / 1000).astimezone(tz)
                    except TypeError:
                        print(station)
                        last_update = "0000-00-00 00:00:00"
                    vals = (int(station.get("number")), int(station.get("available_bikes")), int(station.get("available_bike_stands")), last_update, str(curr.strftime('%Y-%m-%d %H:%M:%S')))
                    cursor.execute("INSERT INTO `dbikes`.`availability` values(%s,%s,%s,%s,%s)", vals)
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                connection.rollback()
        connection.commit()
    return




def main():
    """
    SQL login info.
    """
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'

    """
    bike API info.
    """
    city_name = 'Dublin'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    website_bike = "https://api.jcdecaux.com/vls/v1/stations/"


    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, db), echo=True)

    try:
        r = requests.get(website_bike, params={"apiKey": bike_api_key, "contract": city_name})
        availability_to_db(r.text, engine)


    except AttributeError as event:
        print(traceback.format_exc() + "\n ERROR:The GET request has not been generated correctly")
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
    event_str = "Event \t" + str(event) + "\t captured at \t" + str(curr.strftime('%Y-%m-%d %H:%M:%S')) + "\n"
    file.write(event_str)
    file.close()

if __name__== "__main__":
    main()