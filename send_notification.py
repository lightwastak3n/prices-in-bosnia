#!/usr/bin/python3
import requests

from db_server.sql_server import Server


def send_ntfy(msg):
    headers = {"Title":"Scraper report", "Tags": "page_facing_up, houses, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)


if __name__ == "__main__":
    server = Server()
    msg1 = server.get_stats()
    send_ntfy(f"{msg1}")
