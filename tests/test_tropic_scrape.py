import json

from tropic_scrape.tropicScraper import TropicScraper



def get_test_data(item_type):
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[item_type]


def get_test_html(item_type):
    with open(f"htmls/{item_type}.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


def test_scrape():
    item_types = ["tropic_fruits_and_vegetables", "tropic_dairy_eggs"]
    scraper = TropicScraper()

    for item_type in item_types:
        scraper.items = []
        scraper.htmls = {item_type: [get_test_html(item_type)]}
        scraper.scrape_items()

        # Extract scraped data to test format
        scraped_items = {}
        for item in scraper.items:
            scraped_items[item["name"]] = [item["price"], item["unit"]]
        assert scraped_items == get_test_data(item_type)


