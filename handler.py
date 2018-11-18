import json
from ln_scraper.settings import *
from ln_scraper.scraper import *

def run(event, context):
    # Read the settings
    sp = SettingsParser()
    settings = sp.get_settings('./ln-scraper/settings.yaml')

    # Scrape the data 
    scraper = Scraper(settings)
    scraper.run_scrape_job()

    return


    # body = {
    #     "message": "Go Serverless v1.0! Your function executed successfully!",
    #     "input": event
    # }

    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(body)
    # }

    # return response
