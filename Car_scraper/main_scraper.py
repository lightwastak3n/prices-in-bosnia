import requests
import get_new_cars
import car_scraper
import fix_seller_info

from time import sleep
from random import randint


def send_ntfy(msg):
    headers = {"Title":"Scraper crashed", "Tags": "warning, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)


while True:
    try:
        new_cars = get_new_cars.main()
        print(f"Found {new_cars} new cars.")
        if new_cars > 25:
            allocated_time = randint(200,300)
        elif new_cars > 15:
            allocated_time = randint(400,500)
        elif new_cars > 5:
            allocated_time = randint(600, 800)
        else:
            allocated_time = randint(1000, 1200)
        print(f"Will scrape individual cars for {allocated_time} seconds.")
        time_left = car_scraper.main(allocated_time)
        print(f"Finished scraping cars. Time left {time_left}. Waiting to fetch new cars.")
        sleep(time_left)
    except Exception as e:
        send_ntfy(str(e))
    finally:
        sleep(randint(20,30))

