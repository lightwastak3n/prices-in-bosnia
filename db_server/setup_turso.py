import os
from turso_server import Server


db_org = os.getenv("turso_db_org")
turso_token = os.getenv("turso_db_token")

# Delete tables
def delete_tables():
    server.cur.execute("DROP TABLE cars;")
    server.cur.execute("DROP TABLE links_cars;")
    server.cur.execute("DROP TABLE land;")
    server.cur.execute("DROP TABLE flats;")
    server.cur.execute("DROP TABLE houses;")
    server.cur.execute("DROP TABLE rs_links;")
    server.cur.execute("DROP TABLE item_prices;")
    server.cur.execute("DROP TABLE items;")
    server.cur.execute("DROP TABLE scraping_stats;")
    server.conn.commit()

server = Server(db_org, turso_token)

# Create tables
# server.execute_script("create_tables.sql")
# delete_tables()

