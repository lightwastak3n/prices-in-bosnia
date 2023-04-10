import requests
import re

from time import sleep
from random import randint
from datetime import date, datetime
from bs4 import BeautifulSoup


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
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Referer': 'https://bing.com/'}
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
            match = re.search(r"results:\s*\[[^[\]]*(?:\[[^[\]]*\][^[\]]*)*\](?=,?\s*attributes)", target_script, re.DOTALL)
            results = match.group(0)
            listings_ids = re.findall(r'(?<=,id:)\d+,', results)
            for id in listings_ids:
                self.real_estates[rs_type][id[:-1]] = f"https://olx.ba/artikal/{id[:-1]}/"

    def filter_new_real_estates(self, server) -> int:
        """
        Checks id of each real estate found against the ids already present in the database.

        Returns:
            Total number of new real estate found.
        """
        house_ids = list(self.real_estates['Kuca'])
        flat_ids = list(self.real_estates['Stan'])
        land_ids = list(self.real_estates['Zemljiste'])

        new_houses = server.items_not_in_db('rs_links', house_ids)
        new_flats = server.items_not_in_db('rs_links', flat_ids)
        new_lands = server.items_not_in_db('rs_links', land_ids)

        return new_houses, new_flats, new_lands

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
    
    def get_real_estate_details(self, rs_soup, rs_id, rs_type):
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
        name = rs_soup.find("h2")
        name = name.text.strip()
        data = {"id": rs_id, "Ime": name, "datum": f"{date.today()}"}

        price_span = rs_soup.find("span", {"class": "price-heading vat"})
        data["Cijena"] = price_span.text

        # Extracting table data
        rows = rs_soup.find_all('tr', {'data-v-fffe36e4': ''})
        for row in rows:
            name = row.find_all('td')[0].get_text().strip()
            value = row.find_all('td')[1].get_text().strip()
            if value == "✓":
                value = 1
            data[name] = value

        # Get the location, condition and relative time of ad renewal
        labels = rs_soup.find_all('label', {'class': 'btn-pill'})
        # Mapping since not all cars have all the labels
        label_mapping = {"M17": "Lokacija", "M7": "Stanje"}
        for label in labels:
            for key in label_mapping:
                if key in str(label):
                    # Fix for Obnovljen label included
                    data[label_mapping[key]] = label.get_text().strip()

        # Get the type of seller
        seller_p = rs_soup.find('p', {'class': 'user-info__title pb-md'})
        shop = 1 if seller_p.get_text().strip() == "OLX shop" else 0
        data['kompanija'] = shop


        # Regular expression pattern to extract latitude and longitude values
        pattern = r"location:{lat:(\d+\.\d+),lon:(\d+\.\d+)},feedbacks"

        # Find all matches of the pattern in the string and extract lat and lon from first match
        matches = re.findall(pattern, str(rs_soup))
        if len(matches) > 0:
            data['lat'] = round(float(matches[0][0]), 4)
            data['lng'] = round(float(matches[0][1]), 4)

        # FFS olx what the fuck is with these random properties
        # Deleting al these 
        if "Datum objave" in data:
            del data["Datum objave"]
        if "Vrsta opreme" in data:
            del data["Vrsta opreme"]
        if "Ime i broj licence agenta" in data:
            del data["Ime i broj licence agenta"]
        if "Broj posredničkog ugovora" in data:
            del data["Broj posredničkog ugovora"]

        # Delete stanje for land
        if rs_type == 'Zemljiste' and 'Stanje' in data:
            del data['Stanje']

        return data

    def scrape_real_estate(self, rs_id, rs_link, rs_type, write_log_info) -> dict:
        """
        Scrapes individual real_estate.

        Args:
            rs_id: id of a given real estate.
            rs_link: Link of the real estate's webpage.

        Returns:
            data: dictionary of properties and values found on a given listing
        """
        rs_soup = self.get_soup(rs_link)
        try:
            data = self.get_real_estate_details(rs_soup, rs_id, rs_type)
            if "Plaćam do" in data:
                print("Potraznja. Skipping.")
                return None
            return data
        except KeyError:
            print(f"Real estate {rs_link} deleted. Skipping.")
            write_log_info(f"Real estate {rs_link} deleted. Skipping.")
        return None
