import requests
import re

from datetime import date
from bs4 import BeautifulSoup

from db_server.sql_server import Server
from utils.log_maker import write_log_info
from car_scraper.columns_names import specs_columns_mapping


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
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
        response = requests.get(url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
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
        match = re.search(r"results:\s*\[[^[\]]*(?:\[[^[\]]*\][^[\]]*)*\](?=,?\s*attributes)", target_script, re.DOTALL)
        results = match.group(0)
        car_ids = re.findall(r'(?<=,id:)\d+,', results)
        for id in car_ids:
            self.cars[id[:-1]] = f"https://olx.ba/artikal/{id[:-1]}/"

    def filter_new_cars(self) -> int:
        """
        Checks id of each car found against the ids already present in the database.

        Returns:
            Total number of new cars found.
        """
        server = Server()
        server.create_connection()
        total = 0
        for id, link in self.cars.items():
            if not server.item_in_db("links_cars", id):
                server.add_car_link(id, link, 0)
                total += 1
        server.close_connection()
        return total
    
    # Fix for akcijska cijena 
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

    def get_car_specs_v2(self, car_soup, car_id):
        """
        Gets all the specs it can found on a given car page.
        Name is found manually as h2 tag. Everything else shares the same tag so it can be done in a loop.
        There are also some fixes for the price.

        Args:
            car_soup: soup object (like a raw html) generated from the cars webpage
            car_id: id of the car found
        """
        name = car_soup.find("h2")
        name = name.text.strip()
        data = {"id": car_id, "Ime": name, "datum": f"{date.today()}"}

        boolean_properties = [
            "Metalik",
            "Turbo",
            "Start-Stop sistem",
            "DPF/FAP filter",
            "Park assist",
            "Strane tablice",
            "Registrovan",
            "Ocarinjen",
            "Na lizingu",
            "Prilagođen invalidima",
            "Servisna knjiga",
            "Servo volan",
            "Komande na volanu",
            "Tempomat",
            "ABS",
            "ESP",
            "Airbag",
            "El. podizači stakala",
            "Električni retrovizori",
            "Senzor mrtvog ugla",
            "Klima",
            "Digitalna klima",
            "Navigacija",
            "Touch screen (ekran)",
            "Šiber",
            "Panorama krov",
            "Naslon za ruku",
            "Koža",
            "Hlađenje sjedišta",
            "Masaža sjedišta",
            "Grijanje sjedišta",
            "El. pomjeranje sjedišta",
            "Memorija sjedišta",
            "Senzor auto. svjetla",
            "Alu felge",
            "Alarm",
            "Centralna brava",
            "Daljinsko otključavanje",
            "Oldtimer",
            "Auto kuka",
            "ISOFIX",
            "Udaren",
        ]
        # Find the script tag that contains all the data about the car
        all_scripts = car_soup.findAll("script")
        for script in all_scripts:
            if script.contents and "window.__NUXT__" in script.contents[0][:50]:
                target_script = script.contents[0]
                break
        # Extract section with all the data
        match = re.search(r"data:\s*\[[^[\]]*(?:\[[^[\]]*\][^[\]]*)*\](?=,?\s*fetch)", target_script, re.DOTALL)
        results = match.group(0)
        match2 = re.search(r"attributes:(.*?)(?=model_id:)", results, re.DOTALL)
        attr = match2.group(0)

        return data


    def get_car_specs(self, car_soup, car_id):
        """
        Gets all the specs it can found on a given car page.
        Name is found manually as h1 tag. Everything else shares the same tag so it can be done in a loop.
        There are also some fixes for the price.

        Args:
            car_soup: soup object (like a raw html) generated from the cars webpage
            car_id: id of the car found
        """
        name = car_soup.find("h2")
        name = name.text.strip()
        data = {"id": car_id, "Ime": name, "datum": f"{date.today()}"}

        # Checking if its a shop
        data['radnja'] = 1 if car_soup.findAll("div", {"class": "povjerenje_mmradnja"}) else 0

        basic_info = car_soup.findAll("p", {"class": "n"})
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
        elif "Hitna prodaja" in data:
            data["Cijena"] = data["Hitna prodaja"]
            del data["Hitna prodaja"]
        elif "Akcijska cijena - " in str(car_soup) and data.get('Cijena') == None:
            self.akcijska_cijena(car_soup, data)
            
        if "Cijena" in data and data["Cijena"] == "Po dogovoru":
            data["Cijena"] = "0"

        # Extra info
        extra_keys = car_soup.findAll("div", {"class": "df1"})
        for key in extra_keys:
            value = key.find_next_sibling("div")
            value = value.text.strip()
            if not value:
                value = 1
            key = key.text.strip()
            if key not in data:
                data[key] = value
        if "OLX ID" in data:
            del data["OLX ID"]
        return data

    def scrape_car(self, car_id, car_link) -> dict:
        """
        Scrapes individual car.

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
