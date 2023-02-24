import re
import json
import sys
from bs4 import BeautifulSoup
from datetime import datetime, date

sys.path.append('../')

from carScraper_v2 import CarScraper

car_soup = BeautifulSoup(open("car1.html", "r", encoding="utf-8"), "html.parser")
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

    
    # We are only scraping sell ads
    data["Vrsta oglasa"] = "Prodaja"

    # Get the type of seller
    seller_p = car_soup.find('p', {'class': 'user-info__title pb-md'})
    shop = 1 if seller_p.get_text().strip() == "OLX shop" else 0
    data['radnja'] = shop

    pattern_date = r'date:(\d+)'
    dates = re.findall(pattern_date, str(car_soup))
    # Convert epoch to yyyy-mm-dd
    date_ob = datetime.fromtimestamp(int(dates[0]))
    date_str = date_ob.strftime('%Y-%m-%d')
    data['Datum objave'] = date_str

    return data

data = get_car_data(car_soup)

print(data)