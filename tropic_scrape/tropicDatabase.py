import mysql.connector
from datetime import datetime


def create_groceries_table()
    connection = self.get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groceries (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groceries_prices (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        item_id INTEGER NOT NULL,
        price REAL NOT NULL,
        unit VARCHAR(255) NOT NULL,
        scraped_at DATETIME NOT NULL,
        FOREIGN KEY (item_id) REFERENCES items (id)
    )
    ''')
    connection.commit()
    connection.close()


def insert_groceries(items):
    # Groceries given as a list of dictionaries: items = [{'name': 'item1', 'price': 1.99, 'unit': 'kg'}, ...]
    connection = self.get_connection()
    cursor = connection.cursor()

    for item in items:
        # Check if the item already exists in the 'groceries' table
        cursor.execute("SELECT id FROM groceries WHERE name = ?", (item['name'],))
        item_id = cursor.fetchone()

        # If the item does not exist, insert it and get the new ID
        if item_id is None:
            cursor.execute("INSERT INTO groceries (name) VALUES (?)", (item['name'],))
            connection.commit()
            item_id = cursor.execute("SELECT LAST_INSERT_ID() AS id").fetchone()

        item_id = item_id[0]

        # Insert the price data into the 'item_prices' table
        cursor.execute('''
        INSERT INTO groceries_prices (item_id, price, unit, scraped_at)
        VALUES (?, ?, ?, ?)
        ''', (item_id, item['price'], item['unit'], datetime.now()))

    cnxn.commit()
