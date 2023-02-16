import os
import logging

ROOT = os.path.dirname(__file__)
LOG_FILE = os.path.join(ROOT, "../logs/car_scraper.log")

logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


def write_log_info(msg):
    logging.info(msg)

def write_log_error(msg):
    logging.error(msg)

def get_last_20_lines():
    with open(LOG_FILE, 'r') as logfile:
        last_20 = "".join(logfile.readlines()[-20:])
    return last_20
