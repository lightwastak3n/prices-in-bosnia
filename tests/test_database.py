import sys

sys.path.append('../')
from db_server import sql_server

def connect_to_database():
    server = sql_server.Server()
    return server

def test_create_db():
    server = connect_to_database()
    server.create_connection()
    server.create_database("test_database")

    with server.connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES;")
        result = cursor.fetchall()
        dbs = []
        for item in result:
            dbs.append(item[0])
    with server.connection.cursor() as cursor:
        cursor.execute("DROP DATABASE test_database;")

    server.close_connection()
    assert "test_database" in dbs


