import sys
import pytest

sys.path.append('../')
from db_server import sql_server


@pytest.fixture(scope='session')
def db_connection():
    server = sql_server.Server()
    server.DATABASE = "test_database"
    server.create_connection()
    yield server.connection
    server.close_connection()


def test_connecting_to_server(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
        dbs = []
        for item in result:
            dbs.append(item[0])
    assert "test_database" in dbs


def test_tables_in_db(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        tables = []
        for item in result:
            tables.append(item[0])
    test_tables = sorted(["links_cars", "cars", "rs_links", "land", "flats", "houses"])
    tables.sort()
    assert tables == test_tables

