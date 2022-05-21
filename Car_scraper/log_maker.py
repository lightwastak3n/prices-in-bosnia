import os
import logging


ROOT = os.path.dirname(__file__)
LOG_FILE = os.path.join(ROOT, "scraper.log")


logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(message)s', level=logging.DEBUG)

def write_log(msg):
    logging.info(msg)
