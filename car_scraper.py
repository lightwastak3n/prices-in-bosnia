import requests

from datetime import date
from bs4 import BeautifulSoup

from car_server import Server
from log_maker import write_log_info

class CarScraper:
    """
    Car scraper object that scrapes the main page and checks for new cars and also scrapes individual cars.

    Attributes:
            MAIN_URL: Url of the default location where vehicles are published.
            main_page: Stores raw html the MAIN_URL
            cars: Dictionary that stores id: link of the cars found on main page.
    """
    def __init__(self) -> None:
        """
        Initializes car scraper.
        """
        self.MAIN_URL = "https://www.olx.ba/pretraga?kategorija=18&id=1&stanje=0&vrstapregleda=tabela&sort_order=desc&sort_po=datum&od=100&vrsta=samoprodaja"
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
    
    def get_cars_from_main(self):
        """
        Gets all the links found under div class: "naslov".
        Each link corressponds to a car.
        The links are stored in self.cars attribute.
        """
        self.get_main_page()
        listing_divs = self.main_page.findAll("div", {'class': 'naslov'})
        for listing in listing_divs:
            link_tag = listing.find("a")
            try:
                link = link_tag.get("href")
                car_id = link.split("/")[4]
                self.cars[car_id] = link
            except AttributeError:
                print("Link not found. Empty listing bar.")
            except Exception as e:
                print(f"Unexpected error - {e}")
        
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
            if not server.car_in_db(id):
                server.add_link(id, link, 0)
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

    def get_car_specs(self, car_soup, car_id):
        """
        Gets all the specs it can found on a given car page.
        Name is found manually as h1 tag. Everything else shares the same tag so it can be done in a loop.
        There are also some fixes for the price.

        Args:
            car_soup: soup object (like a raw html) generated from the cars webpage
            car_id: id of the car found
        """
        name = car_soup.find("h1")
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