import requests

from random import randint
from time import sleep

from car_scraper.carScraper_v2 import CarScraper
from car_scraper.car import Car
# from db_server.sql_server import Server
from db_server.turso_server import Server
from utils.log_maker import write_log_error, write_log_info


def send_ntfy(msg):
    headers = {"Title":"Scraper crashed", "Tags": "warning, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)

car_scraper = CarScraper()


while True:
    try:
        car_scraper.get_cars_from_main()
        server = Server()
        new_ids = car_scraper.filter_new_cars(server)
        new_found = len(new_ids)

        # Make [id, link, 0] list to add to the server
        add_ids = [[car_id, car_scraper.cars[car_id], 0] for car_id in new_ids]
        server.add_car_links(add_ids, write_log_info)
        
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

        pause_between_cars = randint(10,20)
        possible_fit = min(allocated_time // pause_between_cars, len(not_scraped))
        time_left = max(allocated_time - total_not_scraped * pause_between_cars, 0)

        print(f"Found {new_found} new cars. Left to scrape {len(not_scraped)}.")
        print(f"Will scrape {possible_fit} cars for {allocated_time} seconds.")
        print(f"Cars to scrape {not_scraped[:possible_fit]}")
        for car in not_scraped[:possible_fit]:
            sleep(pause_between_cars)
            car_id = car[0]
            car_link = car[1]
            print(f"Scraping {car_link}.")
            data = car_scraper.scrape_car(car_id, car_link, write_log_info)
            print("Got data")
            server = Server()
            if data:
                new_car = Car(data)
                server.insert_car_data(new_car.data, write_log_info, write_log_error)
                print(f"Car {car_id} scraped.")
            else:
                print(f"Car {car_id} not scraped, skipping and marking as scraped.")
            server.mark_as_scraped("links_cars", car_id)
        print(f"Cars scraped. Waiting for {time_left} seconds.")
    except Exception as e:
        print(f"Got exception - {e}")
        write_log_error(f"{e}.")
    else:
        print("Car scraper in else.")
        sleep(time_left)
    finally:
        print("Car scraper in finally.")
        sleep(randint(20, 30))
