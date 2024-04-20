from turso_server import Server


db_org = "learning-light"
turso_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MTMwMzU0NzksImlkIjoiNTM3Zjc1ODAtZGVmZC00NWM5LWJkZTktZjU3ODhjYTE2MTNhIn0.fZj0ByssmX7o_LP5AXomuM_3WCec3owuW2HLiwb2nHXo1KCJ1kOzU4XlMDzbDEQHdFuGS800_lU_KnANy3f1CQ"

server = Server(db_org, turso_token)


# Create table
def create_table():
    items_table = "CREATE TABLE items (id INT PRIMARY KEY, name TEXT, type TEXT, unit TEXT, store TEXT)"
    server.cur.execute(items_table)
    server.conn.commit()
    item_prices_table = "CREATE TABLE item_prices (id INT PRIMARY KEY, item_id INT NOT NULL, price REAL NOT NULL, date DATE NOT NULL, FOREIGN KEY(item_id) REFERENCES items(id));"
    server.cur.execute(item_prices_table)
    server.conn.commit()


def delete_tables():
    server.cur.execute("DROP TABLE items;")
    server.cur.execute("DROP TABLE item_prices;")


def show_data():
    server.cur.execute("SELECT * FROM items;")
    result = server.cur.fetchall()
    print(result)


def insert_batch():
    data = [
        ("Apple", 1.50, "2024-04-13"),
        ("Banana", 0.75, "2024-04-13"),
        ("Orange", 1.00, "2024-04-12"),
        ("Grapes", 2.50, "2024-04-12"),
        ("Watermelon", 5.00, "2024-04-11"),
    ]
    query = "INSERT INTO items (name, price, date) VALUES(?, ?, ?)"
    server.cur.executemany(query, data)
    show_data()


items_data = [
    {"name": "banana", "price": 3.19, "unit": "kg", "type": "fruits and vegetables"},
    {
        "name": "luk crveni",
        "price": 1.79,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {"name": "mrkva", "price": 1.89, "unit": "kg", "type": "fruits and vegetables"},
    {
        "name": "krompir mladi bijeli",
        "price": 1.99,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "krompir bijeli lijevce",
        "price": 1.65,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "krompir glamocki crveni",
        "price": 2.49,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "kupus mladi",
        "price": 1.99,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "jabuka ajdared",
        "price": 1.99,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "lubenica sarena",
        "price": 4.59,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
    {
        "name": "narandza spanska",
        "price": 4.29,
        "unit": "kg",
        "type": "fruits and vegetables",
    },
]

query_find_items = """SELECT id, name FROM items WHERE name IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) AND store = ?;"""
