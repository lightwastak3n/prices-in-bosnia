CREATE TABLE links_cars
(id INT PRIMARY KEY NOT NULL UNIQUE,
    link TEXT NOT NULL,
    scraped INT);

CREATE INDEX links_cars_scraped ON links_cars (scraped);

CREATE TABLE cars
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
    FOREIGN KEY(id) REFERENCES links_cars(id));

CREATE INDEX cars_date ON cars (datum);

CREATE TABLE rs_links
(id INT PRIMARY KEY NOT NULL UNIQUE,
    link TEXT NOT NULL,
    type TEXT NOT NULL,
    scraped INT);

CREATE INDEX rs_links_scraped ON rs_links (scraped);

CREATE TABLE houses
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
    namjesten INT,
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
    nedavno_adaptiran INT,
    plin INT,
    telefon INT,
    video_nadzor INT,
    bazen INT,
    kompanija INT,
    datum_objave DATE,
    obnovljen DATE,
    broj_pregleda INT,
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX houses_date ON houses (datum);

CREATE TABLE flats
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
    tv INT,
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX flats_date ON flats (datum);

CREATE TABLE land
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
    FOREIGN KEY(id) REFERENCES rs_links(id));

CREATE INDEX land_date ON land (datum);

CREATE TABLE items 
(id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    unit VARCHAR(255) NOT NULL,
    store VARCHAR(255) NOT NULL);

CREATE TABLE item_prices 
(id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    price REAL NOT NULL,
    date DATE NOT NULL,
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

CREATE TRIGGER insert_new_land
AFTER INSERT ON land
BEGIN
    UPDATE scraping_stats SET land = land + 1;
END;

CREATE TRIGGER insert_new_house
AFTER INSERT ON houses
BEGIN
    UPDATE scraping_stats SET houses = houses + 1;
END;

CREATE TRIGGER insert_new_flats
AFTER INSERT ON flats
BEGIN
    UPDATE scraping_stats SET flats = flats + 1;
END;

CREATE TRIGGER insert_new_car
AFTER INSERT ON cars
BEGIN
    UPDATE scraping_stats SET cars = cars + 1;
END;
