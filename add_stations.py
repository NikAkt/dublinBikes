import requests
import json
import pymysql
from sqlalchemy import create_engine

def stations_to_db(text,engine):
    """
    Read in the static data of each stations to the database
    This needs to be run only once
    """
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    print("stations_to_db")

    stations = json.loads(text)
    connection = pymysql.connect(host=host,user=user,password=password,db=db)
    with connection:
        with connection.cursor() as cursor:
            sql='TRUNCATE TABLE station;'
            cursor.execute(sql)
            connection.commit()
            # sql='ALTER TABLE station ADD PRIMARY KEY (number);'
            # cursor.execute(sql)
            # connection.commit()
            # commented out to avoid overwriting the database with primary keys
            for station in stations:
                    print(station)
                    vals=(station.get('address'),int(station.get('banking')),station.get('bike_stands'),station.get('contract_name'),station.get('name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'),int(station.get('bonus')))
                    cursor.execute("insert into station values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",vals)
        connection.commit()

def main():
    city_name = 'Dublin'
    bike_api_key = '626c8de20316723c1526eed9a83479c9dd13f945'
    website = "https://api.jcdecaux.com/vls/v1/stations/"
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'
    port='3306'
    r = requests.get(website, params={"apiKey": bike_api_key, "contract": city_name})
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host,port,db), echo=True)
    stations_to_db(r.text, engine)

if __name__== "__main__":
    main()
