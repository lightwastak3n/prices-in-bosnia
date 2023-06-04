import csv

from time import sleep
from datetime import datetime

from sql_server import Server


def date_range(server, table, date_column, start_date, end_date) -> list:
    """
    Downloads data for a given date range.

    Args:
        server: sql server object
        table: table name
        date_column: column name of the date column
        start_date: date string in format YYYY-MM-DD
        end_date: date string in format YYYY-MM-DD
    """
    all_records = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    delta = end_date - start_date
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        print(f"Getting records for {date}")
        date_records = server.get_records_on_date(table, date_column, date)
        all_records.extend(date_records)
        sleep(1)
    return all_records


def save_records_csv(records, file_name):
    """
    Saves records to csv file.

    Args:
        records: list of records
        file_name: name of the file
    """
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(records)
