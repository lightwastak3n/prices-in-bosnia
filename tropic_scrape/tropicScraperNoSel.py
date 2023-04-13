import requests
from time import sleep

from bs4 import BeautifulSoup


class TropicScraper:
    category_links = {
    # "fruits and vegetables": "https://eshop.tropic.ba/product-category/voce-i-povrce/?orderby=popularity",
    "dairy": "https://eshop.tropic.ba/product-category/mlijeko-mlijecni-proizvodi-jaja/?orderby=popularity",
    "personal hygiene": "https://eshop.tropic.ba/product-category/licna-higijena/?orderby=popularity",
    "meat": "https://eshop.tropic.ba/product-category/svjeze-meso/?orderby=popularity",
    "bakery products": "https://eshop.tropic.ba/product-category/pekarski-proizvodi/?orderby=popularity",
    "basic groceries": "https://eshop.tropic.ba/product-category/osnovne-zivotne-namirnice/?orderby=popularity"
    }

    div_classes = {
        "link": "woocommerce-LoopProduct-link woocommerce-loop-product__link",
        "name": "woocommerce-loop-product__title",
        "unit": "woocommerce-Price-currencySymbol amount mcmp-recalc-price-suffix",
        "price": "woocommerce-Price-amount amount"
    }

    def __init__(self):
        self.items = []

    def scrape_items(self):
        for link in self.category_links.values():
            html = requests.get(link).content
            soup = BeautifulSoup(html, 'html.parser')

            # Find all links with the specified class
            links = soup.find_all('a', class_=self.div_classes['link'])


            for item in links:
                # Find the item name, price, and unit within each link
                name = item.find('h2', class_=self.div_classes['name']).text.strip().lower()
                price = item.find('span', class_=self.div_classes['price']).find('bdi').text.strip("KM")
                if item.find('span', class_=self.div_classes['unit']) is None:
                    unit = "unit"
                else:
                    unit = item.find('span', class_=self.div_classes['unit']).text.strip("/")

                # Store the extracted data in a dictionary
                item = {
                    'name': name,
                    'price': price,
                    'unit': unit
                }
    
                self.items.append(item)
            break

    # def filter_items(self, server):
    #     items_present = server.


scraper = TropicScraper()
scraper.scrape_items()
print(scraper.items)

