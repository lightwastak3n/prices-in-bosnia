from rsScraper import RealEstateScraper
from real_estate import RealEstate

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/53617305/izdaje-se-stan-zgrada-slasticarna-palma", "Stan", test)

if data:
    rs_data = RealEstate(data, "Zemljiste")
    print(rs_data.data)