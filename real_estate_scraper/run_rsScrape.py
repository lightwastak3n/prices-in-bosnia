from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/53614474/stan-na-dan-studio-apartman-naselje-bulevar", "Stan", test)

if data:
    rs_data = RealEstate(data, "Stan")
    print(rs_data.data)