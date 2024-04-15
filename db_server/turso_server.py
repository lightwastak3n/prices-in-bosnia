import os
import libsql_experimental as libsql
from time import sleep

class Server:
    def __init__(self, db_org=None, token=None):
        self.db_org = db_org if db_org else os.getenv("turso_db_org")
        self.token = token if token else os.getenv("turso_db_token")
        self.db_link = "libsql://" + self.db_org + ".turso.io"
        self.conn = libsql.connect(database=self.db_link, auth_token=self.token)
        # self.conn = libsql.connect("prices_bosnia.db")
        self.cur = self.conn.cursor()
        self.rs_mapping = {"Kuca": "houses", "Stan": "flats", "Zemljiste": "land", "Apartman": "flats"}

    def execute_script(self, file_path):
        with open(file_path, 'r') as file:
            script = file.read()
        self.conn.executescript(script)
        self.conn.commit()

    def transfer_scraped_links(self, links, item_type):
        if item_type == "car":
            query = "INSERT INTO links_cars (id, link, scraped) VALUES(?, ?, ?)"
        else:
            query = "INSERT INTO rs_links (id, link, type, scraped) VALUES(?, ?, ?, ?)"
        batch_size = 50
        for i in range(0, len(links), batch_size):
            batch = links[i:i+batch_size]
            self.cur.executemany(query, batch)
            self.conn.commit()
            print(f"Inserted {i} links.")
            print("Last inserted", batch[-1])
        print("Done.")

    def item_in_db(self, table, item_id):
        """
        Checks if an item is in database.

        Args:
            table: name of the table
            item_id: id of the item

        Returns:
            bool: True if the item is in database already. False otherwise.
        """
        self.cur.execute(f"SELECT id FROM {table} WHERE id='{item_id}'")
        result = self.cur.fetchone()
        if result:
            return True
        return False

    def items_not_in_db(self, table, ids_list):
        """
        Checks which ids from a list are in a table.

        Args:
            table: name of the table
            ids_list: list of ids to check

        Returns:
            list: list of ids that are not in the table
        """
        new_ids = []
        for sid in ids_list:
            present = self.item_in_db(table, sid)
            if not present:
                new_ids.append(sid)
        return new_ids

    def get_non_scraped_cars(self):
        """
        Gets the list of cars that havent been scraped yet.

        Returns:
            result: 2d list of the cars that havent been scraped that contains [car_id, car_link]
        """
        self.cur.execute("SELECT id,link FROM links_cars WHERE scraped=0;")
        result = self.cur.fetchall()
        return result
    
    def get_non_scraped_rs(self):
        """
        Gets the list of rs that havent been scraped yet.

        Returns:
            result: 2d list of the rs that havent been scraped that contains [rs_id, rs_link]
        """
        self.cur.execute("SELECT id, link, type FROM rs_links WHERE scraped=0;")
        result = self.cur.fetchall()
        return result

    def add_car_link(self, car_id, link, scraped, write_log_info=None):
        """
        Adds new cars to the links_cars table.

        Args:
            car_id: id of the car
            link: link of the car listing
            scraped: 0 since it is the new car and hasnt been scraped yet
        """
        self.cur.execute("INSERT INTO links_cars VALUES(?, ?, ?);",
                           (car_id, link, scraped))
        self.conn.commit()
        if write_log_info:
            write_log_info(f"{car_id} - {link} added to the database.")
        print(f"{car_id} - {link} added to the database.")

    def add_car_links(self, cars, write_log_info=None):
        """
        Adds multiple new cars to the links_cars table.

        Args:
            cars: list of lists that has car_id, link, scraped
        """
        for car_id, link, scraped in cars:
            self.cur.execute("INSERT INTO links_cars VALUES(?, ?, ?);",
                        (car_id, link, scraped))
            if write_log_info:
                write_log_info(f"{car_id} - {link} added to the database.")
            print(f"{car_id} - {link} added to the database.")
        self.conn.commit()

    def add_rs_link(self, rs_id, rs_link, rs_type, scraped, write_log_info=None):
        """
        Adds new rs to the rs_links table.

        Args:
            rs_id: id of the rs
            link: link of the rs listing
            scraped: 0 since it is the new rs and hasnt been scraped yet
        """
        self.cur.execute("INSERT INTO rs_links VALUES(?, ?, ?, ?);",
                           (rs_id, rs_link, rs_type, scraped))
        self.conn.commit()
        if write_log_info:
            write_log_info(f"{rs_id} - {rs_link} added to the database.")
        print(f"{rs_id} - {rs_link} added to the database.")

    def add_rs_links(self, rs, write_log_info=None):
        """
        Adds multiple new res to the rs_links table.

        Args:
            rs: list of lists that has rs_id, link, scraped
        """
        for rs_id, rs_link, rs_type, scraped in rs:
            self.cur.execute("INSERT INTO rs_links VALUES(?, ?, ?, ?);",
                        (rs_id, rs_link, rs_type, scraped))
            if write_log_info:
                write_log_info(f"{rs_id} - {rs_link} added to the database.")
            print(f"{rs_id} - {rs_link} added to the database.")
        self.conn.commit()

    def get_missing_seller_cars(self):
        """
        Finds and returns cars that don't have seller type info (shop or individual.)

        Returns:
            result: list of cars that seller type missing
        """
        self.cur.execute("""SELECT links_cars.id, links_cars.link
                                FROM cars
                                LEFT JOIN links_cars
                                ON links_cars.id = cars.id
                                WHERE cars.radnja is NULL;""")
        result = self.cur.fetchall()
        return result

    def mark_as_scraped(self, table, item_id):
        """
        Updates the status of a given id from scraped=0 to scraped=1.
        """
        self.cur.execute(
            f"UPDATE {table} SET scraped=1 WHERE id={item_id};")
        self.conn.commit()

    def update_seller_info(self, car_id, value):
        """
        Updates the seller type in table cars.

        Args:
            car_id: id of the car
            value: value to use as a seller type (1 for shop, 0 for individual)
        """
        self.cur.execute(
            f"UPDATE cars SET radnja={value} WHERE id={car_id};")
        self.conn.commit()

    def get_car_data(self, car_id):
        """
        Gets all the data for a given car_id.

        Args:
            car_id: id of the car.

        Returns:
            result: list of all of the car properties
        """
        self.cur.execute(f"SELECT * FROM cars WHERE id={car_id}")
        result = self.cur.fetchone()
        return result

    def insert_car_data(self, data, write_log_info=None, write_log_error=None):
        """
        Inserts all the data from a given car into table cars.
        """
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO cars({columns}) VALUES({placeholders});"
        values = tuple(data.values())
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            if write_log_info:
                write_log_info(f"Scraped car {data['ime']}")
            print(f"Scraped car {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Car {data['ime']} doesn't have complete data. Skipping.")
            if write_log_error:
                write_log_error(f"Error: {e}. Skipping car.")

    def get_rs_data(self, rs_type, rs_id):
        """
        Gets all the data for a given rs_id

        Args:
            type: type of rs (house, flat, land)
            rs_id: id of the real estate.

        Returns:
            result: list of all of the rs properties
        """
        table_name = self.rs_mapping[rs_type]
        self.cur.execute(f"SELECT * FROM {table_name} WHERE id={rs_id}")
        result = self.cur.fetchone()
        return result

    def insert_rs_data(self, rs_type, data, write_log_info=None, write_log_error=None):
        """
        Inserts all the data from a given rs into correct table.
        """
        table_name = self.rs_mapping[rs_type]
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table_name}({columns}) VALUES({placeholders});"
        values = tuple(data.values())
        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            if write_log_info:
                write_log_info(f"Scraped rs {data['ime']}")
            print(f"Scraped - {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Rs {data['ime']} doesn't have complete data. Skipping.")
            if write_log_error:
                write_log_error(f"Error: {e}. Skipping rs.")

    def get_stats(self):
        """
        Returns the general stats, number of scraped cars and cars left to scrape.

        Returns:
            Message that is sent to ntfy that contains number of scraped cars and number of cars left to scrape.
        """
        non_scraped_cars = len(self.get_non_scraped_cars())
        non_scraped_rs = len(self.get_non_scraped_rs())
        self.cur.execute("SELECT COUNT(id) FROM cars;")
        result = self.cur.fetchall()
        total_cars = result[0][0]
        self.cur.execute("SELECT (SELECT COUNT(id) FROM houses) + (SELECT COUNT(id) FROM flats) + (SELECT COUNT(id) FROM land);")
        result = self.cur.fetchall()
        total_rs = result[0][0]
        return f"Cars scraped {total_cars}. Left to scrape {non_scraped_cars}.\nRs scraped {total_rs}. Left to scrape {non_scraped_rs}."

    def count_item_prices_for_store(self, store):
        """
        Counts the number of prices for a given store.

        Args:
            store (str): The name of the store to count the prices for.

        Returns:
            result (int): The number of prices for the given store.
        """
        query = f"""
            SELECT COUNT(*) AS num_records
            FROM items
            JOIN item_prices ON items.id = item_prices.item_id
            WHERE items.store = '{store}';
        """        
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0]

    def get_cars_basic_info(self):
        self.cur.execute("SELECT * FROM cars_basic_info;")
        result = self.cur.fetchall()
        return result

    def check_if_items_exist(self, items_list, store):
        """
        Checks if items exist in the items table.
        Since we are scraping one store we can just fetch all items from that store that are in our table.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store to check for the items.

        Returns:
            items_to_add: A list of missing items that are not in the items table for the specified store.
        """
        items_names = [item['name'] for item in items_list]
        self.cur.execute(f"SELECT name FROM items WHERE store = '{store}';")
        data = self.cur.fetchall()
        if data:
            existing_items = [x[0] for x in data]
            missing_items = set(items_names) - set(existing_items)
            items_to_add = [item for item in items_list if item['name'] in missing_items]
        else:
            items_to_add = items_list
        return items_to_add
    
    def insert_items(self, items_list, store):
        """
        Inserts item name, type, unit, store into items table.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        for item in items_list:
            self.cur.execute("INSERT INTO items (name, type, unit, store) VALUES (?, ?, ?, ?);", (item['name'], item['type'], item['unit'], store))
        self.conn.commit()

    def insert_item_prices(self, items_list, store, date):
        """
        Insert items into item_prices table. We store the price of the each item and the date on which it was scraped.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        # We are going to insert 100 items at a time.
        batch_size = 50
        for i in range(0, len(items_list), batch_size):
            batch = items_list[i:i+batch_size]
            names = [item['name'] for item in batch]

            placeholders = ', '.join(['?'] * len(batch))
            query = f"SELECT id, name FROM items WHERE name IN ({placeholders}) AND store = ?;"
            self.cur.execute(query, (*names, store))
            result = self.cur.fetchall()
            
            items_id = {name: sid for sid, name in result}
            batch_items_data = [(items_id[item['name']], item['price'], date) for item in batch]

            query = "INSERT INTO item_prices (item_id, price, date) VALUES (?, ?, ?);"
            self.cur.executemany(query, batch_items_data)

        self.conn.commit()

    def get_records_on_date(self, table, date_column, date):
        """
        Gets all records from a given table on a given date.

        Args:
            table (str): The name of the table to get the records from.
            date_column (str): The name of the column that contains the date.
            date (str): The date on which to get the records, in the format YYYY-MM-DD.

        Returns:
            result (list): A list of dictionaries containing the records from the given table.
        """
        self.cur.execute(f"SELECT * FROM {table} WHERE {date_column}=?;", (date,))
        result = self.cur.fetchall()
        return result

    def get_items_on_date(self, date):
        """
        Gets all items and their prices from a given date.

        Args:
            date (str): The date on which to get the items, in the format YYYY-MM-DD.

        Returns:
            result (list): A list of tuples containing the items from the given store.
        """
        query = """
            SELECT items.name, items.type, items.unit, items.store, item_prices.price, item_prices.date
            FROM items
            JOIN item_prices ON items.id = item_prices.item_id
            WHERE item_prices.date = ?;
        """
        self.cur.execute(query, (date,))
        result = self.cur.fetchall()
        return result
        
    def get_records_from_to_date(self, table, date_column, start_date, end_date):
        """
        Gets the items from a given table that have a date between two dates.

        Args:
            table (str): The name of the table to get the records from.
            date_column (str): The name of the column that contains the date.
            start_date (str): The start date, in the format YYYY-MM-DD.
            end_date (str): The end date, in the format YYYY-MM-DD.
        """
        self.cur.execute(f"SELECT * FROM {table} WHERE {date_column} BETWEEN %s AND %s;", (start_date, end_date))
        result = self.cur.fetchall()
        return result
    
    def get_distinct_items_table_column(self, table, column_name):
        """
        Gets the distinct values of a given column from a given table.

        Args:
            table (str): The name of the table to get the distinct values from.
            column_name (str): The name of the column to get the distinct values from.
        
        Returns:
            result (list): A list of values containing the distinct values from the given column.
        """
        self.cur.execute(f"SELECT DISTINCT {column_name} FROM {table};")
        result = self.cur.fetchall()
        result = [x[0] for x in result]
        return result

    def increase_total_scraped(self, column, amount):
        if column in self.rs_mapping:
            column = self.rs_mapping[column]
        query = f"UPDATE scraping_stats SET {column} = {column} + {amount};"
        self.cur.execute(query)
        self.conn.commit()

    def get_totals(self):
        self.cur.execute("SELECT * FROM scraping_stats;")
        result = self.cur.fetchall()
        return result

    def get_triggers(self):
        query = 'SELECT name, sql FROM sqlite_master WHERE type="trigger"' 
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

