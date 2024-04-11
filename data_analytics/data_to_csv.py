import pymysql
import csv
from contextlib import closing
import json

def connect_to_db():
    with open('config.json', 'r') as f:
        config = json.load(f)

    host = config['dburl']
    user = config['dbuser']
    password = config['dbpass']
    db = config['db']

    return pymysql.connect(host=host, user=user, password=password, db=db)

def data_to_csv(table_name, file_name, headers):
    with closing(connect_to_db()) as connection:
        with closing(connection.cursor()) as cursor:
            try:
                cursor.execute(f"SELECT * FROM {table_name}")
                with open(file_name, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    for row in cursor.fetchall():
                        writer.writerow(row)
                connection.commit()
            except pymysql.Error as e:
                print(f"Error executing SQL query: {e}")
                connection.rollback()

def availability_to_csv():
    headers = ['number', 'available_bikes', 'available_bike_stands', 'last_update', 'curr_time']
    data_to_csv('availability', 'availability.csv', headers)

def weather_to_csv():
    headers = ['lon', 'lat', 'id', 'temp', 'feels_like','weather_description','wind_speed','humidity','curr_time']
    data_to_csv('weather', 'weather.csv', headers)

if __name__ == '__main__':
    availability_to_csv()
    weather_to_csv()