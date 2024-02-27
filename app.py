from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import pymysql
from pymysql.cursors import DictCursor


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
    host = 'se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user = 'admin'
    password = 'widzEh-kuwriz-0menki'
    db = 'dbikes'
    stations=[]
    connection = pymysql.connect(host=host, user=user, password=password, db=db,cursorclass=DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM station;")
            rows = cursor.fetchall()
            for row in rows:
                print(row) #test print
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
            cursor.execute("""SELECT * FROM dbikes.availability ORDER BY curr_time DESC LIMIT 114;""")
            rows = cursor.fetchall()
            for row in rows:
                print(row) #test print
                availability.append(dict(row))
            return jsonify(availability=availability)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
    