import sys

sys.path.append('../')
from carScraper_v2 import CarScraper
from bs4 import BeautifulSoup


with open('main_car_page.html', 'r', encoding='utf-8') as mcp:
    main_car_page = mcp.read()

soup = BeautifulSoup(main_car_page, 'html.parser')

scraper = CarScraper()
scraper.main_page = soup
# scraper.get_cars_from_main()

# print(scraper.cars)



all_links = scraper.main_page.select('a[href*="artikal"]')

for link in all_links[:20]:
    car_name = link.find('h1').text.strip()
    link_loc = link["href"]
    correct_link = f"https://olx.ba{link_loc}"   
    car_id = link_loc.split("/")[-2]
    print(car_id)
    print(correct_link)
    print("="*50)