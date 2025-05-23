specs_columns_mapping = {
"id": "id",
"Ime": "ime",
"Cijena": "cijena",
"Stanje": "stanje",
"Lokacija": "lokacija",
"Obnovljen": "obnovljen",
"Proizvođač": "proizvodjac",
"Model": "model",
"Godište": "godiste",
"Kilometraža": "kilometraza",
"Kilovata (KW)": "kilovata",
"Kubikaža": "kubikaza",
"Gorivo": "gorivo",
"Broj vrata": "vrata",
"Konjskih snaga": "konjskih_snaga",
"Metalik": "metalik",
"Masa/Težina (kg)": "masa",
"Tip": "tip",
"Pogon": "pogon",
"Emisioni standard": "emisioni_standard",
"Veličina felgi": "velicina_felgi",
"Transmisija": "transmisija",
"Broj stepeni prijenosa": "brzina",
"Boja": "boja",
"Muzika/ozvučenje": "ozvucenje",
"Parking senzori": "parking_senzori",
"Parking kamera": "parking_kamera",
"Registrovan do": "registrovan_do",
"Godina prve registracije": "prva_registracija",
"Broj prethodnih vlasnika": "prethodnih_vlasnika",
"Posjeduje gume": "gume",
"Višezonska klima": "visezonska_klima",
"Rolo zavjese": "rolo_zavjese",
"Svjetla": "svjetla",
"Zaštita/Blokada": "zastita_blokada",
"Sjedećih mjesta": "sjedecih_mjesta",
"Turbo": "turbo",
"Start-Stop sistem": "start_stop_sistem",
"DPF/FAP filter": "dpf_fap_filter",
"Park assist": "park_assist",
"Strane tablice": "strane_tablice",
"Registrovan": "registrovan",
"Ocarinjen": "ocarinjen",
"Na lizingu": "na_lizingu",
"Prilagođen invalidima": "prilagodjen_invalidima",
"Servisna knjiga": "servisna_knjiga",
"Servo volan": "servo_volan",
"Komande na volanu": "komande_na_volanu",
"Tempomat": "tempomat",
"ABS": "abs",
"ESP": "esp",
"Airbag": "airbag",
"El. podizači stakala": "el_podizaci_stakala",
"Električni retrovizori": "elektricni_retrovizori",
"Senzor mrtvog ugla": "senzor_mrtvog_ugla",
"Klima": "klima",
"Digitalna klima": "digitalna_klima",
"Navigacija": "navigacija",
"Touch screen (ekran)": "touch_screen",
"Šiber": "siber",
"Panorama krov": "panorama_krov",
"Naslon za ruku": "naslon_za_ruku",
"Koža": "koza",
"Hlađenje sjedišta": "hladjenje_sjedista",
"Masaža sjedišta": "masaza_sjedista",
"Grijanje sjedišta": "grijanje_sjedista",
"El. pomjeranje sjedišta": "el_pomjeranje_sjedista",
"Memorija sjedišta": "memorija_sjedista",
"Senzor auto. svjetla": "senzor_auto_svjetla",
"Alu felge": "alu_felge",
"Alarm": "alarm",
"Centralna brava": "centralna_brava",
"Daljinsko otključavanje": "daljinsko_otkljucavanje",
"Oldtimer": "oldtimer",
"Auto kuka": "auto_kuka",
"ISOFIX": "isofix",
"Udaren": "udaren",
"Vrsta oglasa": "vrsta_oglasa",
"Datum objave": "datum_objave",
"Broj pregleda": "broj_pregleda",
"radnja": "radnja",
"datum": "datum"
}


class Car:
    """
    Represents a single car. It takes the data scraped by the CarScraper and then cleans it.

    Attributes:
        data: Properties of a car that are found on its webpage.
    """
    def __init__(self, data):
        """
        Initializes Car object and cleans the data.
        """
        self.data = data
        print("cleaning keys")
        self.clean_dict_keys()
        print("renaming columns")
        self.rename_columns()
        print("fixing basic data")
        self.fix_basic_data()
        print("fixing year")
        self.fix_year()
        print("fixing power")
        self.fix_power()
        self.fix_first_registration()
        self.fix_radio_columns()
        self.fix_serbian_letters()
        
    def clean_dict_keys(self):
        """
        Removes the keys that arent present in specs_columns_mapping
        """
        clean_data = {}
        for key in self.data:
            if key in specs_columns_mapping:
                clean_data[key] = self.data[key]
        self.data = clean_data

    def rename_columns(self):
        """
        Changes the names of the keys (car attributes) in self.data.
        The original names are as found on olx so we rename them to something easier to work with.
        """
        new_data = {}
        for spec in self.data:
            if spec in specs_columns_mapping:
                new_data[specs_columns_mapping[spec]] = self.data[spec]
            else:
                del self.data[spec]
        self.data = new_data

    def fix_basic_data(self):
        """
        Fixes price, mileage, doors and rim size such that they are clean numbers.
        """
        if 'kilometraza' in self.data:
            self.data['kilometraza'] = str(self.data['kilometraza'])
            if "," in self.data['kilometraza']:
                self.data['kilometraza'] = self.data['kilometraza'].split(',')[0]
            self.data['kilometraza'] = self.data['kilometraza'].replace('km', "")
            self.data['kilometraza'] = int(self.data["kilometraza"].replace(".",""))
        if 'vrata' in self.data:
            self.data['vrata'] = self.data['vrata'].split("/")[0]
        if 'velicina_felgi' in self.data and (self.data['velicina_felgi'] == 'Ostalo' or self.data['velicina_felgi'] == ""):
            del self.data['velicina_felgi']

    def fix_year(self):
        """
        Fix for the people listing 2000 years old cars and 'Starije'.
        """
        if 'godiste' not in self.data or self.data['godiste'] == 'Starije' or int(self.data['godiste']) < 1950:
            self.data['godiste'] = 0

    def fix_power(self):
        """
        Tries to change power (kW and PS) to an int if possible. If not changes them to None.
        """
        if 'kilovata' in self.data and type(self.data['kilovata']) == float:
            self.data['kilovata'] = int(self.data['kilovata'])
        if 'konjskih_snaga' in self.data and type(self.data['konjskih_snaga']) == float:
            self.data['konjskih_snaga'] = int(self.data['konjskih_snaga'])

    def fix_first_registration(self):
        """
        Fixes first registration and number of previous owners.
        """
        if 'prva_registracija' in self.data and self.data['prva_registracija'] == "Starije":
            del self.data['prva_registracija']
        if 'prethodnih_vlasnika' in self.data and self.data['prethodnih_vlasnika'] == "Ostalo":
            del self.data['prethodnih_vlasnika']

    def fix_radio_columns(self):
        """
        Fix for a ~40 columns that should be radio buttons but for some reason can be Da Ne.
        """
        radio_columns = list(specs_columns_mapping.values())[36:77]
        radio_columns.append('metalik')
        for col in radio_columns:
            if col in self.data:
                if self.data[col] == 'Da':
                    self.data[col] = 1
                elif self.data[col] == 'Ne':
                    self.data[col] = 0

    def fix_serbian_letters(self):
        """Remove letters š, đ, č, ć, ž from the values in data"""
        latin_chars = {
            'š': 's',
            'đ': 'dj',
            'č': 'c',
            'ć': 'c',
            'ž': 'z'
        }
        # Add capital letters also
        latin_chars.update({key.upper(): value.upper() for key, value in latin_chars.items()})
        latin_chars['Đ'] = 'Dj'
        for key in self.data:
            if isinstance(self.data[key], str):
                self.data[key] = ''.join(latin_chars.get(char, char) for char in self.data[key])
