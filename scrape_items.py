from notifier.notifier import send_ntfy

from item_scrapers.tropicScraper import TropicScraper
from db_server.sql_server import Server


server = Server()
tropic_scraper = TropicScraper()

total_new = 0
total_inserted = 0

try:
    tropic_scraper.get_html()
    tropic_scraper.scrape_items()
    new_items, items_inserted = tropic_scraper.add_items_to_database(server, "tropic")
    total_new += new_items
    total_inserted += items_inserted
except Exception as e:
    print(e)
    print("Tropic scraper failed")

send_ntfy(msg=f"Found {total_new} new items. {total_inserted} items scraped.", title="Tropic scraper", tags=["shopping_cart"])
