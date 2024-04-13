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


def insert_car_links(get_server):
    server = get_server
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    cars_data = [[car, data["cars"][car], 1] for car in data["cars"]]
    server.add_car_links(cars_data)
    server.add_car_link("11111", "google.com", "0")


def test_car_link_in_db(get_server):
    insert_car_links(get_server)
    server = get_server
    not_there = server.item_in_db("links_cars", "1234567")
    there = server.item_in_db("links_cars", "11111")
    assert [not_there, there] == [False, True] 


def test_cars_in_db(get_server):
    server = get_server
    ids = ["51329772", "51856919", "51810247", "987654"]
    not_present = server.items_not_in_db("links_cars", ids)
    assert not_present == ["987654"]


def test_get_non_scraped_cars(get_server):
    server = get_server
    not_scraped = server.get_non_scraped_cars()
    assert not_scraped == [(11111, "google.com")]


def insert_single_car(get_server):
    server = get_server
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    server.insert_car_data(data["car1"])


def test_get_car_data(get_server):
    insert_single_car(get_server)
    server = get_server
    car_data = server.get_car_data(53421314)
    answer = []
    check_items = [17300, "Gradacac", "Karavan", "Dizel", "2023-02-19"]
    for item in check_items:
        answer.append(item in car_data)
    assert all(answer) == True

def insert_rs_data(get_server):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    server = get_server
    server.insert_rs_data("Zemljiste", data["land1"])
    server.insert_rs_data("Stan", data["flat1"])
    server.insert_rs_data("Kuca", data["house1"])


def insert_rs_links(get_server):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    rs_data = data["rs_links"]
    rs_data = [[rs, rs_data[rs][0], rs_data[rs][1], rs_data[rs][2]] for rs in rs_data]
    server = get_server
    server.add_rs_links(rs_data)
    server.add_rs_link(112233, "yahoo.com", "Kuca", "0")
    insert_rs_data(get_server)
    

def test_get_non_scraped_rs(get_server):
    server = get_server
    insert_rs_links(get_server)
    not_scraped = server.get_non_scraped_rs()
    answer = [
            (561091, 'https://www.olx.ba/artikal/561091/', 'Kuca'),
            (667413, 'https://olx.ba/artikal/667413/', 'Stan'),
            (668263, 'https://olx.ba/artikal/668263/', 'Zemljiste'),
            (112233, 'yahoo.com', 'Kuca')
            ]
    answer = sorted(answer, key=lambda x: x[0])
    not_scraped = sorted(not_scraped, key=lambda x: x[0])
    assert answer == not_scraped


def test_mark_as_scraped(get_server):
    server = get_server
    server.mark_as_scraped("rs_links", 112233)
    server.mark_as_scraped("rs_links", 667413)
    not_scraped = server.get_non_scraped_rs()
    answer = [
            (561091, 'https://www.olx.ba/artikal/561091/', 'Kuca'),
            (668263, 'https://olx.ba/artikal/668263/', 'Zemljiste'),
            ]
    answer = sorted(answer, key=lambda x: x[0])
    not_scraped = sorted(not_scraped, key=lambda x: x[0])
    assert answer == not_scraped


def test_get_land_data(get_server):
    server = get_server
    rs_data = server.get_rs_data("Zemljiste", 53070662)
    check_items = [1412, "Ilidza", "Asfalt"]
    answer = []
    for item in check_items:
        answer.append(item in rs_data)
    assert all(answer) == True


def test_get_flat_data(get_server):
    server = get_server
    rs_data = server.get_rs_data("Stan", 48894962)
    check_items = [190, "Ilidza", "Blazujski drum", "Novogradnja"]
    answer = []
    for item in check_items:
        answer.append(item in rs_data)
    assert all(answer) == True


def test_get_house_data(get_server):
    server = get_server
    rs_data = server.get_rs_data("Kuca", 51868032)
    check_items = [155000, "Laktasi", "Kuca sa dvoristem Laktasi", "Drva"]
    answer = []
    for item in check_items:
        answer.append(item in rs_data)
    assert all(answer) == True


def test_delete_tables(get_server):
    delete_tables(get_server)
    cursor = get_server.cur
    cursor.execute( "SELECT * FROM sqlite_master WHERE type='table';")
    result = cursor.fetchall()
    tables = []
    for item in result:
        tables.append(item[0])
    assert tables == []
