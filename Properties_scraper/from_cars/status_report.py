#!/usr/bin/python3
import requests
import os
from database_handler import get_stats

CURRENT_FOLDER = os.path.dirname(__file__)
CARS_TO_FIX = os.path.join(CURRENT_FOLDER, "missing_seller_info.txt")


def number_of_files_to_fix():
    with open(CARS_TO_FIX, 'r') as cars_to_fix:
        total = sum(1 for _ in cars_to_fix)
    return total

def send_ntfy(msg):
    headers = {"Title":"Scraper report", "Tags": "page_facing_up, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)


if __name__ == "__main__":
    msg1 = get_stats()
    # Fixed all cars no need for this anymore
    # msg2 = f"Cars left to fix {number_of_files_to_fix()}."
    send_ntfy(f"{msg1}")
