import mysql.connector
import json
import os

from mysql.connector import Error
from utils.log_maker import write_log_info, write_log_error

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

    def database_setup(self):
        """
        Create database and car tables.
        """
        self.create_connection()
        self.create_database()

        self.create_table_car_links()
        self.create_table_cars()

        self.create_table_rs_links()
        self.create_table_houses()
        self.create_table_flats()
        self.create_table_land()
        
        self.close_connection()

    def item_in_db(self, table, car_id):
        """
        Checks if a car is in database.

        Args:
            car_id: id of the car

        Returns:
            bool: True if the car is in database already. False otherwise.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {table} WHERE id='{car_id}'")
            result = cursor.fetchone()
        self.close_connection()
        if result:
            return True
        return False

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

    def add_car_link(self, car_id, link, scraped):
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
    
    def add_rs_link(self, rs_id, rs_link, type, scraped):
        """
        Adds new cars to the links_cars table.

        Args:
            car_id: id of the car
            link: link of the car listing
            scraped: 0 since it is the new car and hasnt been scraped yet
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO rs_links VALUES(%s, %s, %s, %s);",
                           (rs_id, rs_link, type, scraped))
            self.connection.commit()
        self.close_connection()
        write_log_info(f"{rs_id} - {rs_link} added to the database.")
        print(f"{rs_id} - {rs_link} added to the database.")

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

    def mark_as_scraped(self, table, car_id):
        """
        Updates the status of a given id from scraped=0 to scraped=1.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET scraped=1 WHERE id={car_id};")
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

    def insert_car_data(self, data):
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
            print(
                f"Error {e}. Car {data['ime']} doesn't have complete data. Skipping.")
            write_log_error(f"Error: {e}. Skipping car.")
        finally:
            self.connection.close()

    def get_rs_data(self, type, rs_id):
        """
        Gets all the data for a given rs_id

        Args:
            type: type of rs (house, flat, land)
            rs_id: id of the real estate.

        Returns:
            result: list of all of the rs properties
        """
        self.create_connection()
        table_name = self.mapping[type]
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id={rs_id}")
            result = cursor.fetchone()
        self.close_connection()
        return result

    def insert_rs_data(self, type, data):
        """
        Inserts all the data from a given rs into correct table.
        """
        table_name = self.rs_mapping[type]
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

    def get_cars_basic_info(self):
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM cars_basic_info;")
            result = cursor.fetchall()
        self.close_connection()
        return result
