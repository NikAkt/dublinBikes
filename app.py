from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor

station_count=0

load_dotenv()
app = Flask("__name__", template_folder='templates', static_folder='static')


@app.route("/")
def index():
    GMAP_KEY = os.getenv("GMAP_KEY")
    return render_template("index.html", GMAP_KEY=GMAP_KEY)


@app.route("/stations")
def get_stations():
    """
    Get all stations
    render template to client
    """
    global station_count

    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    stations=[]
    connection = pymysql.connect(host=host, user=user, password=password, db=db,cursorclass=DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql0 = "SELECT COUNT(*) FROM station;"
            cursor.execute(sql0)
            result = cursor.fetchone()
            count_list = list(result.values())
            station_count = int(count_list[0])
            print("==============================================")
            print("Station Count: ",station_count)
            print("==============================================")

            cursor.execute("SELECT * FROM station;")
            rows = cursor.fetchall()
            for row in rows:
                # print(row) #test print
                stations.append(dict(row))
            return jsonify(station=stations)
        
@app.route("/availability")
def get_availability():
    """
    Get availability
    render template to client
    """
    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    availability=[]
    connection = pymysql.connect(host=host, user=user, password=password, db=db,cursorclass=DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM dbikes.availability ORDER BY curr_time DESC LIMIT {station_count};")
            print(station_count)
            rows = cursor.fetchall()
            row_count=0
            for row in rows:
                print(row) #test print
                availability.append(dict(row))
                row_count+=1
            print("==============================================")
            print("Row Count: ",row_count)
            print("==============================================")

            return jsonify(availability=availability)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
    