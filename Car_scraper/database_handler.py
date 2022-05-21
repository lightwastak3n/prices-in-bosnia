import sqlite3
import os
from log_maker import write_log
from specs_columns import specs_columns_mapping

SCRIPT_FOLDER = os.path.dirname(__file__)
DB_NAME = "cars_olx.db"
db = os.path.join(SCRIPT_FOLDER, DB_NAME)


# Creates database if it doesnt exist
def create_database(db):
    try:
        conn = sqlite3.connect(db)
        print("Database created.")
        conn.close()
    except:
        print("Error creating database.")


# Just ids and links - different table for the car details
def create_table_links():
    conn = sqlite3.connect(db)
    conn.execute('''CREATE TABLE links_cars
        (id INT PRIMARY KEY NOT NULL UNIQUE,
        link TEXT NOT NULL,
        scraped INT);''')
    conn.close()


# Check if the car is already in the database
def car_in_db(car_id):
    conn = sqlite3.connect(db)
    cursor = conn.execute("SELECT id FROM links_cars WHERE id=?", (car_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False


# Get cars that arent scraped yet
def get_non_scraped_cars():
    conn = sqlite3.connect(db)
    cursor = conn.execute("SELECT id,link FROM links_cars WHERE scraped=0;")
    result = cursor.fetchall()
    conn.close()
    return result


# Get cars that dont have seller type info
def get_missing_seller_cars():
    conn = sqlite3.connect(db)
    cursor = conn.execute("""SELECT links_cars.id, links_cars.link
                            FROM cars
                            LEFT JOIN links_cars
                            ON links_cars.id = cars.id
                            WHERE cars.radnja is NULL;""")
    result = cursor.fetchall()
    conn.close()
    return result

# Update car with seller type info
def update_seller_info(car_id, value):
    conn = sqlite3.connect(db)
    conn.execute(f"UPDATE cars SET radnja={value} WHERE id={car_id};")
    conn.commit()
    conn.close()


# Updates links table when the car data gets scraped
def mark_as_scraped(car_id):
    conn = sqlite3.connect(db)
    conn.execute(f"UPDATE links_cars SET scraped=1 WHERE id={car_id};")
    conn.commit()
    conn.close()


# Adds new cars from the main olx listing tab
def add_link(car_id, link, scraped):
    conn = sqlite3.connect(db)
    conn.execute(f"INSERT INTO links_cars VALUES(?, ?, ?);",
                 (car_id, link, scraped))
    conn.commit()
    conn.close()
    write_log(f"{car_id} - {link} added to the database.")
    print(f"{car_id} - {link} added to the database.")


# Cars specs table
def create_table_cars():
    conn = sqlite3.connect(db)
    conn.execute('''CREATE TABLE cars
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
                    masa INT,
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
                    prethodnih_vlasnika TEXT,
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
                    datum TEXT,
                    FOREIGN KEY(id) REFERENCES links_cars(id));''')
    conn.close()


def get_car_data(car_id):
    conn = sqlite3.connect(db)
    cursor = conn.execute("SELECT * FROM cars WHERE id=?", (car_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def insert_car_data(data):
    conn = sqlite3.connect(db)
    specs = list(data.keys())
    columns = [specs_columns_mapping[i] for i in specs]
    values = list(data.values())
    conn.execute(f"INSERT INTO cars{*columns,} VALUES{*values,};")
    write_log(f"Scraped car {data['Ime']}")
    print(f"Scraped car {data['Ime']}")
    conn.commit()
    conn.close()


def get_stats():
    non_scraped = len(get_non_scraped_cars())
    conn = sqlite3.connect(db)
    cars_scraped = conn.execute("SELECT COUNT(id) FROM cars")
    cars_scraped = list(cars_scraped)[0][0]
    return f"Cars scraped {cars_scraped}. Left to scrape {non_scraped}."

# Create database and tables
def setup_database():
    create_database(db)
    create_table_links()
    create_table_cars()

