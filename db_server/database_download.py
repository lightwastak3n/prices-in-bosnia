from sql_server import Server

server = Server()

records = server.get_records_on_date("cars", "datum", "2023-05-20")
for record in records:
    print(record)