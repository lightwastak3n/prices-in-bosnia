from notifier.notifier import send_ntfy

from item_scrapers.tropicScraper import TropicScraper
from db_server.sql_server import Server


server = Server()
scraper = TropicScraper()

scraper.get_html()
scraper.scrape_items()
new_items, items_inserted = scraper.add_items_to_database(server)
send_ntfy(msg=f"Found {new_items} new items. {items_inserted} items scraped.", title="Tropic scraper", tags=["shopping_cart"])
