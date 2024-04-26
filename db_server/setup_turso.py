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


server = Server()

# Create tables
server.execute_script("setup_sqlite.sql")
server.execute_script("sqlite_triggers.sql")
# delete_tables()
# server.conn.sync()


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
