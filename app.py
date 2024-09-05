import mysql.connector
from mysql.connector import Error
import os

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'dbhostname'),
            database=os.getenv('DB_NAME', 'mydatabase'),
            user=os.getenv('DB_USER', 'myuser'),
            password=os.getenv('DB_PASSWORD', 'mypassword')
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            # You can execute queries here
            # Example:
            # cursor = connection.cursor()
            # cursor.execute("SELECT DATABASE();")
            # record = cursor.fetchone()
            # print("You're connected to:", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    connect_to_database()