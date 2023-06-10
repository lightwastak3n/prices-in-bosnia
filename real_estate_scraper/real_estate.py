columns = {"Stan":
           {
            "id": "id",
            "Ime": "ime",
            "datum": "datum",
            "Cijena": "cijena",
            "Stanje": "stanje",
            "Lokacija": "lokacija",
            "lat": "lat",
            "lng": "lng",
            "Kvadrata": "kvadrata",
            "Broj soba": "broj_soba",
            "Sprat": "sprat",
            "kompanija": "kompanija",
            "Vrsta grijanja": "vrsta_grijanja",
            "Namješten": "namjesten",
            "Namješten?": "namjesten",
            "Kanalizacija": "kanalizacija",
            "Parking": "parking",
            "Struja": "struja",
            "Uknjiženo / ZK": "uknjizeno",
            "Voda": "voda",
            "Vrsta oglasa": "vrsta_oglasa",
            "Datum objave": "datum_objave",
            "Broj pregleda": "broj_pregleda",
            "Balkon": "balkon",
            "Blindirana vrata": "blindirana_vrata",
            "Internet": "internet",
            "Kablovska TV": "kablovska",
            "Nedavno adaptiran": "nedavno_adaptiran",
            "Plin": "plin",
            "Podrum/Tavan": "podrum",
            "Uključen trošak režija": "rezije",
            "Adresa": "adresa",
            "Godina izgradnje": "godina_izgradnje",
            "Vrsta poda": "vrsta_poda",
            "Primarna orjentacija": "primarna_orijentacija",
            "Klima": "klima",
            "Lift": "lift",
            "Telefonski priključak": "telefon",
            "Video nadzor": "video_nadzor",
            "Za studente": "za_studente",
            "Kvadratura balkona": "kvadratura_balkona",
            "Ostava/Špajz": "ostava",
            "Ostava/špajz": "ostava",
            "Kućni ljubimci": "kucni_ljubimci",
            "Novogradnja": "novogradnja",
            "Alarm": "alarm",
            "Garaža": "garaza",
            "Obnovljen": "obnovljen",
           },
           "Kuca":
           {
            "id": "id",
            "Ime": "ime",
            "datum": "datum",
            "Cijena": "cijena",
            "Stanje": "stanje",
            "Lokacija": "lokacija",
            "lat": "lat",
            "lng": "lng",
            "Kvadrata": "kvadrata",
            "Broj soba": "broj_soba",
            "Broj spratova": "broj_spratova",
            "kompanija": "kompanija",
            "Vrsta grijanja": "vrsta_grijanja",
            "Okućnica (kvadratura)": "okucnica_kvadratura",
            "Vrsta poda": "vrsta_poda",
            "Balkon": "balkon",
            "Iznajmljeno": "iznajmljeno",
            "Kablovska TV": "kablovska",
            "Ostava/Špajz": "ostava",
            "Ostava/špajz": "ostava",
            "Parking": "parking",
            "Podrum/Tavan": "podrum",
            "Struja": "struja",
            "Uknjiženo / ZK": "uknjizeno",
            "Voda": "voda",
            "Vrsta oglasa": "vrsta_oglasa",
            "Datum objave": "datum_objave",
            "Broj pregleda": "broj_pregleda",
            "Kanalizacija": "kanalizacija",
            "Alarm": "alarm",
            "Blindirana vrata": "blindirana_vrata",
            "Garaža": "garaza",
            "Internet": "internet",
            "Klima": "klima",
            "Namještena": "namjestena",
            "Nedavno adaptirana": "nedavno_adaptirana",
            "Plin": "plin",
            "Telefonski priključak": "telefon",
            "Video nadzor": "video_nadzor",
            "Adresa": "adresa",
            "Godina izgradnje": "godina_izgradnje",
            "Primarna orjentacija": "primarna_orijentacija",
            "Bazen": "bazen",
            "Obnovljen": "obnovljen",
           },
           "Zemljiste":
           {
            "id": "id",
            "Ime": "ime",
            "datum": "datum",
            "Cijena": "cijena",
            "Stanje": "stanje",
            "Lokacija": "lokacija",
            "lat": "lat",
            "lng": "lng",
            "Prilaz": "prilaz",
            "Kvadrata": "kvadrata",
            "kompanija": "kompanija",
            "Komunalni priključak": "komunalni_prikljucak",
            "Uknjiženo (ZK)": "uknjizeno",
            "Vrsta oglasa": "vrsta_oglasa",
            "Datum objave": "datum_objave",
            "Broj pregleda": "broj_pregleda",
            "Udaljenost od rijeke (m)": "udaljenost_rijeka",
            "Građevinska dozvola": "gradjevinska_dozvola",
            "Urbanistička dozvola": "urbanisticka_dozvola",
            "Iznajmljeno": "iznajmljeno",
            "Obnovljen": "obnovljen",
            }
           }

radio_columns = [
    "struja",
    "voda",
    "balkon",
    "kablovska",
    "ostava",
    "parking",
    "podrum",
    "uknjizeno",
    "alarm",
    "blindirana_vrata",
    "garaza",
    "internet",
    "klima",
    "nedavno_adaptirana",
    "plin",
    "telefon",
    "video_nadzor",
    "bazen",
    "gradjevinska_dozvola",
    "urbanisticka_dozvola",
    "komunalni_prikljucak",
    "iznajmljeno",
    "lift",
    "za_studente",
    "kucni_ljubimci",
    "novogradnja",
    "nedavno_adaptiran",
    "rezije",
    "kanalizacija",
    "namjesten",
    "namjestena"
]


class RealEstate:
    """
    Represents a single real estate. It takes the data scraped by the rsScraper and then cleans it.

    Attributes:
        data: Properties of a real estate that are found on its webpage.
    """
    def __init__(self, data, type):
        """
        Initializes real estate object and cleans the data.
        """
        self.data = data
        self.type = type
        self.rename_columns()
        self.fix_price_and_area()
        self.fix_int_cols()

        self.fix_number_of_floors()
        self.fix_number_of_rooms()
        self.fix_namjesten()

        self.fix_radio_columns()
        self.fix_serbian_letters()

    def rename_columns(self):
        """
        Changes the names of the keys (real estate attributes) in self.data.
        The original names are as found on olx so we rename them to something easier to work with.
        """
        new_data = {}
        for spec in self.data:
            print(f"Trying to rename {spec}")
            new_data[columns[self.type][spec]] = self.data[spec]
        self.data = new_data

    def fix_price_and_area(self):
        """
        Fixes price, cleans the integer.
        """
        # self.data["cijena"] = self.data["cijena"].rstrip(" KM").replace(".", "")
        # if "," in self.data["cijena"]:
        #     self.data["cijena"] = self.data["cijena"].split(",")[0]
        if self.type == 'Zemljiste' and 'stanje' in self.data:
            del self.data['stanje']
        if 'kvadrata' in self.data:
            self.data['kvadrata'] = self.fix_int(self.data['kvadrata'])

    def fix_int(self, num):
        num = str(num)
        num = num.replace('.', "")
        num = num.replace('m2', "")
        num = num.replace('²', "")
        if ',' in num:
            num = num.split(',')[0]
        num = "".join(filter(str.isdigit, num))
        if num == "":
            num = 0
        num = int(num)
        return num
            

    def fix_int_cols(self):
        """
        Yeah I dont even
        """
        if "udaljenost_rijeka" in self.data:
            self.data["udaljenost_rijeka"] = self.fix_int(self.data["udaljenost_rijeka"])
        if "kvadratura_balkona" in self.data:
            self.data["kvadratura_balkona"] = self.fix_int(self.data["kvadratura_balkona"])
        if "okucnica_kvadratura" in self.data:
            self.data["okucnica_kvadratura"] = self.fix_int(self.data["okucnica_kvadratura"])
    
    def fix_number_of_rooms(self):
        """
        Room number should be int for a house and we can give it values for a apartment
        """
        if 'broj_soba' in self.data and self.data['broj_soba'] == '8+':
            self.data['broj_soba'] = 8
        if self.type == 'Stan' and 'broj_soba' in self.data:
            name_room = {
                'Garsonjera': 0,
                'Jednosoban (1)': 1,
                'Jednoiposoban (1.5)': 1.5,
                'Dvosoban (2)': 2,
                'Trosoban (3)': 3,
                'Četverosoban (4)': 4,
                'Petosoban i više': 5,
                '1': 1,
                '2': 2,
                '3': 3,
                '4': 4,
                '5': 5
            }
            self.data["broj_soba"] = name_room[self.data["broj_soba"]]
    
    def fix_number_of_floors(self):
        if self.type == "Kuca":
            if "broj_spratova" in self.data and self.data["broj_spratova"] == "5+":
                self.data["broj_spratova"] = 5

    def fix_namjesten(self):
        if self.type == "Stan":
            namjesten_mapping = {"Namješten": 2, "Nenamješten": 0, "Polunamješten": 1, "Namje&scaron;ten": 2, 1: 2}
            if "namjesten" in self.data:
                self.data["namjesten"] = namjesten_mapping[self.data["namjesten"]]


    def fix_radio_columns(self):
        """
        Fix for a ~40 columns that should be radio buttons but for some reason can be Da Ne.
        Not sure if this still applies to the new olx.
        """
        for col in radio_columns:
            if col in self.data:
                if self.data[col] == "Da":
                    self.data[col] = 1
                elif self.data[col] == "Ne":
                    self.data[col] = 0

    def fix_serbian_letters(self):
        """Remove lettes š, đ, č, ć, ž from the values in data"""
        latin_chars = {
            "š": "s",
            "đ": "dj",
            "č": "c",
            "ć": "c",
            "ž": "z"
        }
        # Add capital letters also
        latin_chars.update({key.upper(): value.upper() for key, value in latin_chars.items()})
        latin_chars["Đ"] = "Dj"
        for key in self.data:
            if isinstance(self.data[key], str):
                self.data[key] = ''.join(latin_chars.get(char, char) for char in self.data[key])
