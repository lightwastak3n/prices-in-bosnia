import requests

from time import sleep
from random import randint
from datetime import date
from bs4 import BeautifulSoup

from db_server.sql_server import Server
from utils.log_maker import write_log_info

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
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
        response = requests.get(url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def get_main_pages(self):
        """
        Gets the html of the 3 urls defined in __init__ and stores them in main_pages dict object attribute.
        """
        self.main_pages["Stan"] = self.get_soup(self.STANOVI_URL)
        sleep(randint(5,10))
        self.main_pages["Kuca"] = self.get_soup(self.KUCE_URL)
        sleep(randint(5,10))
        self.main_pages["Zemljiste"] = self.get_soup(self.ZEMLJISTA_URL)
    
    def get_real_estates_from_main(self):
        """
        Gets all the links found under div class: "naslov".
        Each link corressponds to a real estate.
        The links are stored in self.real_estate attribute.
        """
        self.get_main_pages()
        for type in self.main_pages:
            soup = self.main_pages[type]

            listing_divs = soup.findAll("div", {'class': 'naslov'})
            for listing in listing_divs:
                link_tag = listing.find("a")
                try:
                    link = link_tag.get("href")
                    rs_id = link.split("/")[4]
                    self.real_estates[type][rs_id] = link
                except AttributeError:
                    print("Link not found. Empty listing bar.")
                except Exception as e:
                    print(f"Unexpected error - {e}")

    def filter_new_real_estates(self) -> int:
        """
        Checks id of each real estate found against the ids already present in the database.

        Returns:
            Total number of new real estate found.
        """
        server = Server()
        server.create_connection()
        total = 0
        for type in self.real_estates:
            for id, link in self.real_estates[type].items():
                if not server.item_in_db("rs_links", id):
                    server.add_rs_link(id, link, type, 0)
                    total += 1
        server.close_connection()
        return total

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
        Gets all the specs it can found on a given real estate page.
        Name is found manually as h1 tag. Everything else shares the same tag so it can be done in a loop.

        Args:
            real_estate_soup: soup object (like a raw html) generated from the real estate webpage
            real_estate_id: id of the real estate found

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        name = rs_soup.find("h1")
        name = name.text.strip()
        data = {"id": rs_id, "Ime": name, "datum": f"{date.today()}"}

        # Checking if its a company
        data['kompanija'] = 1 if rs_soup.findAll("div", {"class": "povjerenje_mmradnja"}) else 0

        basic_info = rs_soup.findAll("p", {"class": "n"})
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
        elif "Akcijska cijena - " in str(rs_soup) and data.get('Cijena') == None:
            self.akcijska_cijena(rs_soup, data)
        elif "Hitno" in data:
            data["Cijena"] = data["Hitno"]
            del data["Hitno"]
            
        if "Cijena" in data and data["Cijena"] == "Po dogovoru":
            data["Cijena"] = "0"

        extra_keys = rs_soup.findAll("div", {"class": "df1"})
        for key in extra_keys:
            value = key.find_next_sibling("div")
            value = value.text.strip()
            if not value:
                value = 1
            key = key.text.strip()
            if key not in data:
                data[key] = value

        scripts = rs_soup.findAll("script")
        for script in scripts:
            if "google.maps.LatLng" in script.text:
                goal_script = script.text
                lat_long = goal_script.split("center: new google.maps.LatLng(")[1].split(")")[0]
                data["lat"], data["lng"] = lat_long.split(", ")
        del data["OLX ID"]
        del data["Obnovljen"]
        return data

    def scrape_real_estate(self, rs_id, rs_link) -> dict:
        """
        Scrapes individual real_estate.

        Args:
            rs_id: id of a given real estate.
            rs_link: Link of the real estate's webpage.

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        real_estate_soup = self.get_soup(rs_link)
        try:
            data = self.get_real_estate_details(real_estate_soup, rs_id)
            if "Plaćam do" in data:
                print("Potraznja. Skipping.")
                return None
            return data
        except KeyError:
            print(f"Real estate {rs_link} deleted. Skipping.")
            write_log_info(f"Real estate {rs_link} deleted. Skipping.")
        return None
