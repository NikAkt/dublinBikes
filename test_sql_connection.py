import sqlalchemy

def test_db_connection():
    # Replace 'your_database_url' with your actual database URL
    db_url = 'mysql://admin:widzEh-kuwriz-0menki@se-database.cjm0yeew4eja.eu-north-1.rds.amazonaws.com:3306/dbikes'

    try:
        # Establish a connection to the database
        engine = sqlalchemy.create_engine(db_url)
        connection = engine.connect()

        # Execute a simple query to test connectivity
        result = connection.execute("SHOW VARIABLES;")

        # Print the results
        for row in result:
            print(row)

        print("Database connection successful.")

        # Close the connection
        connection.close()

    except Exception as e:
        print("Error connecting to the database:", e)

# Call the function to test the database connection
test_db_connection()
