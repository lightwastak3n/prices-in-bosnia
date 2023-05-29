from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/48894962/ilidza-stan-5545m2-novogradnja", "Stan", test)

rs_data = RealEstate(data, "Stan")
print(rs_data.data)