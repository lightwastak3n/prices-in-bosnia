import os
import csv
from turso_server import Server


db_org = os.getenv("turso_db_org")
turso_token = os.getenv("turso_db_token")


# Delete tables
def delete_tables():
    conn = server.get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE cars;")
    cur.execute("DROP TABLE links_cars;")
    cur.execute("DROP TABLE land;")
    cur.execute("DROP TABLE flats;")
    cur.execute("DROP TABLE houses;")
    # cur.execute("DROP TABLE rs_prices;")
    cur.execute("DROP TABLE rs_links;")
    cur.execute("DROP TABLE item_prices;")
    cur.execute("DROP TABLE items;")
    cur.execute("DROP TABLE scraping_stats;")
    conn.commit()


def create_triggers():
    conn = server.get_connection()
    cur = conn.cursor()
    # create_land_trigger = "CREATE TRIGGER insert_new_lan AFTER INSERT ON land BEGIN UPDATE scraping_stats SET land = land + 1; END;"
    create_house_trigger = "CREATE TRIGGER insert_new_house AFTER INSERT ON houses BEGIN UPDATE scraping_stats SET houses = houses + 1; END;"
    # create_flats_trigger = "CREATE TRIGGER insert_new_flats AFTER INSERT ON flats BEGIN UPDATE scraping_stats SET flats = flats + 1; END;"
    # create_car_trigger = "CREATE TRIGGER insert_new_car AFTER INSERT ON cars BEGIN UPDATE scraping_stats SET cars = cars + 1; END;"
    # cur.execute(create_land_trigger)
    cur.execute(create_house_trigger)
    # cur.execute(create_flats_trigger)
    # cur.execute(create_car_trigger)
    conn.commit()


server = Server()


# Create tables
# server.execute_script("setup_sqlite.sql")
create_triggers()
# delete_tables()

# car_links = []
# with open("car_links.csv", "r") as f:
#     reader = csv.reader(f, delimiter=";")
#     for row in reader:
#         car_links.append(tuple(row))
# server.transfer_scraped_links(car_links, "car")

# rs_links = []
# with open("rs_links.csv", "r") as f:
#     reader = csv.reader(f, delimiter=";")
#     for row in reader:
#         rs_links.append(tuple(row))
# server.transfer_scraped_links(rs_links, "rs")
