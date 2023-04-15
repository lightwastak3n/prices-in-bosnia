from tropic_scrape.tropicScraper import TropicScraper
from db_server.sql_server import Server


server = Server()
server.DATABASE = "test_database"
scraper = TropicScraper()


scraper.get_html()
scraper.scrape_items()
scraper.add_items_to_database(server)

