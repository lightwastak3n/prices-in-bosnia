from tropicScraper import TropicScraper

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from time import sleep
from random import randint


class KonzumScraper(TropicScraper):
    category_links = {
            "meat": "https://www.konzumshop.ba/#!/categories/5471538/meso?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
            "bakery products": "https://www.konzumshop.ba/#!/categories/5471486/pekarski-proizvodi?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
            "fruits and vegetables": "https://www.konzumshop.ba/#!/categories/5471582/svjeze-voce-i-povrce?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
            "dairy and eggs": "https://www.konzumshop.ba/#!/categories/5471171/mlijecni-jaja-i-sir?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
            "household supplies": "https://www.konzumshop.ba/#!/categories/5471675/kucanske-potrepstine?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
            "personal hygiene": "https://www.konzumshop.ba/#!/categories/5471644/higijenski-i-papirnati-proizvodi?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&page=1&per_page=200",
    }

    def __init__(self):
        super().__init__()

    def get_webpage_source(self, url):
        # Configure the Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--no-sandbox') # For some reason doesnt work without this
        user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/"
        chrome_options.add_argument(f'user-agent={user_agent}')

        # Replace 'chromedriver' with the path to the chromedriver if needed
        driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

        driver.get(url)
                
        # Wait for the elements
        wait = WebDriverWait(driver, 20)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.title.mb_s.ng-scope')))

        # Get the webpage source and close the driver
        page_source = driver.page_source
        driver.quit()
        return page_source

    def get_html(self):
        for item_type in self.category_links:
            print("Getting html for", item_type)
            html = self.get_webpage_source(self.category_links[item_type])
            self.htmls[item_type].append(html)
            sleep(randint(45, 60))
    
    def scrape_items(self):
        for item_type in self.htmls:
            print("Scraping", item_type)
            # Parse the webpage source using BeautifulSoup
            soup = BeautifulSoup(self.htmls[item_type][0], 'html.parser')
            
            items = soup.find_all('div', class_='ng-scope')
            # Iterate over the items and extract the required properties
            for item in items:
                # Extract the name
                name_tag = item.find('a', class_='title mb_s ng-scope')
                name = name_tag.get_text().lower() if name_tag else None

                # Extract the price and unit
                price_tag = item.find('span', class_='price block ng-binding')
                if price_tag:
                    price = price_tag.get_text().split(' KM')[0].replace(',', '.')
                    unit = price_tag.get_text().split('/')[1].strip().lower()
                else:
                    price = None
                    unit = None

                # Check for alternative price and update the price variable if found
                alternative_price_tag = item.find('span', class_='fine clr_def ng-scope')
                if alternative_price_tag:
                    del_tag = alternative_price_tag.find('del', class_='ng-binding')
                    if del_tag:
                        price = del_tag.get_text().split(' KM')[0].replace(',', '.')
                        unit = del_tag.get_text().split('/')[1].strip().lower()
                if name != None:
                    if unit == "ko":
                        unit = "unit"
                    item = {
                        'name': self.fix_serbian_letters(name),
                        'price': float(price),
                        'unit': unit,
                        'type': item_type
                    }
                    self.items.append(item)




