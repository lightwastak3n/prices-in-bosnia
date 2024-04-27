CREATE TABLE links_cars
(id INT PRIMARY KEY NOT NULL UNIQUE,
    link TEXT NOT NULL,
    scraped INT,
    date TEXT DEFAULT CURRENT_DATE);

CREATE INDEX links_cars_scraped ON links_cars (scraped);
CREATE INDEX links_cars_date ON links_cars (date);

CREATE TABLE cars
(id INT NOT NULL UNIQUE,
    ime TEXT NOT NULL,
    cijena INT NOT NULL,
    stanje TEXT,
    lokacija TEXT,
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
    tip TEXT,
    pogon TEXT,
    emisioni_standard TEXT,
    transmisija TEXT,
    brzina TEXT,
    boja TEXT,
    registrovan_do TEXT,
    prva_registracija INT,
    prethodnih_vlasnika INT,
    gume TEXT,
    sjedecih_mjesta TEXT,
    strane_tablice INT,
    registrovan INT,
    ocarinjen INT,
    na_lizingu INT,
    servisna_knjiga INT,
    servo_volan INT,
    tempomat INT,
    abs INT,
    esp INT,
    airbag INT,
    klima INT,
    digitalna_klima INT,
    navigacija INT,
    touch_screen INT,
    oldtimer INT,
    udaren INT,
    vrsta_oglasa TEXT,
    datum_objave TEXT,
    broj_pregleda INT,
    radnja INT,
    date DATE DEFAULT CURRENT_DATE,
FOREIGN KEY(id) REFERENCES links_cars(id));

CREATE INDEX cars_date ON cars (date);

CREATE TABLE rs_links
(id INT PRIMARY KEY NOT NULL UNIQUE,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    scraped INT,
    date DATE DEFAULT CURRENT_DATE);

CREATE INDEX rs_links_scraped ON rs_links (scraped);
CREATE INDEX rs_links_date ON rs_links (date);

CREATE TABLE houses
(id	INT NOT NULL UNIQUE,
    ime TEXT,
    date DATE DEFAULT CURRENT_DATE,
    cijena INT,
    kvadrata INT,
    stanje TEXT,
    lokacija TEXT,
    adresa TEXT,
    iznajmljeno INT,
    lat FLOAT,
    lng FLOAT,
    godina_izgradnje TEXT,
    broj_soba INT,
    broj_spratova INT,
    okucnica_kvadratura INT,
    namjesten INT,
    vrsta_grijanja TEXT,
    vrsta_poda TEXT,
    struja INT,
    voda INT,
    primarna_orijentacija TEXT,
    balkon INT,
    kablovska INT,
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
    nedavno_adaptiran INT,
    plin INT,
    telefon INT,
    video_nadzor INT,
    bazen INT,
    kompanija INT,
    datum_objave DATE,
    broj_pregleda INT,
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX houses_date ON houses (date);

CREATE TABLE flats
(id	INT NOT NULL UNIQUE,
    ime TEXT,
    date DATE DEFAULT CURRENT_DATE,
    cijena INT,
    kvadrata INT,
    stanje TEXT,
    lokacija TEXT,
    lat FLOAT,
    lng FLOAT,
    adresa TEXT,
    godina_izgradnje TEXT,
    broj_soba FLOAT,
    kuhinja TEXT,
    kupatilo TEXT,
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
    kucni_ljubimci INT,
    novogradnja INT,
    alarm INT,
    garaza INT,
    kompanija INT,
    datum_objave DATE,
    broj_pregleda INT,
    tv INT,
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX flats_date ON flats (date);

CREATE TABLE land
(id	INT NOT NULL UNIQUE,
    ime TEXT,
    date DATE DEFAULT CURRENT_DATE,
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
    datum_objave DATE,
    broj_pregleda INT,
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX land_date ON land (date);

CREATE TABLE rs_prices
(id INTEGER PRIMARY KEY,
    rs_id INT,
    price INT,
    date date DEFAULT CURRENT_DATE,
    FOREIGN KEY(rs_id) REFERENCES rs_links(id));

CREATE TABLE items 
(id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    unit VARCHAR(255) NOT NULL,
    store VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE);

CREATE TABLE item_prices 
(id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    price REAL NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (item_id) REFERENCES items (id));

CREATE INDEX items_date ON item_prices (date);

CREATE TABLE scraping_stats
(id INT PRIMARY KEY,
cars INT,
houses INT,
flats INT,
land INT,
items_dates INT);

INSERT INTO scraping_stats (id, cars, houses, flats, land, items_dates) VALUES(0, 0, 0, 0, 0, 0);
