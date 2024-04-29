import requests
import re
import js2py
import json

from datetime import datetime, date
from bs4 import BeautifulSoup


def run_js(js):
    target_script = js.replace("new Map([])", "[]")
    output = js2py.eval_js(target_script)
    output = str(output)
    if "Request failed with status code 404" in output:
        print("Listing deleted")
        return None
    # Fix for car models that break json
    output = output.replace("cee'd", "ceed")
    output = output.replace("R'line", "Rline")

    output = (
        output.replace("None", "null")
        .replace("False", "false")
        .replace('"', "")
        .replace("True", "true")
        .replace("'", '"')
        .replace("\\", "")
    )
    pattern = r'"description":\s*".*?"\s*,\s*"updated_at"'
    output = re.sub(pattern, '"description": null, "updated_at"', output)
    try:
        output = json.loads(output)
    except json.decoder.JSONDecodeError:
        print("Json decode error probably some shit in the title")
        print(output)
        return None
    return output


class CarScraper:
    """
    Car scraper object that scrapes the main page and checks for new cars and also scrapes individual cars.

    Attributes:
            MAIN_URL: Url of the default location where vehicles are published.
            main_page: Stores raw html of the MAIN_URL
            cars: Dictionary that stores id: link of the cars found on main page.
    """

    def __init__(self) -> None:
        """
        Initializes car scraper.
        """
        self.MAIN_URL = "https://olx.ba/pretraga?attr=&category_id=18&sort_by=date&sort_order=desc&price_from=1&listing_type=sell&page=1"
        self.main_page = None
        self.cars = {}

    def get_soup(self, url):
        """
        Gets the raw html of url. Sites block regular requests so we use user agent.

        Parameters:
            url: Url for which to get html.

        Returns:
            Returns raw html.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Referer": "https://bing.com/",
        }
        response = requests.get(url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def get_main_page(self):
        """
        Gets the html of the MAIN_PAGE and stores it in main_page object attribute
        """
        self.main_page = self.get_soup(self.MAIN_URL)

    def get_cars_from_main(self, request_main_page=True):
        """
        Gets all the links found under div class: "naslov".
        Each link corressponds to a car.
        The links are stored in self.cars attribute.
        """
        if request_main_page:
            self.get_main_page()
        all_scripts = self.main_page.findAll("script")
        for script in all_scripts:
            if script.contents and "window.__NUXT__" in script.contents[0][:50]:
                target_script = script.contents[0]
                break
        print("Found script", target_script[:50])
        data = run_js(target_script)
        for listing in data["state"]["search"]["results"]:
            self.cars[listing["id"]] = f"https://olx.ba/artikal/{listing['id']}/"

    def get_found_ids(self) -> list:
        """
        Get the list of found ids.

        Returns:
            ids: List of all the new ids found
        """
        ids = list(self.cars)
        return ids

    def akcijska_cijena(self, car_soup, data):
        """
        Akcijska cijena is in a different class so we need special fix for that.

        Args:
            car_soup: soup object (like a raw html) generated from the cars webpage
            data: Car attributes found.
        """
        target_div = car_soup.findAll("div", {"class": "op pop"})[0]
        price_p = target_div.find("p")
        price = price_p.text.split("KM")[1]
        data["Cijena"] = price

    def get_car_specs(self, car_soup, car_id):
        """
        Gets all the specs it can found on a given car page.
        Name is found manually as h2 tag.
        Most of the data is found via table. Some is found via labels.
        The rest is found using class lookup in bs4 and regex.

        Args:
            car_soup: soup object (like a raw html) generated from the cars webpage
            car_id: id of the car found
        Returns:
            data: dictionary with found car data
        """
        # Run window.__NUXT__ function and get the data
        data = {"id": car_id, "datum": f"{date.today()}"}
        all_scripts = car_soup.findAll("script")
        for script in all_scripts:
            if script.contents and "window.__NUXT__" in script.contents[0][:50]:
                target_script = script.contents[0]
                output = run_js(target_script)
                if output == None:
                    print("Skipping")
                    return None

                # Get name, id, price
                print("Getting name and price")
                data["Ime"] = output["data"][0]["title"]
                if output["data"][0]["listing"]["display_price"] == "Na upit":
                    return None
                data["Cijena"] = output["data"][0]["listing"]["price"]

                # Table data
                print("Getting table data")
                for prop in output["data"][0]["listing"]["attributes"]:
                    if prop["value"] == "true":
                        prop_val = 1
                    elif prop["value"] == "false":
                        prop_val = 0
                    else:
                        prop_val = prop["value"]
                    data[prop["name"]] = prop_val

                # Get brand and model
                if output["data"][0]["listing"]["brand"] != None:
                    data["Proizvođač"] = output["data"][0]["listing"]["brand"]["name"]
                if output["data"][0]["listing"]["model"] != None:
                    data["Model"] = output["data"][0]["listing"]["model"]["name"]

                # Get the location
                print("Getting location")
                data["Lokacija"] = output["data"][0]["listing"]["cities"][0]["name"]

                # Get the type of seller
                print("Getting seller info")
                seller_type = output["data"][0]["listing"]["user"]["type"]
                shop = 1 if seller_type == "shop" else 0
                data["radnja"] = shop

                # FFS olx what the fuck is with these random properties
                # Deleting al these
                print("Deleting extra columns if needed")
                if "Vrsta opreme" in data:
                    del data["Vrsta opreme"]
                if "Ime i broj licence agenta" in data:
                    del data["Ime i broj licence agenta"]
                if "Broj posredničkog ugovora" in data:
                    del data["Broj posredničkog ugovora"]

                # Get the number of views and all the dates
                print("Getting views and dates")
                data["Broj pregleda"] = output["data"][0]["listing"]["views"]
                data["Datum objave"] = datetime.fromtimestamp(
                    int(output["data"][0]["listing"]["created_at"])
                ).strftime("%Y-%m-%d")
                if "date" in output["data"][0]["listing"]:
                    data["Obnovljen"] = datetime.fromtimestamp(
                        int(output["data"][0]["listing"]["date"])
                    ).strftime("%Y-%m-%d")

                # Get listing type
                listing_type_map = {"sell": "prodaja", "rent": "iznajmljivanje"}
                data["Vrsta oglasa"] = listing_type_map[
                    output["data"][0]["listing"]["listing_type"]
                ]

                # Get the state
                print("Getting state")
                if output["data"][0]["listing"]["state"] == "none":
                    if data["Kilometraža"] < 500:
                        data["Stanje"] = "novo"
                    else:
                        data["Stanje"] = "koristeno"
                else:
                    state_map = {"used": "koristeno", "new": "novo"}
                    data["Stanje"] = state_map[output["data"][0]["listing"]["state"]]
                print("Finished getting data")

        return data

    def scrape_car(self, car_id, car_link, write_log_info):
        """
        Scrapes individual car. Skipps if the car is already deleted from the website (empty webpage).

        Args:
            car_id: id of a given car.
            car_link: Link of the cars webpage.

        Returns:
            Cars data.
        """
        car_soup = self.get_soup(car_link)
        try:
            data = self.get_car_specs(car_soup, car_id)
            return data
        except KeyError:
            print(f"Car {car_link} deleted. Skipping.")
            write_log_info(f"Car {car_link} deleted. Skipping.")
        return None
