from turso_server import Server

server = Server()

data = {'id': 60377629, 'datum': '2024-04-18', 'ime': 'Stan Bihac 93m2', 'cijena': 2800, 'stanje': 'koristeno', 'vrsta_oglasa': 'prodaja', 'broj_soba': 3, 'kvadrata': 93, 'namjesten': 0, 'sprat': '4', 'vrsta_grijanja': 'Ostalo', 'kvadratura_balkona': 88, 'adresa': '501 slavne brigade 57', 'vrsta_poda': 'Ostalo', 'lokacija': 'Bihac', 'lat': 44.8075, 'lng': 15.8708, 'kompanija': 0, 'broj_pregleda': '', 'datum_objave': '2024-04-18', 'obnovljen': '2024-04-18'}

server.insert_rs_data("Stan", data)

