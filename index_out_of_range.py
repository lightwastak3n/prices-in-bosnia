from real_estate_scraper.rsScraper import RealEstateScraper
from real_estate_scraper.real_estate import RealEstate

def write_log_info(p):
    print(p)


scraper = RealEstateScraper()

link = "https://olx.ba/artikal/52001397/"
data = scraper.scrape_real_estate(1, link, "Stan", write_log_info=write_log_info)

new_rs = RealEstate(data, "Stan")

print(new_rs.data)