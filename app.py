from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pymysql
import datetime
import json
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

if __name__ == "__main__":
    app.run(debug=True)
    