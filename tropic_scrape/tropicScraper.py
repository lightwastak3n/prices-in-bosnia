import requests
import time

from bs4 import BeautifulSoup

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC




LINKS = [
    "https://eshop.tropic.ba/product-category/voce-i-povrce/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/mlijeko-mlijecni-proizvodi-jaja/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/licna-higijena/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/svjeze-meso/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/pekarski-proizvodi/?orderby=popularity",
    "https://eshop.tropic.ba/product-category/osnovne-zivotne-namirnice/?orderby=popularity"
]




# Set up headless mode for Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize the webdriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Wait for the "load more" button to appear, adjust the timeout as needed
wait = WebDriverWait(driver, 10)

# You may need to update the CSS selector to match the "load more" button on your target website
load_more_button_selector = '.load-more-button'

while True:
    try:
        # Find the "load more" button and click it
        load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, load_more_button_selector)))
        load_more_button.click()
        time.sleep(7)  # Add a small delay to allow the new content to load
    except Exception as e:
        print("No more 'load more' buttons found or an error occurred.")
        break

# Get the page source and parse it using BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Close the browser window
driver.quit()

# Now, you can use BeautifulSoup to find and extract the data you need.
# Replace the CSS selector below with the appropriate one for the items you want to scrape.

