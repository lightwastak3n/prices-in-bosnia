import csv
from db_server.sql_server import Server


headers = [
    "id",
    "ime",
    "lokacija",
    "stanje",
    "proizvodjac",
    "model",
    "godiste",
    "kilometraza",
    "vrata",
    "gorivo",
    "kubikaza",
    "kilovata",
    "konjskih_snaga",
    "emisioni_standard",
    "registrovan",
    "udaren",
    "broj_pregleda",
    "datum",
    "datum_objave",
    "radnja",
    "cijena",
    "link"
    ]

server = Server()

data = server.get_cars_basic_info()

with open("car_data.csv", 'w') as car_data:
    writer = csv.writer(car_data, delimiter=";")
    writer.writerow(headers)

    for row in data[:]:
        car = list(row)
        dtime = car[-4]
        date = dtime.split(" u ")[0]
        day = date[:2]
        month = date[3:5]
        year = date[6:10]
        car[-4] = f"{year}-{month}-{day}"
        writer.writerow(car)
