import sys
import os
import json

from bs4 import BeautifulSoup

from car_scraper.carScraper_v2 import CarScraper
from car_scraper.car import Car



def get_main_page_data():
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["cars"]


def get_car_data(car):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    car_data = data[car]
    for prop in list(car_data):
        if car_data[prop] == "None":
            del car_data[prop]
    return car_data


def test_get_cars_from_main():
    with open('htmls/car_listing_page.html', 'r', encoding='utf-8') as mcp:
        main_car_page = mcp.read()
    soup = BeautifulSoup(main_car_page, 'html.parser')

    scraper = CarScraper()
    scraper.main_page = soup
    scraper.get_cars_from_main(request_main_page=False)
    test_cars = get_main_page_data()
    assert scraper.cars == test_cars


def test_car_scrape():
    for car in ["car1", "car2"]:
        with open(f"htmls/{car}.html", 'r', encoding='utf-8') as car_html:
            car_page = car_html.read()
        car_soup = BeautifulSoup(car_page, 'html.parser')

        test_car_data = get_car_data(car)

        scraper = CarScraper()
        car_id = test_car_data["id"]
        

        car_data = scraper.get_car_specs(car_soup, car_id)
        new_car = Car(car_data)

        # Fix for date since scraper automatically uses todays date
        new_car.data["datum"] = test_car_data["datum"]

        # Fix for test data ints since we are comparing them against strings
        for name in new_car.data:
            if isinstance(new_car.data[name], str) and new_car.data[name].isdigit():
                new_car.data[name] = int(new_car.data[name])
        assert new_car.data == test_car_data
