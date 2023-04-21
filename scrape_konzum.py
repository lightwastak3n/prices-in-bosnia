from time import sleep
from notifier.notifier import send_ntfy

from item_scrapers.konzumScraper import KonzumScraper
from db_server.sql_server import Server


server = Server()
konzum_scraper = KonzumScraper()
total_new = 0
total_inserted = 0


category_links = {
    "meat": "https://www.konzumshop.ba/#!/categories/5471538/meso?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    "bakery products": "https://www.konzumshop.ba/#!/categories/5471486/pekarski-proizvodi?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    "fruits and vegetables": "https://www.konzumshop.ba/#!/categories/5471582/svjeze-voce-i-povrce?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    "dairy and eggs": "https://www.konzumshop.ba/#!/categories/5471171/mlijecni-jaja-i-sir?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    "household supplies": "https://www.konzumshop.ba/#!/categories/5471675/kucanske-potrepstine?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    "personal hygiene": "https://www.konzumshop.ba/#!/categories/5471644/higijenski-i-papirnati-proizvodi?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
}
categories = list(category_links.keys())
urls = list(category_links.values())

i = 0
while i < len(urls):
    konzum_scraper.items = []
    url = urls[i]
    category = categories[i]
    try:
        konzum_scraper.get_html(url, category)
        konzum_scraper.scrape_items()
        new_items, items_inserted = konzum_scraper.add_items_to_database(server, 'konzum')
        total_new += new_items
        total_inserted += items_inserted
        print(f"Scraped {url} {category} and found {new_items} new and {items_inserted} total items.")
    except Exception as e:
        print(e)
        print("Error getting data for", category)
    finally:
        i += 1
        sleep(10)


send_ntfy(msg=f"Found {total_new} new items. {total_inserted} items scraped.", title="Konzum scraper", tags=["shopping_cart"])
