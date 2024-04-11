import pymysql
from pymysql.cursors import DictCursor
import json

station_count = 0


def get_stations():
    """
    Get all stations
    render template to client
    """
    with open("config.json") as config_file:
        config = json.load(config_file)

    host = config["dburl"]
    user = config["dbuser"]
    password = config["dbpass"]
    db = config["db"]
    stations = []
    connection = pymysql.connect(
        host=host, user=user, password=password, db=db, cursorclass=DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            sql0 = "SELECT COUNT(*) FROM station;"
            cursor.execute(sql0)
            result = cursor.fetchone()
            count_list = list(result.values())
            station_count = int(count_list[0])
            print("Station Count: ", station_count)
            cursor.execute("SELECT * FROM station;")
            rows = cursor.fetchall()
            for row in rows:
                # print(row) #test print
                stations.append(dict(row))


if __name__ == "__main__":
    get_stations()
