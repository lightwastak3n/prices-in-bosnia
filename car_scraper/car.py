from car_scraper.columns_names import specs_columns_mapping

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
        self.clean_dict_keys()
        self.rename_columns()
        self.fix_basic_data()
        self.fix_year()
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
        self.data["cijena"] = self.data["cijena"].rstrip(" KM").replace(".", "")
        if "," in self.data["cijena"]:
            self.data["cijena"] = self.data["cijena"].split(",")[0]
        self.data["cijena"] = int(self.data["cijena"])
        if "kilometraza" in self.data:
            if "," in self.data["kilometraza"]:
                self.data["kilometraza"] = self.data["kilometraza"].split(",")[0]
            self.data["kilometraza"] = self.data["kilometraza"].replace("km", "")
            self.data["kilometraza"] = int(self.data["kilometraza"].replace(".",""))
        if "vrata" in self.data:
            self.data["vrata"] = self.data["vrata"].split("/")[0]
        if "velicina_felgi" in self.data and (self.data["velicina_felgi"] == "Ostalo" or self.data["velicina_felgi"] == ""):
            del self.data["velicina_felgi"]

    def fix_year(self):
        """
        Fix for the people listing 2000 years old cars and 'Starije'.
        """
        if 'godiste' not in self.data or self.data['godiste'] == "Starije" or int(self.data['godiste']) < 1950:
            self.data['godiste'] = 0

    def fix_power(self):
        """
        Tries to change power (kW and PS) to an int if possible. If not changes them to None.
        """
        if 'kilovata' in self.data and not self.data['kilovata'].isnumeric():
            try:
                self.data['kilovata'] = int("".join(filter(str.isdigit, self.data['kilovata'])))
            except ValueError:
                self.data['kilovata'] = None
        if 'konjskih_snaga' in self.data and not self.data['konjskih_snaga'].isnumeric():
            try:
                self.data['konjskih_snaga'] = int("".join(filter(str.isdigit, self.data['konjskih_snaga'])))
            except ValueError:
                self.data['konjskih_snaga'] = None

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
        radio_columns.append("metalik")
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
