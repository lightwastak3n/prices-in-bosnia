from rsScraper import RealEstateScraper

def test(x):
    pass

scraper = RealEstateScraper()
data = scraper.scrape_real_estate("533070662", "https://olx.ba/artikal/48894962/ilidza-stan-5545m2-novogradnja", "Zemljiste", test)
print(data)



