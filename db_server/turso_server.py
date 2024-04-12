import os
import libsql_experimental as libsql


class Server:
    def __init__(self, db_org, token):
        self.db_link = "libsql://" + db_org + ".turso.io"
        self.token = token
        self.conn = libsql.connect(database=self.db_link, auth_token=self.token)

    def execute_script(self, file_path):
        with open(file_path, 'r') as file:
            script = file.read()
        self.conn.executescript(script)
        self.conn.commit()

    def item_in_db(self, table, item_id):
        """
        Checks if an item is in database.

        Args:
            item_id: id of the item

        Returns:
            bool: True if the item is in database already. False otherwise.
        """
        result = self.conn.execute(f"SELECT id FROM {table} WHERE id='{item_id}'").fetchone()
        if result:
            return True
        return False

    def items_not_in_db(self, table, ids_list):
        """
        Checks which ids from a list are in a table.

        Args:
            ids_list: list of ids to check

        Returns:
            list: list of ids that are not in the table
        """
        new_ids = []
        for id in ids_list:
            result = self.conn.execute(f"SELECT id FROM {table} WHERE id='{id}'")
            if not result:
                new_ids.append(id)
        return new_ids

    def get_non_scraped_cars(self):
        """
        Gets the list of cars that havent been scraped yet.

        Returns:
            result: 2d list of the cars that havent been scraped that contains [car_id, car_link]
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id,link FROM links_cars WHERE scraped=0;")
            result = cursor.fetchall()
        self.close_connection()
        return result
    
    def get_non_scraped_rs(self):
        """
        Gets the list of rs that havent been scraped yet.

        Returns:
            result: 2d list of the rs that havent been scraped that contains [rs_id, rs_link]
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id, link, type FROM rs_links WHERE scraped=0;")
            result = cursor.fetchall()
        self.close_connection()
        return result

    def add_car_link(self, car_id, link, scraped, write_log_info):
        """
        Adds new cars to the links_cars table.

        Args:
            car_id: id of the car
            link: link of the car listing
            scraped: 0 since it is the new car and hasnt been scraped yet
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO links_cars VALUES(%s, %s, %s);",
                           (car_id, link, scraped))
            self.connection.commit()
        self.close_connection()
        write_log_info(f"{car_id} - {link} added to the database.")
        print(f"{car_id} - {link} added to the database.")

    def add_car_links(self, cars, write_log_info):
        """
        Adds multiple new cars to the links_cars table.

        Args:
            cars: list of lists that has car_id, link, scraped
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            for car_id, link, scraped in cars:
                cursor.execute(f"INSERT INTO links_cars VALUES(%s, %s, %s);",
                            (car_id, link, scraped))
                write_log_info(f"{car_id} - {link} added to the database.")
                print(f"{car_id} - {link} added to the database.")
        self.connection.commit()
        self.close_connection()

    def add_rs_link(self, rs_id, rs_link, rs_type, scraped, write_log_info):
        """
        Adds new rs to the rs_links table.

        Args:
            rs_id: id of the rs
            link: link of the rs listing
            scraped: 0 since it is the new rs and hasnt been scraped yet
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO rs_links VALUES(%s, %s, %s, %s);",
                           (rs_id, rs_link, rs_type, scraped))
            self.connection.commit()
        self.close_connection()
        write_log_info(f"{rs_id} - {rs_link} added to the database.")
        print(f"{rs_id} - {rs_link} added to the database.")

    def add_rs_links(self, rs, write_log_info):
        """
        Adds multiple new res to the rs_links table.

        Args:
            rs: list of lists that has rs_id, link, scraped
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            for rs_id, rs_link, rs_type, scraped in rs:
                cursor.execute(f"INSERT INTO rs_links VALUES(%s, %s, %s, %s);",
                            (rs_id, rs_link, rs_type, scraped))
                write_log_info(f"{rs_id} - {rs_link} added to the database.")
                print(f"{rs_id} - {rs_link} added to the database.")
        self.connection.commit()
        self.close_connection()


    def get_missing_seller_cars(self):
        """
        Finds and returns cars that don't have seller type info (shop or individual.)

        Returns:
            result: list of cars that seller type missing
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT links_cars.id, links_cars.link
                                    FROM cars
                                    LEFT JOIN links_cars
                                    ON links_cars.id = cars.id
                                    WHERE cars.radnja is NULL;""")
            result = cursor.fetchall()
        self.close_connection()
        return result

    def mark_as_scraped(self, table, item_id):
        """
        Updates the status of a given id from scraped=0 to scraped=1.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET scraped=1 WHERE id={item_id};")
            self.connection.commit()
        self.close_connection()

    def update_seller_info(self, car_id, value):
        """
        Updates the seller type in table cars.

        Args:
            car_id: id of the car
            value: value to use as a seller type (1 for shop, 0 for individual)
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE cars SET radnja={value} WHERE id={car_id};")
            self.connection.commit()
        self.close_connection()

    def get_car_data(self, car_id):
        """
        Gets all the data for a given car_id.

        Args:
            car_id: id of the car.

        Returns:
            result: list of all of the car properties
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM cars WHERE id={car_id}")
            result = cursor.fetchone()
        self.close_connection()
        return result

    def insert_car_data(self, data, write_log_info, write_log_error):
        """
        Inserts all the data from a given car into table cars.
        """
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO cars({columns}) VALUES({placeholders});"
        values = list(data.values())
        self.create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
            self.connection.commit()
            write_log_info(f"Scraped car {data['ime']}")
            print(f"Scraped car {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Car {data['ime']} doesn't have complete data. Skipping.")
            write_log_error(f"Error: {e}. Skipping car.")
        finally:
            self.connection.close()

    def get_rs_data(self, rs_type, rs_id):
        """
        Gets all the data for a given rs_id

        Args:
            type: type of rs (house, flat, land)
            rs_id: id of the real estate.

        Returns:
            result: list of all of the rs properties
        """
        self.create_connection()
        table_name = self.mapping[rs_type]
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id={rs_id}")
            result = cursor.fetchone()
        self.close_connection()
        return result

    def insert_rs_data(self, rs_type, data, write_log_info, write_log_error):
        """
        Inserts all the data from a given rs into correct table.
        """
        table_name = self.rs_mapping[rs_type]
        columns = ", ".join([str(x) for x in list(data.keys())])
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table_name}({columns}) VALUES({placeholders});"
        values = list(data.values())
        self.create_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, values)
            self.connection.commit()
            write_log_info(f"Scraped rs {data['ime']}")
            print(f"Scraped - {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Rs {data['ime']} doesn't have complete data. Skipping.")
            write_log_error(f"Error: {e}. Skipping rs.")
        finally:
            self.connection.close()

    def get_stats(self):
        """
        Returns the general stats, number of scraped cars and cars left to scrape.

        Returns:
            Message that is sent to ntfy that contains number of scraped cars and number of cars left to scrape.
        """
        non_scraped_cars = len(self.get_non_scraped_cars())
        non_scraped_rs = len(self.get_non_scraped_rs())
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(id) FROM cars;")
            result = cursor.fetchall()
            total_cars = result[0][0]
            cursor.execute("SELECT (SELECT COUNT(id) FROM houses) + (SELECT COUNT(id) FROM flats) + (SELECT COUNT(id) FROM land);")
            result = cursor.fetchall()
            total_rs = result[0][0]
        self.close_connection()
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
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        self.close_connection()
        return result[0]

    def get_cars_basic_info(self):
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cars_basic_info;")
            result = cursor.fetchall()
        self.close_connection()
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
        self.create_connection()
        items_names = [item['name'] for item in items_list]
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT name FROM items WHERE store = %s;", (store,))
            existing_items = [x[0] for x in cursor.fetchall()]
        self.close_connection()
        missing_items = set(items_names) - set(existing_items)
        items_to_add = [item for item in items_list if item['name'] in missing_items]
        return items_to_add
    
    def insert_items(self, items_list, store):
        """
        Inserts item name, type, unit, store into items table.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            for item in items_list:
                cursor.execute("INSERT INTO items (name, type, unit, store) VALUES (%s, %s, %s, %s);", (item['name'], item['type'], item['unit'], store))
        self.connection.commit()
        self.close_connection()

    def insert_item_prices(self, items_list, store, date):
        """
        Insert items into item_prices table. We store the price of the each item and the date on which it was scraped.

        Args:
            items_list (list): A list of dictionaries containing information about items.
            store (str): The name of the store in which the items are sold.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            # We are going to insert 100 items at a time.
            batch_size = 100
            for i in range(0, len(items_list), batch_size):
                batch = items_list[i:i+batch_size]
                names = [item['name'] for item in batch]

                placeholders = ', '.join(['%s'] * len(batch))
                query = f"SELECT id, name FROM items WHERE name IN ({placeholders}) AND store = %s;"
                cursor.execute(query, (*names, store))
                
                items_id = {name: id for id, name in cursor.fetchall()}
                batch_items_data = [(items_id[item['name']], item['price'], date) for item in batch]
                query = "INSERT INTO item_prices (item_id, price, date) VALUES (%s, %s, %s);"
                cursor.executemany(query, batch_items_data)

        self.connection.commit()
        self.close_connection()

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
        self.create_connection()
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} WHERE {date_column}=%s;", (date,))
            result = cursor.fetchall()
        self.close_connection()
        return result

    def get_items_on_date(self, date):
        """
        Gets all items and their prices from a given date.

        Args:
            date (str): The date on which to get the items, in the format YYYY-MM-DD.

        Returns:
            result (list): A list of tuples containing the items from the given store.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            query = """
                SELECT items.name, items.type, items.unit, items.store, item_prices.price, item_prices.date
                FROM items
                JOIN item_prices ON items.id = item_prices.item_id
                WHERE item_prices.date = %s;
            """
            cursor.execute(query, (date,))
            result = cursor.fetchall()
        self.close_connection()
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
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table} WHERE {date_column} BETWEEN %s AND %s;", (start_date, end_date))
            result = cursor.fetchall()
        self.close_connection()
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
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT DISTINCT {column_name} FROM {table};")
            result = cursor.fetchall()
            result = [x[0] for x in result]
        self.close_connection()
        return result

db_org = os.getenv("turso_db_org")
token = os.getenv("turso_db_token")
turso = Turso(db_org, token)

print(turso.show_all_records("test"))
