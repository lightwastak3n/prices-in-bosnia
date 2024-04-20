#!/usr/bin/python3
import requests
import json
from db_server.sql_server import Server as MySQLServer
from db_server.turso_server import Server as TursoServer


def send_ntfy(msg):
    headers = {"Title": "Scraper report", "Tags": "page_facing_up, houses, car"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)


def send_stats_mysql():
    server = MySQLServer()
    msg1 = server.get_stats()
    send_ntfy(f"{msg1}")


def send_stats_turso():
    server = TursoServer()
    data = server.get_totals()
    print("Got data for sendind", data)
    msg = f"Cars: {data[0][1]}\nHouses: {data[0][2]}\nFlats: {data[0][3]}\nLand: {data[0][4]}\nItems: {data[0][5]}\n"
    send_ntfy(f"{msg}")


if __name__ == "__main__":
    send_stats_turso()
