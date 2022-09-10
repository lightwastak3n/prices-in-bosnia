import mysql.connector
import json
import os

from mysql.connector import Error
from log_maker import write_log_info, write_log_error

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

    def __init__(self) -> None:
        """
        Initializes Server object and populates attributes by loading the from the .json file.
        """
        self.load_config()

    def load_config(self):
        """
        Loads MySQL config into object attributes.
        """
        CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
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

    def create_database(self):
        """
        Creates database prices.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE prices;")

    def create_table_links_real_estate(self):
        """
        Creates table that stores id, links, and status (scraped or not) of a car found on main page of OLX.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('''CREATE TABLE links_real_estate
                (id INT PRIMARY KEY NOT NULL UNIQUE,
                link TEXT NOT NULL,
                scraped INT);''')

    def create_table_real_estate(self):
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

    def database_setup(self):
        """
        Create database and car tables.
        """
        self.create_connection()
        self.create_database()
        self.create_table_car_links()
        self.create_table_cars()
        self.close_connection()

    def car_in_db(self, car_id):
        """
        Checks if a car is in database.

        Args:
            car_id: id of the car

        Returns:
            bool: True if the car is in database already. False otherwise.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM links_cars WHERE id='{car_id}'")
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

    def add_link(self, car_id, link, scraped):
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

    def mark_as_scraped(self, car_id):
        """
        Updates the status of car in links_cars from scraped=0 to scraped=1.
        """
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE links_cars SET scraped=1 WHERE id={car_id};")
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
            cursor.execute(f"UPDATE cars SET radnja={value} WHERE id={car_id};")
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
                cursor.execute(sql,values)
            self.connection.commit()
            write_log_info(f"Scraped car {data['ime']}")
            print(f"Scraped car {data['ime']}")
        except Exception as e:
            print(f"Error {e}. Car {data['ime']} doesn't have complete data. Skipping.")
            write_log_error(f"Error: {e}. Skipping car.") 
        finally:
            self.connection.close()

    def get_stats(self):
        """
        Returns the general stats, number of scraped cars and cars left to scrape.

        Returns:
            Message that is sent to ntfy that contains number of scraped cars and number of cars left to scrape.
        """
        non_scraped = len(self.get_non_scraped_cars())
        self.create_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(id) FROM links_cars;")
            result = cursor.fetchall()
        car_scraped = result[0][0]
        self.close_connection()
        return f"Cars scraped {car_scraped}. Left to scrape {non_scraped}."
