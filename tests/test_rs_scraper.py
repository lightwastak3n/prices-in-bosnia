import json

from bs4 import BeautifulSoup

from real_estate_scraper.rsScraper import RealEstateScraper
from real_estate_scraper.real_estate import RealEstate


def get_main_page_test_data(item_type):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[item_type]


def get_item_data(item):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    item_data = data[item]
    for prop in list(item_data):
        if item_data[prop] == "None":
            del item_data[prop]
    return item_data


def get_page_soup(html_file):
    with open(f"htmls/{html_file}.html", 'r', encoding='utf-8') as mcp:
        main_listing_page = mcp.read()
    soup = BeautifulSoup(main_listing_page, 'html.parser')
    return soup


def scrape_item(item_id, item_html_name, rs_type):
    test_item_data = get_item_data(item_html_name)

    scraper = RealEstateScraper()
    listing_id = item_id
    listing_soup = get_page_soup(item_html_name)

    listing_data = scraper.get_real_estate_details(listing_soup, listing_id, rs_type)
    new_listing = RealEstate(listing_data, rs_type)

    # Fix for test data ints since we are comparing them against strings
    for name in new_listing.data:
        if isinstance(new_listing.data[name], str) and new_listing.data[name].isdigit():
            new_listing.data[name] = int(new_listing.data[name])
    # Fix todays date
    new_listing.data["datum"] = test_item_data["datum"]

    return new_listing, test_item_data


def test_main_page_scrape():    
    scraper = RealEstateScraper()
    scraper.main_pages["Stan"] = get_page_soup("flats")
    scraper.main_pages["Kuca"] = get_page_soup("houses")
    scraper.main_pages["Zemljiste"] = get_page_soup("land")

    
    scraper.get_real_estates_from_main(get_main_pages=False)
    
    test_houses = get_main_page_test_data('houses')
    test_lands = get_main_page_test_data('land')
    test_flats = get_main_page_test_data('flats')

    assert scraper.real_estates["Stan"] == test_flats
    assert scraper.real_estates["Kuca"] == test_houses
    assert scraper.real_estates["Zemljiste"] == test_lands


def test_land_scrape():
    new_land, test_land_data = scrape_item(53070662, "land1", "Zemljiste")
    assert new_land.data == test_land_data


def test_flat_scrape():
    new_flat, test_flat_data = scrape_item(48894962, "flat1", "Stan")
    assert new_flat.data == test_flat_data


def test_house_scrape():
    new_house, test_house_data = scrape_item(51868032, "house1", "Kuca")
    assert new_house.data == test_house_data
