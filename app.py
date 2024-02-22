from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pymysql
import datetime

load_dotenv()
app = Flask("__name__", template_folder='templates', static_folder='static')


@app.route("/")
def index():
    GMAP_KEY = os.getenv("GMAP_KEY")
    return render_template("index.html", GMAP_KEY=GMAP_KEY)


if __name__ == "__main__":
    app.run(debug=True)
    
@app.route("/stations")
def get_stations():
    """
    Get all stations
    render template to client
    """
    global last_updated_availability_time, last_updated_availability_data, first_run
    if (((last_updated_availability_time - datetime.datetime.now()).total_seconds() < -900) or first_run):
        first_run = False
        sql_get_availability = """select db_a.number, position_lat, position_lng, name, address, available_bikes, available_bike_stands, max(db_a.last_update) as last_update
    FROM dublin_bikes.station db_s
    INNER JOIN dublin_bikes.availability db_a ON
    db_s.number = db_a.number
    GROUP BY number
    """  # create select statement for stations table
        print("INSIDE 1")
        rows = sql_query(sql_get_availability)  # execute select statement
        
        last_updated_availability_data = []
        for row in rows:
            last_updated_availability_data.append(dict(row))  # inset dict of data into list
            print(row)
        last_updated_availability_time = datetime.datetime.now()
    return jsonify(station=last_updated_availability_data)  # return json string of data

def sql_query(query):
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'

    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    try:
        with connection.cursor() as cursor:
            # Execute the query
            cursor.execute(query)
            # Fetch all rows from the result
            rows = cursor.fetchall()
    finally:
        connection.close()

    return rows

query = """
    SELECT dbikes.number, position_lat, position_lng, name, address, available_bikes, available_bike_stands, MAX(db_a.last_update) AS last_update
    FROM dublin_bikes.station db_s
    INNER JOIN dublin_bikes.availability db_a ON db_s.number = db_a.number
    GROUP BY db_a.number;
"""

result = sql_query(query)
print(result)