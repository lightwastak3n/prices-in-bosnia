from carScraper_v2 import CarScraper
from car import Car

def test(x):
    pass

scraper = CarScraper()
data = scraper.scrape_car("53068731", "https://olx.ba/artikal/53370955/", test)
print("Got data")

if data:
    car = Car(data)
    print("Created car")
    print(car.data)
else:
    print("No data")