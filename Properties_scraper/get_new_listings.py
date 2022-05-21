import requests
import database_handler

from bs4 import BeautifulSoup


MAIN_URL = "https://www.olx.ba/pretraga?kategorija=18&id=1&stanje=0&vrstapregleda=tabela&sort_order=desc&sort_po=datum&od=100&vrsta=samoprodaja"

# Site seems to be blocking regular requests so use user agent
def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup


# Get all links that are under div class: "naslov"
# Add links with new ids to the database
def main():
    new_listings = 0
    soup = get_page(MAIN_URL)
    listing_divs = soup.findAll("div", {'class': 'naslov'})
    for listing in listing_divs:
        link_tag = listing.find("a")
        try:
            link = link_tag.get("href")
            listing_id = link.split("/")[4]
            if not database_handler.listing_in_db(listing_id):
                database_handler.add_link(listing_id, link, 0)
                new_listings += 1
        except AttributeError:
            print("Link not found. Empty listing bar.")
        except Exception as e:
            print(f"Unexpected error - {e}")
    return new_listings 
