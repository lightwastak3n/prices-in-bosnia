import database_handler
import get_new_cars

from datetime import date
from time import sleep
from random import randint
from sqlite3 import IntegrityError
from log_maker import write_log

# Gets the html of the individual car
def get_car_soup(car_link):
    soup = get_new_cars.get_page(car_link)
    return soup

# Fix for akcijska cijena 
def akcijska_cijena(soup, data):
    target_div = soup.findAll("div", {"class": "op pop"})[0]
    price_p = target_div.find("p")
    price = price_p.text.split("KM")[1]
    data["Cijena"] = price

# Finds all fields below cars name
def get_all_specs(soup, car_id):
    # Name found manually everything else shares a class so it can be done in a loop
    name = soup.find("h1")
    name = name.text.strip()
    data = {"id": car_id, "Ime": name, "datum": f"{date.today()}"}

    # Checking if its a shop
    data['radnja'] = 1 if soup.findAll("div", {"class": "povjerenje_mmradnja"}) else 0

    basic_info = soup.findAll("p", {"class": "n"})
    for i in basic_info:
        key = i.text.strip()
        value_p = i.find_next_sibling("p")
        value = value_p.text.strip()
        data[key] = value
    # Fix for cijena shenanigans
    if "Cijena bez PDV-a" in data:
        del data["Cijena bez PDV-a"]
    elif "Cijena - Hitna prodaja [?]" in data:
        data["Cijena"] = data["Cijena - Hitna prodaja [?]"]
        del data["Cijena - Hitna prodaja [?]"]
    elif "Akcijska cijena - " in str(soup) and data.get('Cijena') == None:
        akcijska_cijena(soup, data)

    if "Cijena" in data and data["Cijena"] == "Po dogovoru":
        data["Cijena"] = "0"

    # Extra info
    extra_keys = soup.findAll("div", {"class": "df1"})
    for key in extra_keys:
        value = key.find_next_sibling("div")
        value = value.text.strip()
        if not value:
            value = 1
        key = key.text.strip()
        if key not in data:
            data[key] = value
    return data

# Fix some data to avoid headaches later
def fix_data(data):
    del data["OLX ID"]
    data["Cijena"] = data["Cijena"].rstrip(" KM").replace(".", "")
    if "," in data["Cijena"]:
        data["Cijena"] = data["Cijena"].split(",")[0]
    data["Cijena"] = int(data["Cijena"])
    if "Kilometraža" in data:
        if "," in data["Kilometraža"]:
            data["Kilometraža"] = data["Kilometraža"].split(",")[0]
        data["Kilometraža"] = int(data["Kilometraža"].replace(".",""))
    if "Broj vrata" in data:
        data["Broj vrata"] = data["Broj vrata"].split("/")[0]
    if "Veličina felgi" in data and data["Veličina felgi"] == "Ostalo":
        data["Veličina felgi"] = ""


def main(allocated_time):
    not_scraped = database_handler.get_non_scraped_cars()
    if len(not_scraped) == 0:

        write_log("No cars to scrape")
        print("No cars to scrape")

        left_over = allocated_time
    else:
        pause = randint(30,45)
        cutoff = min(len(not_scraped), allocated_time//pause)

        print(f"Cars left to scrape {len(not_scraped)}. About to scrape {cutoff}.")
        write_log(f"Cars left to scrape {len(not_scraped)}. About to scrape {cutoff}.")

        left_over = allocated_time - cutoff*pause

        write_log(f"About to scrape {not_scraped[:cutoff]}")
        print(f"About to scrape {not_scraped[:cutoff]}")

        for car_id, car_link in not_scraped[:cutoff]:

            print(f"Currently scraping {car_id} - {car_link}")
            write_log(f"Currently scraping {car_id} - {car_link}")

            soup = get_car_soup(car_link)
            data = get_all_specs(soup, car_id)
            try:
                fix_data(data)
                database_handler.insert_car_data(data)
            except KeyError as e:
                write_log(f"{e} - Car probably deleted. Skipping. {car_link}")
                print(f"{e} - Car probably deleted. Skipping. {car_link}")
            except IntegrityError as e:
                write_log(f"{e} - Skipping. {car_link}")
                print(f"{e} - Skipping. {car_link}")
            finally:
                database_handler.mark_as_scraped(car_id)
            sleep(pause)
    return left_over

