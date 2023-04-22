import mysql.connector
import json
import os

from mysql.connector import Error

class Server:
    """
    Represents connection with the MySQL server.
    Creates databases, tables.
    Runs queries on the database.

    Attributes:
        HOST: IP of the MySQL server
        PORT: Port of the MySQL server
        DATABASE: Name of the database to which to connect
        USER: Username to use
        PASSWORD: Password to use
        connection: connection used to comunicate with the database.
    """

    def __init__(self, configfile="config.json") -> None:
        """
        Initializes Server object and populates attributes by loading the from the .json file.
        """
        self.load_config(configfile)
        self.rs_mapping = {"Kuca": "houses", "Stan": "flats", "Zemljiste": "land"}

    def load_config(self, configfile):
        """
        Loads MySQL config into object attributes.
        """
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), configfile)
        with open(CONFIG_FILE, 'r') as cnf:
            config = json.load(cnf)
        self.HOST = config['host']
        self.PORT = config['port']
        self.DATABASE = config['database']
        self.USER = config['user']
        self.PASSWORD = config['password']

    def create_connection(self):
        """
        Creates connection and stores it as attribute.
        """
        self.connection = self.get_connection()

    def get_connection(self):
        """
        Creates connection.
        """
        try:
            connection = mysql.connector.connect(
                host=self.HOST,
                port=self.PORT,
                database=self.DATABASE,
                user=self.USER,
                password=self.PASSWORD)
            if connection.is_connected():
                return connection
        except Error as e:
            print("Error while connecting", e)

    def close_connection(self):
        """
        Closes connection stored in the attribute.
        """
        self.connection.close()

    def create_database(self, db_name):
        """
        Creates database prices.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {db_name};")

    def create_table_car_links(self):
        """
        Creates table that stores id, links, and status (scraped or not) of a car found on main page of OLX.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE links_cars
                (id INT PRIMARY KEY NOT NULL UNIQUE,
                link TEXT NOT NULL,
                scraped INT);''')

    def create_table_cars(self):
        """
        Creates table that stores cars and their properties.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE cars
                            (id INT NOT NULL UNIQUE,
                            ime TEXT NOT NULL,
                            cijena INT NOT NULL,
                            stanje TEXT,
                            lokacija TEXT,
                            obnovljen TEXT,
                            proizvodjac TEXT NOT NULL,
                            model TEXT NOT NULL,
                            godiste INT NOT NULL,
                            kilometraza INT,
                            kilovata INT,
                            kubikaza TEXT,
                            gorivo TEXT,
                            vrata INT,
                            konjskih_snaga INT,
                            metalik INT,
                            masa TEXT,
                            tip TEXT,
                            pogon TEXT,
                            emisioni_standard TEXT,
                            velicina_felgi INT,
                            transmisija TEXT,
                            brzina TEXT,
                            boja TEXT,
                            ozvucenje TEXT,
                            parking_senzori TEXT,
                            parking_kamera TEXT, 
                            registrovan_do TEXT,
                            prva_registracija INT,
                            prethodnih_vlasnika INT,
                            gume TEXT,
                            visezonska_klima TEXT,
                            rolo_zavjese TEXT,
                            svjetla TEXT,
                            zastita_blokada TEXT,
                            sjedecih_mjesta TEXT,
                            turbo INT,
                            start_stop_sistem INT,
                            dpf_fap_filter INT,
                            park_assist INT,
                            strane_tablice INT,
                            registrovan INT,
                            ocarinjen INT,
                            na_lizingu INT,
                            prilagodjen_invalidima INT,
                            servisna_knjiga INT,
                            servo_volan INT,
                            komande_na_volanu INT,
                            tempomat INT,
                            abs INT,
                            esp INT,
                            airbag INT,
                            el_podizaci_stakala INT,
                            elektricni_retrovizori INT,
                            senzor_mrtvog_ugla INT,
                            klima INT,
                            digitalna_klima INT,
                            navigacija INT,
                            touch_screen INT,
                            siber INT,
                            panorama_krov INT,
                            naslon_za_ruku INT,
                            koza INT,
                            hladjenje_sjedista INT,
                            masaza_sjedista INT,
                            grijanje_sjedista INT,
                            el_pomjeranje_sjedista INT,
                            memorija_sjedista INT,
                            senzor_auto_svjetla INT,
                            alu_felge INT,
                            alarm INT,
                            centralna_brava INT,
                            daljinsko_otkljucavanje INT,
                            oldtimer INT,
                            auto_kuka INT,
                            isofix INT,
                            udaren INT,
                            vrsta_oglasa TEXT,
                            datum_objave TEXT,
                            broj_pregleda INT,
                            radnja INT,
                            datum DATE,
                            FOREIGN KEY(id) REFERENCES links_cars(id));''')

    def create_table_rs_links(self):
        """
        Creates table that stores id, links, and status (scraped or not) of a real estate found on main pages of their respective listings.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE rs_links
                (id INT PRIMARY KEY NOT NULL UNIQUE,
                link TEXT NOT NULL,
                type TEXT NOT NULL,
                scraped INT);''')

    def create_table_houses(self):
        """
        Creates a table that stores houses and their properties.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE houses
                            (id	INT NOT NULL UNIQUE,
                            ime TEXT,
                            datum DATE,
                            cijena INT,
                            kvadrata INT,
                            stanje TEXT,
                            lokacija TEXT,
                            adresa TEXT,
                            lat FLOAT,
                            lng FLOAT,
                            godina_izgradnje TEXT,
                            broj_soba INT,
                            broj_spratova INT,
                            okucnica_kvadratura INT,
                            namjestena INT,
                            vrsta_grijanja TEXT,
                            vrsta_poda TEXT,
                            struja INT,
                            voda INT,
                            primarna_orijentacija TEXT,
                            balkon INT,
                            kablovska INT,
                            ostava INT,
                            parking INT,
                            podrum INT,
                            uknjizeno INT,
                            vrsta_oglasa TEXT,
                            kanalizacija TEXT,
                            alarm INT,
                            blindirana_vrata INT,
                            garaza INT,
                            internet INT,
                            klima INT,
                            nedavno_adaptirana INT,
                            plin INT,
                            telefon INT,
                            video_nadzor INT,
                            bazen INT,
                            kompanija INT,
                            datum_objave DATE,
                            obnovljen DATE,
                            broj_pregleda INT,
                            FOREIGN KEY(id) REFERENCES rs_links(id));''')

    def create_table_flats(self):
        """
        Creates a table that stores flats and their properties.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE flats
                            (id	INT NOT NULL UNIQUE,
                            ime TEXT,
                            datum DATE,
                            cijena INT,
                            kvadrata INT,
                            stanje TEXT,
                            lokacija TEXT,
                            lat FLOAT,
                            lng FLOAT,
                            adresa TEXT,
                            godina_izgradnje TEXT,
                            broj_soba FLOAT,
                            sprat TEXT,
                            balkon INT,
                            kvadratura_balkona INT,
                            namjesten INT,
                            iznajmljeno INT,
                            vrsta_poda TEXT,
                            vrsta_grijanja TEXT,
                            kanalizacija INT,
                            parking INT,
                            struja INT,
                            uknjizeno INT,
                            voda INT,
                            vrsta_oglasa TEXT,
                            blindirana_vrata INT,
                            internet INT,
                            kablovska INT,
                            nedavno_adaptiran INT,
                            plin INT,
                            podrum INT,
                            rezije INT,
                            primarna_orijentacija TEXT,
                            klima INT,
                            lift INT,
                            telefon INT,
                            video_nadzor INT,
                            za_studente INT,
                            ostava INT,
                            kucni_ljubimci INT,
                            novogradnja INT,
                            alarm INT,
                            garaza INT,
                            kompanija INT,
                            datum_objave DATE,
                            obnovljen DATE,
                            broj_pregleda INT,
                            FOREIGN KEY(id) REFERENCES rs_links(id));''')

    def create_table_land(self):
        """
        Creates a table that stores lands and their properties.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE land
                            (id	INT NOT NULL UNIQUE,
                            ime TEXT,
                            datum DATE,
                            cijena INT,
                            kvadrata INT,
                            lokacija TEXT,
                            lat FLOAT,
                            lng FLOAT,
                            vrsta_oglasa TEXT,
                            uknjizeno INT,
                            gradjevinska_dozvola INT,
                            urbanisticka_dozvola INT,
                            komunalni_prikljucak INT,
                            udaljenost_rijeka INT,
                            iznajmljeno INT,
                            prilaz TEXT,
                            kompanija INT,
                            obnovljen DATE,
                            datum_objave DATE,
                            broj_pregleda INT,
                            FOREIGN KEY(id) REFERENCES rs_links(id));''')

    def create_table_items(self):
        """
        Creates a table that stores items from stores.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE items 
                (id INTEGER AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(255) NOT NULL,
                unit VARCHAR(255) NOT NULL,
                store VARCHAR(255) NOT NULL);''')
    
    def create_table_item_prices(self):
        """
        Creates a table that stores historical prices of items.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE item_prices 
                (id INTEGER AUTO_INCREMENT PRIMARY KEY,
                item_id INTEGER NOT NULL,
                price REAL NOT NULL,
                date DATE NOT NULL,
                FOREIGN KEY (item_id) REFERENCES items (id));''')

    def database_setup(self):
        """
        Setup all the tables.
        """
        self.create_connection()

        self.create_table_car_links()
        self.create_table_cars()

        self.create_table_rs_links()
        self.create_table_houses()
        self.create_table_flats()
        self.create_table_land()

        self.create_table_items()
        self.create_table_item_prices()

        self.close_connection()

    def item_in_db(self, table, item_id):
        """
        Checks if a car is in database.

        Args:
            car_id: id of the car

        Returns:
            bool: True if the car is in database already. False otherwise.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {table} WHERE id='{item_id}'")
            result = cursor.fetchone()
        self.close_connection()
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
        self.create_connection()
        new_ids = []
        with self.connection.cursor() as cursor:
            for id in ids_list:
                cursor.execute(f"SELECT id FROM {table} WHERE id='{id}'")
                result = cursor.fetchone()
                if not result:
                    new_ids.append(id)
        self.close_connection()
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
