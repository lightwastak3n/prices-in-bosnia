from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/53500046/zemljiste-zivinice-sjever-2", "Zemljiste", test)

if data:
    rs_data = RealEstate(data, "Zemljiste")
    print(rs_data.data)