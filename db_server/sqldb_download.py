import csv

from time import sleep
from datetime import datetime, timedelta

from sql_server import Server


def generate_date_range(start_date, end_date) -> list:
    """
    Generates date range between two dates, including the start and end date.
    Returns a list of dates in format YYYY-MM-DD.

    Args:
        start_date: date string in format YYYY-MM-DD
        end_date: date string in format YYYY-MM-DD
    Returns:
        list of dates in the format YYYY-MM-DD
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = []
    for i in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        date_list.append(date)
    return date_list


def download_date_range_records(
    server, table, date_column, start_date, end_date
) -> list:
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
    dates = generate_date_range(start_date, end_date)

    for date in dates:
        print(f"Getting records for {date}")
        date_records = server.get_records_on_date(table, date_column, date)
        all_records.extend(date_records)
        sleep(1)
    return all_records


def download_date_range_items(server, start_date, end_date) -> list:
    """
    Downloads items for a given date range.

    Args:
        server: sql server object
        start_date: date string in format YYYY-MM-DD
        end_date: date string in format YYYY-MM-DD
    """
    columns = ["name", "type", "unit", "store", "price", "date"]
    all_records = [columns]
    dates = generate_date_range(start_date, end_date)
    for date in dates:
        print(f"Getting items for {date}")
        date_records = server.get_items_on_date(date)
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
