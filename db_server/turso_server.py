import os
import libsql_experimental as libsql
import datetime
import json


def get_config():
    with open(
        "/home/sasa/Documents/Code/prices-in-bosnia/db_server/config.json", "r"
    ) as f:
        data = f.read()
    return json.loads(data)


class Server:
    def __init__(self, db_org=None, token=None):
        self.db_org = db_org if db_org else os.getenv("turso_db_org")
        self.token = token if token else os.getenv("turso_db_token")
        if self.db_org == None or self.token == None:
            print("WARNING! TURSO CREDENTIALS NOT PROVIDED.")
            print("Using config to find them.")
            data = get_config()
            self.db_org = data["turso_db_org"]
            self.token = data["turso_db_token"]
        self.db_link = "libsql://" + self.db_org + ".turso.io"
        self.rs_mapping = {
            "Kuca": "houses",
            "Stan": "flats",
            "Zemljiste": "land",
            "Apartman": "flats",
        }

    def get_connection(self):
        # self.conn = libsql.connect("prices_bosnia.db")
        # self.cur = self.conn.cursor()
        conn = libsql.connect(database=self.db_link, auth_token=self.token)
        # If using local db
        # conn = libsql.connect("~/bosnia_prices.db", sync_url=self.db_link, auth_token=self.token)
        return conn

    def execute_script(self, file_path):
        conn = self.get_connection()
        with open(file_path, "r") as file:
            script = file.read()
        print("About to execute", script)
        conn.executescript(script)
        conn.commit()

    def transfer_scraped_links(self, links, item_type):
        conn = self.get_connection()
        cur = conn.cursor()
        if item_type == "car":
            query = "INSERT INTO links_cars (id, link, scraped) VALUES(?, ?, ?)"
        else:
            query = "INSERT INTO rs_links (id, link, type, scraped) VALUES(?, ?, ?, ?)"
        batch_size = 50
        for i in range(0, len(links), batch_size):
            batch = links[i : i + batch_size]
            cur.executemany(query, batch)
            conn.commit()
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
        print(f"Checking if {item_id} in {table}")
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM {table} WHERE id='{item_id}'")
        result = cur.fetchone()
        if result:
            return True
        return False

    def items_not_in_db(self, table, ids_list) -> list:
        """
        Checks which ids from a list are in a table.

        Args:
            table: name of the table
            ids_list: list of ids to check

        Returns:
            list: list of ids that are not in the table
        """
        print(f"Checking if {ids_list} in {table}")
        conn = self.get_connection()
        cur = conn.cursor()
        new_ids = []
        for item_id in ids_list:
            print(f"Checking {item_id}")
            cur.execute(f"SELECT id FROM {table} WHERE id={item_id}")
            result = cur.fetchone()
            if not result:
                new_ids.append(item_id)
        print(f"Found new ids - {new_ids}")
        return new_ids

    def get_non_scraped_cars(self):
        """
        Gets the list of cars that havent been scraped yet.

        Returns:
            result: 2d list of the cars that havent been scraped that contains [car_id, car_link]
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id,link FROM links_cars WHERE scraped=0;")
        result = cur.fetchall()
        return result

    def get_non_scraped_rs(self):
        """
        Gets the list of rs that havent been scraped yet.

        Returns:
            result: 2d list of the rs that havent been scraped that contains [rs_id, rs_link]
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, link, type FROM rs_links WHERE scraped=0;")
        result = cur.fetchall()
        return result

    def add_car_link(self, car_id, link, scraped, write_log_info=None):
        """
        Adds new cars to the links_cars table.

        Args:
            car_id: id of the car
            link: link of the car listing
            scraped: 0 since it is the new car and hasnt been scraped yet
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO links_cars (id, link, scraped) VALUES(?, ?, ?);",
            (car_id, link, scraped),
        )
        conn.commit()
        if write_log_info:
            write_log_info(f"{car_id} - {link} added to the database.")
        print(f"{car_id} - {link} added to the database.")

    def add_car_links(self, cars, write_log_info=None):
        """
        Adds multiple new cars to the links_cars table.

        Args:
            cars: list of lists that has car_id, link, scraped
        """
        conn = self.get_connection()
        cur = conn.cursor()
        query = "INSERT INTO links_cars (id, link, scraped) VALUES(?, ?, ?);"
        batch_size = 30
        for i in range(0, len(cars), batch_size):
            batch = cars[i : i + batch_size]
            cur.executemany(query, batch)
            conn.commit()
            if write_log_info:
                write_log_info(f"{batch} added to the database.")
            print(f"{batch} added to the database.")
        print("Finished adding new cars to the database.")

    def add_rs_link(self, rs_id, rs_link, rs_type, scraped, write_log_info=None):
        """
        Adds new rs to the rs_links table.

        Args:
            rs_id: id of the rs
            link: link of the rs listing
            scraped: 0 since it is the new rs and hasnt been scraped yet
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO rs_links(id, link, type, scraped) VALUES(?, ?, ?, ?);",
            (rs_id, rs_link, rs_type, scraped),
        )
        conn.commit()
        if write_log_info:
            write_log_info(f"{rs_id} - {rs_link} added to the database.")
        print(f"{rs_id} - {rs_link} added to the database.")

    def add_rs_links(self, rs, write_log_info=None):
        """
        Adds multiple new res to the rs_links table.

        Args:
            rs: list of lists that has rs_id, link, scraped
        """
        conn = self.get_connection()
        cur = conn.cursor()
        for rs_id, rs_link, rs_type, scraped in rs:
            cur.execute(
                "INSERT INTO rs_links(id, link, type, scraped) VALUES(?, ?, ?, ?);",
                (rs_id, rs_link, rs_type, scraped),
            )
            if write_log_info:
                write_log_info(f"{rs_id} - {rs_link} added to the database.")
            print(f"{rs_id} - {rs_link} added to the database.")
            conn.commit()

    def get_missing_seller_cars(self):
        """
        Finds and returns cars that don't have seller type info (shop or individual.)

        Returns:
            result: list of cars that seller type missing
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT links_cars.id, links_cars.link
                                FROM cars
                                LEFT JOIN links_cars
                                ON links_cars.id = cars.id
                                WHERE cars.radnja is NULL;"""
        )
        result = cur.fetchall()
        return result

    def mark_as_scraped(self, table, item_id):
        """
        Updates the status of a given id from scraped=0 to scraped=1.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE {table} SET scraped=1 WHERE id={item_id};")
        conn.commit()

    def update_seller_info(self, car_id, value):
        """
        Updates the seller type in table cars.

        Args:
            car_id: id of the car
            value: value to use as a seller type (1 for shop, 0 for individual)
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE cars SET radnja={value} WHERE id={car_id};")
        conn.commit()

    def get_car_data(self, car_id):
        """
        Gets all the data for a given car_id.

        Args:
            car_id: id of the car.

        Returns:
            result: list of all of the car properties
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM cars WHERE id={car_id}")
        result = cur.fetchone()
        return result

    def insert_car_data(self, data, write_log_info=None, write_log_error=None):
        """
        Inserts all the data from a given car into table cars.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO cars({columns}) VALUES({placeholders});"
        values = tuple(data.values())
        try:
            cur.execute(sql, values)
            conn.commit()
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
        conn = self.get_connection()
        cur = conn.cursor()
        table_name = self.rs_mapping[rs_type]
        cur.execute(f"SELECT * FROM {table_name} WHERE id={rs_id}")
        result = cur.fetchone()
        return result

    def insert_rs_data(self, rs_type, data, write_log_info=None, write_log_error=None):
        """
        Inserts all the data from a given rs into correct table.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        table_name = self.rs_mapping[rs_type]
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table_name}({columns}) VALUES({placeholders});"
        values = tuple(data.values())
        try:
            cur.execute(sql, values)
            conn.commit()
            if write_log_info:
                write_log_info(f"Scraped rs {data['ime']}")
            print(f"Scraped - {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Rs {data['ime']} doesn't have complete data. Skipping.")
            if write_log_error:
                write_log_error(f"Error: {e}. Skipping rs.")

    def rs_price_added_date(self, rs_ids_prices, date):
        """
        Checks if rs price is already added for given rs id and date.

        Args:
            rs_ids_prices: 2d list of found rs - [[rs_id, price],...]
            date: date for which we are doing the check

        Returns:
            bool: present or not present
        """
        # Fetch individual id given
        # query = (
        #     f"SELECT rs_id, price, date FROM rs_prices WHERE rs_id={rs_id} AND date='{date}';"
        # )
        # Fetch all ids stored that day and compare against them?
        query = f"SELECT rs_id FROM rs_prices WHERE date='{date}'"
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        if not result:
            return rs_ids_prices
        all_ids = [x[0] for x in result]
        new_ids = []
        for rs in rs_ids_prices:
            if rs[0] not in all_ids:
                new_ids.append(rs)
        print(
            f"Checked rs_prices for {rs_ids_prices[:10]}... on {date} and got {len(new_ids)} new ids."
        )
        return new_ids

    def add_rs_prices(self, rs_found):
        """
        Inserts prices for all rs found. Checks if already inserted that day.

        Args:
            rs_found: 2d list of found rs - [[rs_id, price],...]
        """
        conn = self.get_connection()
        cur = conn.cursor()
        today = datetime.date.today().isoformat()
        new_rs_today = self.rs_price_added_date(rs_found, today)
        to_add = [(rs[0], rs[0], today) for rs in new_rs_today]
        query = "INSERT INTO rs_prices (rs_id, price, date) VALUES(?, ?, ?)"
        batch_size = 30
        for i in range(0, len(to_add), batch_size):
            batch = to_add[i : i + batch_size]
            cur.executemany(query, batch)
            conn.commit()
        print("Inserted rs prices found.")

    def get_stats(self):
        """
        Returns the general stats, number of scraped cars and cars left to scrape.

        Returns:
            Message that is sent to ntfy that contains number of scraped cars and number of cars left to scrape.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        non_scraped_cars = len(self.get_non_scraped_cars())
        non_scraped_rs = len(self.get_non_scraped_rs())
        cur.execute("SELECT COUNT(id) FROM cars;")
        result = cur.fetchall()
        total_cars = result[0][0]
        cur.execute(
            "SELECT (SELECT COUNT(id) FROM houses) + (SELECT COUNT(id) FROM flats) + (SELECT COUNT(id) FROM land);"
        )
        result = cur.fetchall()
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
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        return result[0]

    def get_cars_basic_info(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cars_basic_info;")
        result = cur.fetchall()
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
        conn = self.get_connection()
        cur = conn.cursor()
        items_names = [item["name"] for item in items_list]
        print(f"Running check if items exist against {items_names[:10]}")
        cur.execute(f"SELECT name FROM items WHERE store = '{store}';")
        data = cur.fetchall()
        print("Checked for items using if_items_exist and got", data)
        if data:
            existing_items = [x[0] for x in data]
            missing_items = set(items_names) - set(existing_items)
            items_to_add = [
                item for item in items_list if item["name"] in missing_items
            ]
        else:
            print("All items are new items.")
            items_to_add = items_list
        return items_to_add

    def insert_items(self, items_list, store):
        """
        Inserts item name, type, unit, store into items table.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        query = "INSERT INTO items (name, type, unit, store) VALUES (?, ?, ?, ?);"
        batch_size = 30
        for i in range(0, len(items_list), batch_size):
            batch = items_list[i : i + batch_size]
            insert_data = []
            for item in batch:
                insert_data.append((item["name"], item["type"], item["unit"], store))
            cur.executemany(query, insert_data)
            conn.commit()

    def insert_item_prices(self, items_list, store, date):
        """
        Insert items into item_prices table. We store the price of the each item and the date on which it was scraped.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        # We are going to insert 100 items at a time.
        conn = self.get_connection()
        cur = conn.cursor()
        batch_size = 30
        for i in range(0, len(items_list), batch_size):
            batch = items_list[i : i + batch_size]
            names = [item["name"] for item in batch]

            placeholders = ", ".join(["?"] * len(batch))
            query = f"SELECT id, name FROM items WHERE name IN ({placeholders}) AND store = ?;"
            cur.execute(query, (*names, store))
            result = cur.fetchall()

            items_id = {name: sid for sid, name in result}
            batch_items_data = [
                (items_id[item["name"]], item["price"], date) for item in batch
            ]

            query = "INSERT INTO item_prices (item_id, price, date) VALUES (?, ?, ?);"
            cur.executemany(query, batch_items_data)
            conn.commit()
        self.increase_total_scraped("items_dates", len(items_list))

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
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE {date_column}=?;", (date,))
        result = cur.fetchall()
        return result

    def get_items_on_date(self, date):
        """
        Gets all items and their prices from a given date.

        Args:
            date (str): The date on which to get the items, in the format YYYY-MM-DD.

        Returns:
            result (list): A list of tuples containing the items from the given store.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        query = """
            SELECT items.name, items.type, items.unit, items.store, item_prices.price, item_prices.date
            FROM items
            JOIN item_prices ON items.id = item_prices.item_id
            WHERE item_prices.date = ?;
        """
        cur.execute(query, (date,))
        result = cur.fetchall()
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
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM {table} WHERE {date_column} BETWEEN %s AND %s;",
            (start_date, end_date),
        )
        result = cur.fetchall()
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
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT DISTINCT {column_name} FROM {table};")
        result = cur.fetchall()
        result = [x[0] for x in result]
        return result

    def increase_total_scraped(self, column, amount):
        conn = self.get_connection()
        cur = conn.cursor()
        if column in self.rs_mapping:
            column = self.rs_mapping[column]
        query = f"UPDATE scraping_stats SET {column} = {column} + {amount};"
        cur.execute(query)
        conn.commit()

    def get_totals(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM scraping_stats;")
        result = cur.fetchall()
        return result

    def get_triggers(self):
        conn = self.get_connection()
        cur = conn.cursor()
        query = 'SELECT name, sql FROM sqlite_master WHERE type="trigger"'
        cur.execute(query)
        result = cur.fetchall()
