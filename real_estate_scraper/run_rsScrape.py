from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/51870703/", "Zemljiste", test)
print(data)
if data:
    rs_data = RealEstate(data, "Stan")
    print(rs_data.data)