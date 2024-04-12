import requests

from random import randint
from datetime import date
from time import sleep
from bs4 import BeautifulSoup


class TropicScraper:
    category_links = {
    "fruits and vegetables": "https://eshop.tropic.ba/product-category/voce-i-povrce/?orderby=popularity",
    "dairy and eggs": "https://eshop.tropic.ba/product-category/mlijeko-mlijecni-proizvodi-jaja/?orderby=popularity",
    "personal hygiene": "https://eshop.tropic.ba/product-category/licna-higijena/?orderby=popularity",
    "meat": "https://eshop.tropic.ba/product-category/svjeze-meso/?orderby=popularity",
    "bakery products": "https://eshop.tropic.ba/product-category/pekarski-proizvodi/?orderby=popularity",
    "basic groceries": "https://eshop.tropic.ba/product-category/osnovne-zivotne-namirnice/?orderby=popularity"
    }

    prop_classes = {
        "link": "woocommerce-LoopProduct-link woocommerce-loop-product__link",
        "name": "woocommerce-loop-product__title",
        "unit": "woocommerce-Price-currencySymbol amount mcmp-recalc-price-suffix",
        "price": "woocommerce-Price-amount amount"
    }

    def __init__(self):
        self.items = []
        self.htmls = {item_type: [] for item_type in self.category_links}

    def get_html(self):
        """ Gets the raw html of urls specified above. When testing we skip this step"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        get_nth_page = lambda n, link: link.split("?")[0] + "page/" + str(n) + "/?" + link.split("?")[1]
        for item_type in self.category_links:
            print("Getting html for", item_type)
            html = requests.get(self.category_links[item_type], headers=headers).content
            self.htmls[item_type].append(html)
            page_limit = 6 if item_type != "meat" else 4
            for page_number in range(2, page_limit):
                sleep(randint(30, 45))
                html = requests.get(get_nth_page(page_number, self.category_links[item_type])).content
                self.htmls[item_type].append(html)
            sleep(randint(30, 48))

    def fix_serbian_letters(self, text):
        latin_chars = {
            "š": "s",
            "đ": "dj",
            "č": "c",
            "ć": "c",
            "ž": "z"
        }
        text = text.strip()
        return ''.join(latin_chars.get(char, char) for char in text)

    def scrape_items(self):
        for item_type in self.htmls:
            print("Scraping", item_type)
            for html in self.htmls[item_type]:
                soup = BeautifulSoup(html, 'html.parser')

                # Find all links with the specified class
                links = soup.find_all('a', class_=self.prop_classes['link'])

                for item in links:
                    # Find the item name, price, and unit within each link
                    name = item.find('h2', class_=self.prop_classes['name']).text.strip().lower()
                    price = item.find('span', class_=self.prop_classes['price']).find('bdi').text.strip("KM")
                    if item.find('span', class_=self.prop_classes['unit']) is None:
                        unit = "unit"
                    else:
                        unit = item.find('span', class_=self.prop_classes['unit']).text.strip("/").lower()

                    # Store the extracted data in a dictionary
                    item = {
                        'name': self.fix_serbian_letters(name.strip()),
                        'price': float(price),
                        'unit': unit,
                        'type': item_type
                    }

                    self.items.append(item)

    def add_items_to_database(self, server, store):
        """
        Add new items to the items table in the database
        
        Args:
            server: The server object that handles the database connection
        """
        print("Adding items to database")
        today = date.today()
        new_items = server.check_if_items_exist(self.items, store)
        if not new_items:
            print("No new items")
        else:
            server.insert_items(new_items, store)
        server.insert_item_prices(self.items, store, today)
        return len(new_items), len(self.items)
