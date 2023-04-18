from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_webpage_source(url):
    # Configure the Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (optional)
    chrome_options.add_argument('--no-sandbox')
    # Set the user agent
    user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/"
    chrome_options.add_argument(f'user-agent={user_agent}')


    # Bingbott user agent
    # Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)

    # Replace 'chromedriver' with the path to the chromedriver if needed
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

    # Replace 'https://www.example.com' with the URL of the webpage you want to get
    url = 'https://www.konzumshop.ba/#!/categories/5471171/mlijecni-jaja-i-sir?show=all&sort_field=soldStatistics&sort=soldStatisticsDesc&max_price=45&page=1&per_page=200'
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.title.mb_s.ng-scope')))

    # Get the webpage source
    page_source = driver.page_source

    # Close the browser
    driver.quit()

# Parse the webpage source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
print(soup)

# Find all the links with the specified class and print their titles
links = soup.find_all('a', class_='title mb_s ng-scope')
for link in links:
    print(link.get_text())
