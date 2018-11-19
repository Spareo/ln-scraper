try:
    from scraper import *
    from settings import *
except:
    from ln_scraper.scraper import *
    from ln_scraper.settings import *

import boto3, os, glob


def run():
    # Find the settings file
    settings_file = None
    for filename in glob.iglob('**/ln_scraper_settings.yaml', recursive=True):
        print("Found settings file in: %s" % filename)
        settings_file = filename
        break

    if settings_file is None:
        print("Failed to find settings file")
        return false

    # Read the settings
    sp = SettingsParser()
    settings = sp.get_settings(settings_file)
    simple_db_domain = settings['SimpleDB']['Domain']

    # Check SimpleDB if setup, if not, setup.
    client = boto3.client('sdb')
    domains = client.list_domains()
    if domains.get(simple_db_domain) is None:
        client.create_domain(DomainName=simple_db_domain)

    # Scrape the data 
    scraper = Scraper(settings)
    scraper.run_scrape_job()


if __name__ == "__main__":
    run()