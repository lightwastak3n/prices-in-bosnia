import csv
from db_server.sql_server import Server


def write_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


server = Server()
data = server.get_records_on_date("item_prices", "date", "2023-05-01")
for item in data:
    item[3] = str(item[3])

write_csv(data, "test.json")