import csv
import calendar

from datetime import datetime
from db_server.sql_server import Server
from time import sleep

cars_columns = [
    "id",
    "ime",
    "cijena",
    "stanje",
    "lokacija",
    "obnovljen",
    "proizvodjac",
    "model",
    "godiste",
    "kilometraza",
    "kilovata",
    "kubikaza",
    "gorivo",
    "vrata",
    "konjskih_snaga",
    "metalik",
    "masa",
    "tip",
    "pogon",
    "emisioni_standard",
    "velicina_felgi",
    "transmisija",
    "brzina",
    "boja",
    "ozvucenje",
    "parking_senzori",
    "parking_kamera",
    "registrovan_do",
    "prva_registracija",
    "prethodnih_vlasnika",
    "gume",
    "visezonska_klima",
    "rolo_zavjese",
    "svjetla",
    "zastita_blokada",
    "sjedecih_mjesta",
    "turbo",
    "start_stop_sistem",
    "dpf_fap_filter",
    "park_assist",
    "strane_tablice",
    "registrovan",
    "ocarinjen",
    "na_lizingu",
    "prilagodjen_invalidima",
    "servisna_knjiga",
    "servo_volan",
    "komande_na_volanu",
    "tempomat",
    "abs",
    "esp",
    "airbag",
    "el_podizaci_stakala",
    "elektricni_retrovizori",
    "senzor_mrtvog_ugla",
    "klima",
    "digitalna_klima",
    "navigacija",
    "touch_screen",
    "siber",
    "panorama_krov",
    "naslon_za_ruku",
    "koza",
    "hladjenje_sjedista",
    "masaza_sjedista",
    "grijanje_sjedista",
    "el_pomjeranje_sjedista",
    "memorija_sjedista",
    "senzor_auto_svjetla",
    "alu_felge",
    "alarm",
    "centralna_brava",
    "daljinsko_otkljucavanje",
    "oldtimer",
    "auto_kuka",
    "isofix",
    "udaren",
    "vrsta_oglasa",
    "datum_objave",
    "broj_pregleda",
    "radnja",
    "datum",
]

flats_columns = [
    "id",
    "ime",
    "datum",
    "cijena",
    "kvadrata",
    "stanje",
    "lokacija",
    "lat",
    "lng",
    "adresa",
    "godina_izgradnje",
    "broj_soba",
    "kuhinja",
    "kupatilo",
    "sprat",
    "balkon",
    "kvadratura_balkona",
    "namjesten",
    "iznajmljeno",
    "vrsta_poda",
    "vrsta_grijanja",
    "kanalizacija",
    "parking",
    "struja",
    "uknjizeno",
    "voda",
    "vrsta_oglasa",
    "blindirana_vrata",
    "internet",
    "kablovska",
    "nedavno_adaptiran",
    "plin",
    "podrum",
    "rezije",
    "primarna_orijentacija",
    "klima",
    "lift",
    "telefon",
    "video_nadzor",
    "za_studente",
    "ostava",
    "kucni_ljubimci",
    "novogradnja",
    "alarm",
    "garaza",
    "kompanija",
    "datum_objave",
    "obnovljen",
    "broj_pregleda",
    "tv"
]

houses_columns = [
    "id",
    "ime",
    "datum",
    "cijena",
    "kvadrata",
    "stanje",
    "lokacija",
    "adresa",
    "lat",
    "lng",
    "godina_izgradnje",
    "broj_soba",
    "broj_spratova",
    "okucnica_kvadratura",
    "namjesten",
    "vrsta_grijanja",
    "vrsta_poda",
    "struja",
    "voda",
    "primarna_orijentacija",
    "balkon",
    "kablovska",
    "ostava",
    "parking",
    "podrum",
    "uknjizeno",
    "vrsta_oglasa",
    "kanalizacija",
    "alarm",
    "blindirana_vrata",
    "garaza",
    "internet",
    "klima",
    "nedavno_adaptiran",
    "plin",
    "telefon",
    "video_nadzor",
    "bazen",
    "kompanija",
    "datum_objave",
    "obnovljen",
    "broj_pregleda",
]

land_columns = [
    "id",
    "ime",
    "datum",
    "cijena",
    "kvadrata",
    "lokacija",
    "lat",
    "lng",
    "vrsta_oglasa",
    "uknjizeno",
    "gradjevinska_dozvola",
    "urbanisticka_dozvola",
    "komunalni_prikljucak",
    "udaljenost_rijeka",
    "iznajmljeno",
    "prilaz",
    "kompanija",
    "obnovljen",
    "datum_objave",
"broj_pregleda",
]

items_columns = [
    "name",
    "type",
    "unit",
    "store",
    "price",
    "date"
]


olx_columns = {
    "cars": cars_columns,
    "flats": flats_columns,
    "houses": houses_columns,
    "land": land_columns
}


def get_month_range(year, month):
    # Determine the number of days in the month
    _, num_days = calendar.monthrange(year, month)

    # Format the first day of the month
    first_day = f"{year}-{month:02d}-01"

    # Format the last day of the month
    last_day = f"{year}-{month:02d}-{num_days:02d}"

    return first_day, last_day


def generate_dates(month, year):
    dates = []
    for day in range(1, 32):
        try:
            date = datetime(year, month, day)
            formatted_date = date.strftime('%Y-%m-%d')
            dates.append(formatted_date)
        except ValueError:
            break
    return dates


def write_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerows(data)


def get_items_date(server, date):
    items = server.get_items_on_date(date)
    data = [items_columns] + items
    write_csv(data, f"sql_dumps/items_{date}.csv")


def get_olx_data(server, type, date):
    items = server.get_records_on_date(type, "datum", date)
    data = [olx_columns[type]] + items
    write_csv(data, f"sql_dumps/{type}_{date}.csv")


def get_olx_data_from_to_date(server, type, start_date, end_date):
    items = server.get_records_from_to_date(type, "datum", start_date, end_date)
    data = [olx_columns[type]] + items
    write_csv(data, f"sql_dumps/{type}_{start_date}_{end_date}.csv")


def download_everything(server, date):
    get_items_date(server, date)
    sleep(5)
    for listing_type in olx_columns:
        get_olx_data(server, listing_type, date)
        sleep(5)


server = Server()
dates = generate_dates(12, 2023) 

dates = ['2023-12-31']

for date in dates:
    download_everything(server, date)
