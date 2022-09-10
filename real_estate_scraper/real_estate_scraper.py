import requests

from datetime import date
from bs4 import BeautifulSoup

# from real_estate_server import Server
# from log_maker import write_log_info

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
        self.MAIN_URL = "https://www.olx.ba/nekretnine"
        self.main_page = None
        self.real_estates = {}

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
        Gets the html of the MAIN_URL and stores it in main_page object attribute
        """
        self.main_page = self.get_soup(self.MAIN_URL)
    
    def get_real_estate_from_main(self):
        """
        Gets all the links found under div class: "naslov".
        Each link corressponds to a real estate.
        The links are stored in self.real_estate attribute.
        """
        self.get_main_page()
        first_divs = self.main_page.findAll("div", {'class': 'artikal imaHover-disabled otvorimodal obicniArtikal g p'})
        second_divs = self.main_page.findAll("div", {'class': 'artikal h imaHover-disabled otvorimodal obicniArtikal g p'})
        listing_divs = [*first_divs, *second_divs]
        for listing in listing_divs:
            link_tag = listing.find("a")
            link = link_tag.get("href")
            real_id = link.split("/")[4]
            self.real_estates[real_id] = link

    def filter_new_real_estates(self) -> int:
        """
        Checks id of each real estate found against the ids already present in the database.

        Returns:
            Total number of new real estate found.
        """
        server = Server()
        server.create_connection()
        total = 0
        for id, link in self.real_estates.items():
            if not server.car_in_db(id):
                server.add_link(id, link, 0)
                total += 1
        server.close_connection()
        return total
    
    def get_real_estate_details(self, real_estate_soup, real_estate_id):
        """
        Gets all the specs it can found on a given real estate page.
        Name is found manually as h1 tag. Everything else shares the same tag so it can be done in a loop.

        Args:
            real_estate_soup: soup object (like a raw html) generated from the real estate webpage
            real_estate_id: id of the real estate found

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        name = real_estate_soup.find("h1")
        name = name.text.strip()
        data = {"id": real_estate_id, "Ime": name, "datum": f"{date.today()}"}
        basic_info = real_estate_soup.findAll("p", {"class": "n"})
        for i in basic_info:
            key = i.text.strip()
            value_p = i.find_next_sibling("p")
            value = value_p.text.strip()
            data[key] = value
        extra_keys = real_estate_soup.findAll("div", {"class": "df1"})
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

    def scrape_real_estate(self, real_estate_id, real_estate_link) -> dict:
        """
        Scrapes individual real_estate.

        Args:
            car_id: id of a given car.
            car_link: Link of the cars webpage.

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        real_estate_soup = self.get_soup(real_estate_link)
        try:
            data = self.get_car_specs(real_estate_soup, real_estate_id)
            return data
        except KeyError:
            print(f"Car {real_estate_link} deleted. Skipping.")
            write_log_info(f"Car {real_estate_link} deleted. Skipping.")
        return None


scraper = RealEstateScraper()
# scraper.get_real_estate_from_main()

# print(scraper.real_estates)
test_izdavanje = "https://www.olx.ba/artikal/39240777/stan-na-dan-banja-luka-centar-kod-meriot-coutyard/"
test_prodaja = "https://www.olx.ba/artikal/48691676/total-pro-dvosoban-stan-56-m2-grbavica/"

test_soup = scraper.get_soup(test_prodaja)
test_id = 39240777
data = scraper.get_real_estate_details(test_soup, test_id)
for key, value in data.items():
    print(f"{key} - {value}")
