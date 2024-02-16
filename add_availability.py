import json
import os
import requests
import traceback
import datetime
import time
import pymysql
from sqlalchemy import create_engine
import pytz

def availability_to_db(text,engine):
    """
    Add availability data to the database
    This needs to be run every 5 minutes
    """
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    print("availability_to_db")

def main():
    city_name = 'Dublin'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'

if __name__== "__main__":
    main()