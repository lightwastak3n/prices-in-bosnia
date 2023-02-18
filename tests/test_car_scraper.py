import sys
import json

from bs4 import BeautifulSoup

sys.path.append('../')
from carScraper_v2 import CarScraper


def get_main_page_data():
    with open("test_data.json", "r") as f:
        data = json.load(f)
    return data['cars']


def test_get_cars_from_main():    
    with open('car_listing_page.html', 'r', encoding='utf-8') as mcp:
        main_car_page = mcp.read()
    soup = BeautifulSoup(main_car_page, 'html.parser')

    scraper = CarScraper()
    scraper.main_page = soup
    scraper.get_cars_from_main(False)
    test_cars = get_main_page_data()
    assert scraper.cars == test_cars

