import csv

from car import Car
from real_estate_scraper.real_estate_server import Server
from columns_names import specs_columns_mapping


def data_cleaner(data):
        if "velicina_felgi" in data and (data["velicina_felgi"] == "Ostalo" or data["velicina_felgi"] == ""):
            data["velicina_felgi"] = None
        if data['godiste'] == None or data['godiste'] == "Starije" or int(data['godiste']) < 1950:
            data['godiste'] = 0
        if data['kilovata'] != None and not data['kilovata'].isnumeric():
            try:
                data['kilovata'] = int("".join(filter(str.isdigit, data['kilovata'])))
                data['kilovata'] = min(10000, data['kilovata'])
            except ValueError:
                data['kilovata'] = None
        if data['konjskih_snaga'] != None and not data['konjskih_snaga'].isnumeric():
            try:
                data['konjskih_snaga'] = int("".join(filter(str.isdigit, data['konjskih_snaga'])))
            except ValueError:
                data['konjskih_snaga'] = None
        if 'prva_registracija' in data and data['prva_registracija'] == "Starije":
            data['prva_registracija'] = None
        if 'prethodnih_vlasnika' in data and  data['prethodnih_vlasnika'] == "Ostalo":
            data['prethodnih_vlasnika'] = None
        radio_columns = list(specs_columns_mapping.values())[36:77]
        radio_columns.append("metalik")
        for col in radio_columns:
            if col in data:
                if data[col] == "Da":
                    data[col] = 1
                elif data[col] == "Ne":
                    data[col] = 0
        return data

def build_data_dict(columns, line):
    data = {}
    for i in range(len(columns)):
        if line[i] != "":
            data[columns[i]] = line[i]
        else:
            data[columns[i]] = None
    return data


all_cars = []

with open("cars.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter="|")
    for line in reader:
        if 'kilometraza' in line:
            columns = line
        else:
            raw_data = build_data_dict(columns, line)
            all_cars.append(raw_data)


srv = Server()
srv.create_connection()

i = 89001
placeholders = ", ".join(["%s"] * len(columns))
columns = ", ".join(columns)
sql = f"INSERT INTO cars ({columns}) VALUES ({placeholders})"
vals = []
for data in all_cars[89001:]:
    data = data_cleaner(data)
    to_insert = tuple(data.values())
    vals.append(to_insert)
    if i % 1 == 0:
        with srv.connection.cursor() as cursor:
            cursor.executemany(sql, vals)
            srv.connection.commit()
        vals = []
        print(i)
        print(data['id'])
    i += 1
