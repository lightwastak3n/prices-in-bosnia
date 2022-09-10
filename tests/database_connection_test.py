import mysql.connector
from mysql.connector import Error

try:
connection = mysql.connector.connect(
            host="159.89.19.69",
            port="5231",
            database="prices",
            user="scraper",
            password="jh4yXWPWV!nogywjy22i")
    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"Connected to MySQL server version {db_info}")
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print(f"You're connected to database {record}")
except Error as e:
    print("Error whie connecting to MySQL server.", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
