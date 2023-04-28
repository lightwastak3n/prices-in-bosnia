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
    sleep(10)

server = Server()
real_estate_scraper = RealEstateScraper()


while True:
    try:
        real_estate_scraper.get_real_estates_from_main()
        new_houses, new_flats, new_lands = real_estate_scraper.filter_new_real_estates(server)
        new_found = len(new_houses) + len(new_flats) + len(new_lands)

        print("Scraped main rs pages. And checked for new listings.")
        # Make [id, link, type, 0] list to add to the server
        add_houses = [[house_id, f"https://olx.ba/artikal/{house_id}/", "Kuca", 0] for house_id in new_houses]
        add_flats = [[flat_id, f"https://olx.ba/artikal/{flat_id}/", "Stan", 0] for flat_id in new_flats]
        add_lands = [[land_id, f"https://olx.ba/artikal/{land_id}/", "Zemljiste", 0] for land_id in new_lands]
        

        server.add_rs_links(add_houses, write_log_info)
        server.add_rs_links(add_flats, write_log_info)
        server.add_rs_links(add_lands, write_log_info)
        print("Added new listings to the server.")
        not_scraped = server.get_non_scraped_rs()
        total_not_scraped = len(not_scraped)
        print("Got the non scraped listings from the server.")

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
            sleep(pause_between_items)
            rs_id = item[0]
            rs_link = item[1]
            rs_type = item[2]
            print(f"Scraping {rs_link}.")
            data = real_estate_scraper.scrape_real_estate(rs_id, rs_link, rs_type, write_log_info)
            if data:
                new_rs = RealEstate(data, rs_type)
                server.insert_rs_data(rs_type, new_rs.data, write_log_info, write_log_error)
                print(f"Rs {rs_id} scraped and inserted into the database.")
            server.mark_as_scraped("rs_links", rs_id)
        print(f"Rs scraped. Waiting for {time_left} seconds.")
    except Exception as e:
        print(e)
        send_ntfy(str(f"{e}"))
        write_log_error(f"{e}.")
    else:
        sleep(time_left)
    finally:
        sleep(randint(30, 40))