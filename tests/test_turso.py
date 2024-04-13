import sys
import os
import json
import pytest
from time import sleep

# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(parent_dir)

from db_server import turso_server


@pytest.fixture(scope='session')
def get_server():
    test_org = "testprices-light"
    test_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MTI5NjYyMzYsImlkIjoiMzVmMzU4ODUtOTdmYi00MTA5LTgxNzctYWQwYjczZDU0OGZlIn0.P1ZW_5OVXTwpfvgLpfqLojwsV3gRhLoONBPGkb0mUfgV5TfO7UpzR_Ah5lfjoo5Ydmxh44fB3iLAz413MvN5Dw"
    server = turso_server.Server(test_org, test_token)
    sleep(3)
    yield server


def create_tables(get_server):
    server = get_server
    with open('create_tables.sql', 'r') as file:
        script = file.read()
    server.conn.executescript(script)
    server.conn.commit()


def delete_tables(get_server):
    server = get_server
    server.cur.execute("DROP TABLE cars;")
    server.cur.execute("DROP TABLE links_cars;")
    server.cur.execute("DROP TABLE land;")
    server.cur.execute("DROP TABLE flats;")
    server.cur.execute("DROP TABLE houses;")
    server.cur.execute("DROP TABLE rs_links;")
    server.cur.execute("DROP TABLE item_prices;")
    server.cur.execute("DROP TABLE items;")
    server.conn.commit()


def test_tables_in_db(get_server):
    server = get_server
    create_tables(get_server)
    query = "SELECT * FROM sqlite_master WHERE type='table';"
    server.cur.execute(query)
    result = server.cur.fetchall()
    tables = []
    for item in result:
        tables.append(item[1])
    print(tables)
    test_tables = ["links_cars", "cars", "rs_links", "land", "flats", "houses", "items", "item_prices"]
    assert all([table in tables for table in test_tables]) == True


def insert_data(get_server):
    server = get_server
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    cars_data = [[car, data["cars"][car], 1] for car in data["cars"]]
    print(cars_data)
    server.add_car_links(cars_data)
    server.add_car_link(11111, "google.com", 0)

def test_car_in_db(get_server):
    insert_data(get_server)
    server = get_server
    not_there = server.item_in_db("links_cars", 1234567)
    there = server.item_in_db("links_cars", 11111)
    assert [not_there, there] == [False, True] 


def test_cars_in_db(get_server):
    server = get_server
    ids = [51329772, 51856919, 51810247, 987654]
    not_present = server.items_not_in_db("links_cars", ids)
    assert not_present == [987654]


def test_delete_tables(get_server):
    delete_tables(get_server)
    cursor = get_server.cur
    cursor.execute( "SELECT * FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    tables = []
    for item in result:
        tables.append(item[0])
    assert tables == []
