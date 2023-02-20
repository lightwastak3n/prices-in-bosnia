import mysql.connector
import json

with open("config.json", 'r') as cnf:
    config = json.load(cnf)
    HOST = config['host']
    PORT = config['port']
    DATABASE = config['database']
    USER = config['user']
    PASSWORD = config['password']


def get_car_data_dict(car_id):
    connection = mysql.connector.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD)

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM cars where id={car_id};")
        columns = [column[0] for column in cursor.description]
        result = cursor.fetchone()
        result = dict(zip(columns, result))

    connection.close()

    for name, val in result.items():
        print(f"{name}: {val}")
