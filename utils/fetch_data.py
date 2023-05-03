import json
from db_server.sql_server import Server


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

server = Server()
data = server.get_records_on_date("item_prices", "date", "2023-05-01")
for item in data:
    item[3] = str(item[3])

print(data)
write_json(data, "test.json")