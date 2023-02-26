import requests

from random import randint
from time import sleep

from real_estate_scraper.rsScraper import RealEstateScraper
from real_estate_scraper.real_estate import RealEstate
from db_server.sql_server import Server
from utils.log_maker import write_log_error, write_log_info


def send_ntfy(msg):
    headers = {"Title":"Scraper crashed", "Tags": "warning, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)

server = Server()
real_estate_scraper = RealEstateScraper()


while True:
    try:
        real_estate_scraper.get_real_estates_from_main()
        new_houses, new_flats, new_lands = real_estate_scraper.filter_new_real_estates(server)
        new_found = len(new_houses) + len(new_flats) + len(new_lands)

        # Make [id, link, 0] list to add to the server
        add_houses = [[house_id, f"https://olx.ba/artikal/{house_id}/", "Kuca", 0] for house_id in new_houses]
        add_flats = [[flat_id, f"https://olx.ba/artikal/{flat_id}/", "Stan", 0] for flat_id in new_flats]
        add_lands = [[land_id, f"https://olx.ba/artikal/{land_id}/", "Zemljiste", 0] for land_id in new_lands]

        server.add_car_links(add_houses, write_log_info)
        server.add_car_links(add_flats, write_log_info)
        server.add_car_links(add_lands, write_log_info)

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

