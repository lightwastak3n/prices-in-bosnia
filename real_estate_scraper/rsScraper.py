import requests
import re
import json
import js2py

from time import sleep
from random import randint
from datetime import date, datetime
from bs4 import BeautifulSoup


def run_js(js):
    target_script = js.replace("new Map([])", "[]")
    output = js2py.eval_js(target_script)
    output = str(output)
    if "Request failed with status code 404" in output:
        print("Listing deleted")
        return None
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


class RealEstateScraper:
    """
    Real estate scraper object that scrapes the main page and checks for new real estate and also scrapes individual properties.

    Attributes:
            MAIN_URL: Url of the default location where real estate is published.
            main_page: Stores raw html the MAIN_URL
            properties: Dictionary that stores id: link of the real estate found on main page.
    """

    def __init__(self) -> None:
        """
        Initializes real estate scraper.
        """
        self.STANOVI_URL = "https://olx.ba/pretraga?attr=&category_id=23&sort_by=date&sort_order=desc&price_from=1&page=1"
        self.KUCE_URL = "https://olx.ba/pretraga?attr=&category_id=24&price_from=1&sort_by=date&sort_order=desc&page=1"
        self.ZEMLJISTA_URL = "https://olx.ba/pretraga?attr=&category_id=29&price_from=1&sort_by=date&sort_order=desc&page=1"
        self.main_pages = {"Stan": None, "Kuca": None, "Zemljiste": None}
        self.real_estates = {"Stan": {}, "Kuca": {}, "Zemljiste": {}}

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

    def get_main_pages(self):
        """
        Gets the html of the 3 urls defined in __init__ and stores them in main_pages dict object attribute.
        """
        self.main_pages["Stan"] = self.get_soup(self.STANOVI_URL)
        sleep(randint(5, 10))
        self.main_pages["Kuca"] = self.get_soup(self.KUCE_URL)
        sleep(randint(5, 10))
        self.main_pages["Zemljiste"] = self.get_soup(self.ZEMLJISTA_URL)

    def get_real_estates_from_main(self, get_main_pages=True):
        """
        New olx update so it uses regex insted of bs4 to get the ids.
        Gets all the ids found in __NUXT__ function return.
        """
        if get_main_pages:
            self.get_main_pages()
        for rs_type in self.main_pages:
            soup = self.main_pages[rs_type]

            all_scripts = soup.findAll("script")
            for script in all_scripts:
                if script.contents and "window.__NUXT__" in script.contents[0][:50]:
                    target_script = script.contents[0]
                    break

            print("Found script", target_script[:50])
            data = run_js(target_script)
            for listing in data["state"]["search"]["results"]:
                self.real_estates[rs_type][listing["id"]] = listing["price"]

    def get_found_ids(self) -> tuple:
        """
        Checks id of each real estate found against the ids already present in the database.

        Returns:
            Total number of new real estate found.
        """
        house_ids = list(self.real_estates["Kuca"])
        flat_ids = list(self.real_estates["Stan"])
        land_ids = list(self.real_estates["Zemljiste"])
        return house_ids, flat_ids, land_ids

    def get_all_rs_prices(self) -> list:
        """
        Gets all the rs_ids and prices as a list.
        """
        all_rs = [
            [rs_id, price]
            for rs_type, rs_dict in self.real_estates.items()
            for rs_id, price in rs_dict.items()
        ]
        return all_rs

    def akcijska_cijena(self, rs_soup, data):
        """
        Akcijska cijena is in a different class so we need special fix for that.

        Args:
            rs_soup: soup object (like a raw html) generated from the real estate webpage
            data: real estate attributes found.
        """
        target_div = rs_soup.findAll("div", {"class": "op pop"})[0]
        price_p = target_div.find("p")
        price = price_p.text.split("KM")[1]
        data["Cijena"] = price

    def get_real_estate_details(self, rs_soup, rs_id):
        """
        Gets all the specs it can found on a given rs page.
        Name is found manually as h2 tag.
        Most of the data is found via table. Some is found via labels.
        The rest is found using class lookup in bs4 and regex.

        Args:
            real_estate_soup: soup object (like a raw html) generated from the real estate webpage
            real_estate_id: id of the real estate found

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        # Run window.__NUXT__ function and get the data
        data = {"id": rs_id, "datum": f"{date.today()}"}
        all_scripts = rs_soup.findAll("script")
        for script in all_scripts:
            if script.contents and "window.__NUXT__" in script.contents[0][:50]:
                print("Finding script")
                output = run_js(script.contents[0])
                if output == None:
                    print("Skipping.")
                    return None

                # Get name, id, price
                print("Getting name and price")
                print(f"name is {output['data'][0]['title']}")
                data["Ime"] = output["data"][0]["title"]
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

                # Get the location, city and coordinates
                print("Getting location")
                data["Lokacija"] = output["data"][0]["listing"]["cities"][0]["name"]
                if "location" in output["data"][0]["listing"]:
                    data["lat"] = round(
                        float(output["data"][0]["listing"]["location"]["lat"]), 4
                    )
                    data["lng"] = round(
                        float(output["data"][0]["listing"]["location"]["lon"]), 4
                    )

                # Get the type of seller
                print("Getting seller info")
                seller_type = output["data"][0]["listing"]["user"]["type"]
                shop = 1 if seller_type == "shop" else 0
                data["kompanija"] = shop

                # FFS olx what the fuck is with these random properties
                # Deleting all these extra columns
                print("Deleting extra columns if needed")
                extra_cols = [
                    "Vrsta opreme",
                    "Ime i broj licence agenta",
                    "Broj posredničkog ugovora",
                    "Kuhinja",
                    "Broj kreveta",
                    "Vrsta",
                    "Broj kupatila",
                ]
                for col in extra_cols:
                    if col in data:
                        del data[col]

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

                # Get the state
                print("Getting state")
                print(output["data"][0]["listing"]["state"])
                state_map = {"used": "koristeno", "new": "novo"}
                if output["data"][0]["listing"]["state"] != "none":
                    data["Stanje"] = state_map[output["data"][0]["listing"]["state"]]

                # Get listing type
                listing_type_map = {"sell": "prodaja", "rent": "iznajmljivanje"}
                data["Vrsta oglasa"] = listing_type_map[
                    output["data"][0]["listing"]["listing_type"]
                ]
                print("Got all the data")

        print(data)
        return data

    def scrape_real_estate(self, rs_id, rs_type, write_log_info):
        """
        Scrapes individual real_estate.

        Args:
            rs_id: id of a given real estate.
            rs_link: Link of the real estate's webpage.

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        rs_link = f"https://olx.ba/artikal/{rs_id}/"
        rs_soup = self.get_soup(rs_link)
        try:
            data = self.get_real_estate_details(rs_soup, rs_id, rs_type)
            if data and "Plaćam do" in data:
                print("Potraznja. Skipping.")
                return None
            return data
        except KeyError:
            print(KeyError)
            print(f"Real estate {rs_link} deleted. Skipping.")
            write_log_info(f"Real estate {rs_link} deleted. Skipping.")
        return None
