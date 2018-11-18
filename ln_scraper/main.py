from scraper import *
from settings import *


if __name__ == "__main__":
    # Read the settings
    sp = SettingsParser()
    settings = sp.get_settings('./ln_scraper/settings.yaml')

    # Scrape the data 
    scraper = Scraper(settings)
    scraper.run_scrape_job()