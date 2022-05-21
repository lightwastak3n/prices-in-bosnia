from database_handler import get_missing_seller_cars, update_seller_info
from get_new_cars import get_page as get_car_soup
from random import randint
from time import sleep


def create_missing_list(missing_cars):
    with open("missing_seller_info.txt", "w") as missing_info:
        for car_id, link in missing_cars:
            missing_info.write(f"{car_id},{link}\n")


def create_list_from_db():
    missing_cars = get_missing_seller_cars()
    create_missing_list(missing_cars)


def get_updated_missing_list():
    updated_missing_list = []
    with open("missing_seller_info.txt", "r") as missing_info:
        missing_cars = missing_info.read().split("\n")
        missing_cars.pop()
        for info in missing_cars:
            car_id, link = info.split(",")
            updated_missing_list.append((car_id, link))
    return updated_missing_list


def find_seller_info(car_id, link):        
    soup = get_car_soup(link)
    if "Artikal je izbrisan od strane prodavca" in str(soup):
        return f"{link} - car deleted"
    if soup.findAll("div", {"class": "povjerenje_mmradnja"}):
        val = 1
    else:
        val = 0
    update_seller_info(car_id, val)
    return f"seller info updated with {val} - {link}"


def main(allocated_time):
    cars_data = get_updated_missing_list()
    pause = randint(30,40)
    cutoff = allocated_time // pause
    cars_to_fix = min(len(cars_data), cutoff)
    for i in range(cars_to_fix):
        car_id, link = cars_data.pop()
        print(find_seller_info(car_id, link))
        sleep(pause)
    # Update the list with finished cars (write file again)
    create_missing_list(cars_data)
