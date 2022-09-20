import requests

from random import randint
from time import sleep

from carScraper import CarScraper
from car_scraper.car import Car
from db_server.sql_server import Server
from utils.log_maker import write_log_error


def send_ntfy(msg):
    headers = {"Title":"Scraper crashed", "Tags": "warning, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)

server = Server()
car_scraper = CarScraper()


while True:
    try:
        car_scraper.get_cars_from_main()
        new_found = car_scraper.filter_new_cars()

        not_scraped = server.get_non_scraped_cars()
        total_not_scraped = len(not_scraped)

        if new_found > 25:
            allocated_time = randint(200,250)
        elif new_found > 15:
            allocated_time = randint(400,500)
        elif new_found > 5:
            allocated_time = randint(600, 800)
        else:
            allocated_time = randint(1000, 1200)

        pause_between_cars = randint(20,40)
        possible_fit = min(allocated_time // pause_between_cars, len(not_scraped))
        time_left = max(allocated_time - total_not_scraped * pause_between_cars, 0)

        print(f"Found {new_found} new cars. Left to scrape {len(not_scraped)}.")
        print(f"Will scrape {possible_fit} cars for {allocated_time} seconds.")
        for car in not_scraped[:possible_fit]:
            car_id = car[0]
            car_link = car[1]
            print(f"Scraping {car_link}.")
            data = car_scraper.scrape_car(car_id, car_link)
            if data:
                new_car = Car(data)
                server.insert_car_data(new_car.data)
            server.mark_as_scraped("links_cars", car_id)
            sleep(pause_between_cars)
        print(f"Cars scraped. Waiting for {time_left} seconds.")
    except Exception as e:
        send_ntfy(str(e))
        write_log_error(f"{e}.")
    else:
        sleep(time_left)
    finally:
        sleep(randint(20, 30))
