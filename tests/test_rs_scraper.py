import sys
import os
import json

from bs4 import BeautifulSoup

from real_estate_scraper.rsScraper import RealEstateScraper
from real_estate_scraper.real_estate import RealEstate


def get_main_page_test_data(type):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[type]


def get_item_data(item):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    car_data = data[item]
    for prop in list(car_data):
        if car_data[prop] == "None":
            del car_data[prop]
    return car_data


def get_main_page_soup(type):
    with open(f"htmls/{type}.html", 'r', encoding='utf-8') as mcp:
        main_listing_page = mcp.read()
    soup = BeautifulSoup(main_listing_page, 'html.parser')
    return soup


def test_main_page_scrape():    
    scraper = RealEstateScraper()
    scraper.main_pages["Stan"] = get_main_page_soup("apartments")
    scraper.main_pages["Kuca"] = get_main_page_soup("houses")
    scraper.main_pages["Zemljiste"] = get_main_page_soup("land")

    
    scraper.get_real_estates_from_main(get_main_pages=False)
    
    test_houses = get_main_page_test_data('houses')
    test_lands = get_main_page_test_data('land')
    test_apartments = get_main_page_test_data('apartments')

    assert scraper.real_estates["Stan"] == test_apartments
    assert scraper.real_estates["Kuca"] == test_houses
    assert scraper.real_estates["Zemljiste"] == test_lands

