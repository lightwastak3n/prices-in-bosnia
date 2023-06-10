from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/46267119/", "Kuca", test)
print(data)
if data:
    rs_data = RealEstate(data, "Kuca")
    print(rs_data.data)