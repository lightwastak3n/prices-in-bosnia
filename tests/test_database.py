import sys
import pytest

sys.path.append('../')
from db_server import sql_server


@pytest.fixture(scope='session')
def db_connection():
    server = sql_server.Server()
    server.DATABASE = "test_database"
    server.create_connection()
    yield server
    server.close_connection()


def delete_tables(db_connection):
    if db_connection.DATABASE == "test_database":
        with db_connection.connection.cursor() as cursor:
            cursor.execute("DROP TABLE cars;")
            cursor.execute("DROP TABLE links_cars;")
            cursor.execute("DROP TABLE land;")
            cursor.execute("DROP TABLE flats;")
            cursor.execute("DROP TABLE houses;")
            cursor.execute("DROP TABLE rs_links;")


def test_connecting_to_server(db_connection):
    with db_connection.connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
        dbs = []
        for item in result:
            dbs.append(item[0])
    assert "test_database" in dbs


def test_tables_in_db(db_connection):
    db_connection.database_setup(close_on_finish=False)
    with db_connection.connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        tables = []
        for item in result:
            tables.append(item[0])
    test_tables = ["links_cars", "cars", "rs_links", "land", "flats", "houses"]
    assert all([table in tables for table in test_tables]) == True


def test_delete_tables(db_connection):
    delete_tables(db_connection)
    with db_connection.connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        tables = []
        for item in result:
            tables.append(item[0])
    assert tables == []

