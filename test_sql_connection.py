import sqlalchemy
import pymysql

def test_db_connection():
    # Replace 'your_database_url' with your actual database URL
    db_url = 'mysql://admin:widzEh-kuwriz-0menki@se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com:3306/dbikes'
    host='se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com'
    user='admin'
    password='widzEh-kuwriz-0menki'
    db='dbikes'

    try:
        connection = pymysql.connect(host=host,user=user,password=password,db=db)
        # Execute a simple query to test connectivity
        with connection.cursor() as cursor:
            cursor.execute("SHOW VARIABLES;")
            for row in cursor:
                print(row)
    except Exception as e:
        print(f"Error connecting to the database: {e}")

        # Close the connection
        connection.close()

# Call the function to test the database connection
test_db_connection()
