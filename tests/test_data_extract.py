import re
import json
import sys
from bs4 import BeautifulSoup

sys.path.append('../')

from carScraper_v2 import CarScraper

car_soup = BeautifulSoup(open("car1_backup.html", "r", encoding="utf-8"), "html.parser")

# Find the script tag that contains all the data about the car
all_scripts = car_soup.findAll("script")
for script in all_scripts:
    if script.contents and "window.__NUXT__" in script.contents[0][:50]:
        target_script = script.contents[0]
        break


match = re.search(r"data:\s*\[[^[\]]*(?:\[[^[\]]*\][^[\]]*)*\](?=,?\s*fetch)", target_script, re.DOTALL)
results = match.group(0)


match2 = re.search(r"attributes:(.*?)(?=model_id:)", results, re.DOTALL)
attr = match2.group(0)
attr = attr[:-1]

data = json.loads(attr)
print(data)

# attr = attr.split("\n")
