import requests
import re

from datetime import datetime, date
from bs4 import BeautifulSoup


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
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Referer': 'https://bing.com/'}
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

    def filter_new_cars(self, server) -> list:
        """
        Checks id of each car found against the ids already present in the database and returns the new ones.

        Returns:
            new_ids: List of all the new ids found
        """
        ids = list(self.cars)
        new_ids = server.items_not_in_db("links_cars", ids)
        return new_ids
    
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
        name = car_soup.find("h2")
        name = name.text.strip()
        data = {"id": car_id, "Ime": name, "datum": f"{date.today()}"}

        price_span = car_soup.find("span", {"class": "price-heading vat"})
        data["Cijena"] = price_span.text

        # Extracting table data
        rows = car_soup.find_all('tr', {'data-v-fffe36e4': ''})
        for row in rows:
            name = row.find_all('td')[0].get_text().strip()
            value = row.find_all('td')[1].get_text().strip()
            if value == "✓":
                value = 1
            data[name] = value
    
        # Get the location, condition and relative time of ad renewal
        labels = car_soup.find_all('label', {'class': 'btn-pill'})
        # Mapping since not all cars have all the labels
        label_mapping = {"M17": "Lokacija", "M7": "Stanje"}
        for label in labels:
            for key in label_mapping:
                if key in str(label):
                    # Fix for Obnovljen label included
                    data[label_mapping[key]] = label.get_text().strip()

        # We are only scraping sell ads
        data["Vrsta oglasa"] = "Prodaja"

        # Get the type of seller
        seller_p = car_soup.find('p', {'class': 'user-info__title pb-md'})
        shop = 1 if seller_p.get_text().strip() == "OLX shop" else 0
        data['radnja'] = shop

        return data

    def scrape_car(self, car_id, car_link, write_log_info) -> dict:
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
