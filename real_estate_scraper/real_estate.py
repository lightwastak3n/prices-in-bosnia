columns = {
    "id": "id",
    "Ime": "ime",
    "datum": "date",
    "Cijena": "cijena",
    "Stanje": "stanje",
    "Lokacija": "lokacija",
    "Kuhinja": "kuhinja",
    "WC / Kupatilo": "kupatilo",
    "lat": "lat",
    "lng": "lng",
    "Kvadrata": "kvadrata",
    "Kvadratura": "kvadrata",
    "Broj soba": "broj_soba",
    "Sprat": "sprat",
    "kompanija": "kompanija",
    "Vrsta grijanja": "vrsta_grijanja",
    "Namješten": "namjesten",
    "Namješten?": "namjesten",
    "Namještena": "namjesten",
    "Opremljenost": "namjesten",
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
    "Kvadratura balkona": "kvadratura_balkona",
    "Kućni ljubimci": "kucni_ljubimci",
    "Novogradnja": "novogradnja",
    "Alarm": "alarm",
    "Garaža": "garaza",
    "Broj spratova": "broj_spratova",
    "Okućnica (kvadratura)": "okucnica_kvadratura",
    "Iznajmljeno": "iznajmljeno",
    "Nedavno adaptirana": "nedavno_adaptiran",
    "Bazen": "bazen",
    "Prilaz": "prilaz",
    "Komunalni priključak": "komunalni_prikljucak",
    "Uknjiženo (ZK)": "uknjizeno",
    "Udaljenost od rijeke (m)": "udaljenost_rijeka",
    "Građevinska dozvola": "gradjevinska_dozvola",
    "Urbanistička dozvola": "urbanisticka_dozvola",
    "TV": "TV",
}

radio_columns = [
    "struja",
    "voda",
    "balkon",
    "kablovska",
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
    "kucni_ljubimci",
    "novogradnja",
    "nedavno_adaptiran",
    "rezije",
    "kanalizacija",
    "namjesten",
    "namjestena",
]


class RealEstate:
    """
    Represents a single real estate. It takes the data scraped by the rsScraper and then cleans it.

    Attributes:
        data: Properties of a real estate that are found on its webpage.
    """

    def __init__(self, data, rs_type):
        """
        Initializes real estate object and cleans the data.
        """
        self.data = data
        self.type = rs_type
        self.clean_dict_keys()
        self.rename_columns()
        self.fix_name()
        self.fix_price_and_area()
        self.fix_int_cols()
        self.fix_number_of_floors()
        self.fix_number_of_rooms()
        self.fix_namjesten()

        self.fix_radio_columns()
        self.fix_serbian_letters()

    def clean_dict_keys(self):
        """
        Removes the keys that arent present in specs_columns_mapping
        """
        clean_data = {}
        for key in self.data:
            if key in columns and self.data[key] != None:
                clean_data[key] = self.data[key]
        self.data = clean_data

    def rename_columns(self):
        """
        Changes the names of the keys (real estate attributes) in self.data.
        The original names are as found on olx so we rename them to something easier to work with.
        """
        new_data = {}
        for spec in self.data:
            new_data[columns[spec]] = self.data[spec]
        self.data = new_data

    def fix_name(self):
        abc = "ABCČĆDDŽĐEFGHIJKLLJMNNJOPRSŠTUVZŽ"
        allowed = abc + abc.lower() + "0123456789" + " ,wyq"
        name = self.data["ime"]
        for char in self.data["ime"]:
            if char not in allowed:
                name = name.replace(char, "")
        self.data["ime"] = name

    def fix_price_and_area(self):
        """
        Fixes price, cleans the integer.
        """
        if self.type == "Zemljiste" and "stanje" in self.data:
            del self.data["stanje"]
        if "kvadrata" in self.data:
            self.data["kvadrata"] = self.fix_int(self.data["kvadrata"])

    def fix_int(self, num):
        num = str(num)
        num = num.replace(".", "")
        num = num.replace("m2", "")
        num = num.replace("²", "")
        if "," in num:
            num = num.split(",")[0]
        num = "".join(filter(str.isdigit, num))
        if num == "":
            num = 0
        num = int(num)
        return num

    def fix_number_of_rooms(self):
        """
        Room number should be int for a house and we can give it values for a apartment
        """
        if "broj_soba" in self.data:
            name_room = {
                "Garsonjera": 0,
                "Jednosoban (1)": 1,
                "Jednoiposoban (1.5)": 1.5,
                "Dvosoban (2)": 2,
                "Trosoban (3)": 3,
                "Četverosoban (4)": 4,
                "Petosoban i više": 5,
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8+": 8,
            }
            self.data["broj_soba"] = name_room[self.data["broj_soba"]]

    def fix_number_of_floors(self):
        if "broj_spratova" in self.data:
            if self.data["broj_spratova"] == "5+":
                self.data["broj_spratova"] = 5
            self.data["broj_spratova"] = int(self.data["broj_spratova"])

    def fix_namjesten(self):
        if self.type == "Stan":
            namjesten_mapping = {
                "Namješten": 2,
                "Nenamješten": 0,
                "Polunamješten": 1,
                "Namje&scaron;ten": 2,
                1: 2,
                0: 0,
            }
            if "namjesten" in self.data:
                self.data["namjesten"] = namjesten_mapping[self.data["namjesten"]]

    def fix_int_cols(self):
        """
        Yeah I dont even
        """
        if "udaljenost_rijeka" in self.data:
            self.data["udaljenost_rijeka"] = self.fix_int(
                self.data["udaljenost_rijeka"]
            )
        if "kvadratura_balkona" in self.data:
            self.data["kvadratura_balkona"] = self.fix_int(
                self.data["kvadratura_balkona"]
            )
        if "okucnica_kvadratura" in self.data:
            self.data["okucnica_kvadratura"] = self.fix_int(
                self.data["okucnica_kvadratura"]
            )

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
        latin_chars = {"š": "s", "đ": "dj", "č": "c", "ć": "c", "ž": "z"}
        # Add capital letters also
        latin_chars.update(
            {key.upper(): value.upper() for key, value in latin_chars.items()}
        )
        latin_chars["Đ"] = "Dj"
        for key in self.data:
            if isinstance(self.data[key], str):
                self.data[key] = "".join(
                    latin_chars.get(char, char) for char in self.data[key]
                )
