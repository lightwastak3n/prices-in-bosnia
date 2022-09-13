import requests

from random import randint
from time import sleep
from threading import Thread

from carScraper import CarScraper
from car_scraper.car import Car
from rsScraper import RealEstateScraper
from real_estate_scraper.real_estate import RealEstate
from db_server.sql_server import Server
from utils.log_maker import write_log_error


def send_ntfy(msg):
    headers = {"Title":"Scraper crashed", "Tags": "warning, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)

server = Server()
car_scraper = CarScraper()
real_estate_scraper = RealEstateScraper()


def scrape_cars():
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


def scrape_real_estates():
    while True:
        try:
            real_estate_scraper.get_real_estates_from_main()
            new_found = real_estate_scraper.filter_new_real_estates()

            not_scraped = server.get_non_scraped_rs()
            total_not_scraped = len(not_scraped)

            if new_found > 40:
                allocated_time = randint(200,300)
            elif new_found > 25:
                allocated_time = randint(400,500)
            elif new_found > 10:
                allocated_time = randint(600, 800)
            else:
                allocated_time = randint(1000, 1200)

            pause_between_items = randint(20,40)
            possible_fit = min(allocated_time // pause_between_items, len(not_scraped))
            time_left = max(allocated_time - total_not_scraped * pause_between_items, 0)

            print(f"Found {new_found} new items. Left to scrape {len(not_scraped)}.")
            print(f"Will scrape {possible_fit} real estate for {allocated_time} seconds.")
            for item in not_scraped[:possible_fit]:
                rs_id = item[0]
                rs_link = item[1]
                type = item[2]
                print(f"Scraping {rs_link}.")
                try:
                    data = real_estate_scraper.scrape_real_estate(rs_id, rs_link)
                    if data:
                        new_rs = RealEstate(data, type)
                        server.insert_rs_data(type, new_rs.data)
                except Exception as e:
                    print(f"{e}. Invalid listing.")
                finally:
                    server.mark_as_scraped("rs_links", rs_id)
                sleep(pause_between_items)
            print(f"Rs scraped. Waiting for {time_left} seconds.")
        except Exception as e:
            print(e, rs_link)
            send_ntfy(str(f"{e} - {rs_link}"))
            write_log_error(f"{e}.")
        else:
            sleep(time_left)
        finally:
            sleep(randint(30, 40))


t1 = Thread(target=scrape_cars)
t2 = Thread(target=scrape_real_estates)

t1.start()
t2.start()

