import re
import json
import sys
from bs4 import BeautifulSoup

sys.path.append('../')

from carScraper_v2 import CarScraper

car_soup = BeautifulSoup(open("car1_backup.html", "r", encoding="utf-8"), "html.parser")
car_id = 51829903
name = "VW TIGUAN 4MOTION 2.0 TDI 2012 god."


def get_car_data(car_soup):
    name = car_soup.find("h2")
    name = name.text.strip()
    data = {"id": car_id, "Ime": name, "datum": "2023-02-15"}

    price_span = car_soup.find("span", {"class": "price-heading vat"})
    data["Cijena"] = price_span.text

    # pattern = r'value:(("[^"]*")|(c|\d)),name:"([^"]*)"'
    pattern = r'value:([^,]*),name:"([^"]*)"'

    # Extract all the name and value pairs from the string
    matches = re.findall(pattern, str(car_soup))

    # Create a dictionary with values and names
    for value, name in matches:
        value = value.strip('"')
        name = name.strip('"')
        if value == "c":
            value = 1
        elif "\\u002F" in value:
            value = value.replace("\\u002F", "/")
        if "\\u002F" in name:
            name = name.replace("\\u002F", "/")
        # data[name] = value

    # New way to get data - gets some that regex doesnt get
    rows = car_soup.find_all('tr', {'data-v-fffe36e4': ''})
    for row in rows:
        name = row.find_all('td')[0].get_text().strip()
        value = row.find_all('td')[1].get_text().strip()
        if value == "✓":
            value = 1
        data[name] = value

    # Get the location, condition, time the ad was renewed
    labels = car_soup.find_all('label', {'class': 'btn-pill'})
    location = labels[0].get_text().strip()
    condition = labels[1].get_text().strip()
    data['Lokacija'] = location
    data['Stanje'] = condition
    data 
    print(labels[2])
    
    # We are only scraping sell ads
    data["Vrsta oglasa"] = "Prodaja"

    return data

data = get_car_data(car_soup)
print(data)
