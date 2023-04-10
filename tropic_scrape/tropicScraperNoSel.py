import requests
import time

from bs4 import BeautifulSoup

LINKS = [
    "https://eshop.tropic.ba/product-category/voce-i-povrce/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/mlijeko-mlijecni-proizvodi-jaja/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/licna-higijena/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/svjeze-meso/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/pekarski-proizvodi/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/osnovne-zivotne-namirnice/?orderby=popularity"
]

link_class = "woocommerce-LoopProduct-link woocommerce-loop-product__link"
name_class = "woocommerce-loop-product__title"
unit_class = "woocommerce-Price-currencySymbol amount mcmp-recalc-price-suffix"
price_class = "woocommerce-Price-amount amount"


html = requests.get(LINKS[0]).content
soup = BeautifulSoup(html, 'html.parser')

# Find all links with the specified class
links = soup.find_all('a', class_=link_class)

items = []

for link in links:
    # Find the item name, price, and unit within each link
    name = link.find('h2', class_=name_class).text.strip().lower()
    price = link.find('span', class_=price_class).find('bdi').text.strip("KM")
    unit = link.find('span', class_=unit_class).text.strip("/")

    # Store the extracted data in a dictionary
    item = {
        'name': name,
        'price': price,
        'unit': unit
    }
    
    items.append(item)

# Print the extracted items
for item in items:
    print(f"Name: {item['name']}, Price: {item['price']}, Unit: {item['unit']}")


