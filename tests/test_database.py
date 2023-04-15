import sys
import os
import json
import pytest

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(parent_dir)

from db_server import sql_server


@pytest.fixture(scope='session')
def get_server():
    server = sql_server.Server()
    server.DATABASE = "test_database"
    yield server
    server.connection.close()


def delete_tables(get_server):
    get_server.create_connection()
    if get_server.DATABASE == "test_database":
        with get_server.connection.cursor() as cursor:
            cursor.execute("DROP TABLE cars;")
            cursor.execute("DROP TABLE links_cars;")
            cursor.execute("DROP TABLE land;")
            cursor.execute("DROP TABLE flats;")
            cursor.execute("DROP TABLE houses;")
            cursor.execute("DROP TABLE rs_links;")
            cursor.execute("DROP TABLE item_prices;")
            cursor.execute("DROP TABLE items;")
    get_server.connection.close()


def test_connecting_to_server(get_server):
    get_server.create_connection()
    with get_server.connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
        dbs = []
        for item in result:
            dbs.append(item[0])
    get_server.connection.close()
    assert "test_database" in dbs


def test_tables_in_db(get_server):
    get_server.database_setup()
    get_server.create_connection()
    with get_server.connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        tables = []
        for item in result:
            tables.append(item[0])
    test_tables = ["links_cars", "cars", "rs_links", "land", "flats", "houses", "items", "item_prices"]
    get_server.connection.close()
    assert all([table in tables for table in test_tables]) == True


# def test_filter_cars(get_server):
#     with open("test_data.json", 'r') as f:
#         data = json.load(f)
#     new_cars = data['cars']
#     get_server.create_connection()

    

def test_delete_tables(get_server):
    delete_tables(get_server)
    get_server.create_connection()
    with get_server.connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        tables = []
        for item in result:
            tables.append(item[0])
    get_server.connection.close()
    assert tables == []
