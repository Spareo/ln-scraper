try: 
    from result import *
    import slack
except:
    from ln_scraper.result import *
    import ln_scraper.slack as slack

import requests, json, re, boto3
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, settings):
        self.settings = settings
        self.simple_db_domain = settings['SimpleDB']['Domain']
        self.sdb_client = boto3.client('sdb')
        self.BASE_URL = "https://www.loopnet.com"
        self.SEARCH_URL = "%s/services/search" % self.BASE_URL
        self.results = []
        self.headers = { 
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/json'
        }

    def run_scrape_job(self):
        # Execute Search API call and get HTML that represents the results
        response = requests.post(self.SEARCH_URL, data=json.dumps(self.settings['LoopNet']), headers=self.headers)
        if response.status_code is 200:
            results = response.json()
            results_html = results['SearchPlacards']['Html']
        else:
            print("Last status code from requests: %s" % response.status_code)
            print("Last response from requests: %s" % response.content.decode())
            print("Failed to get search results with given settings")
            return False

        # Process the search results HTML with bs4
        soup = BeautifulSoup(results_html, features="html.parser")
        properties = soup.find_all('article')
        if len(properties) > 0:
            for property in properties:
                property_url = property.find("header").find("a").get("href")
                processed_result = self.process_search_result(property_url)
                self.results.append(processed_result)

        # Send the properties to slack
        if len(self.results) > 0: 
            for r in self.results:
                if self.property_exists_in_db(r) is False:
                    self.result_to_slack_message(r)
                    #self.save_result_to_sdb(r)

    def process_search_result(self, result_url):
        result = None
        results_dict = {}
        response = requests.get(result_url, headers=self.headers)
        if response.status_code is 200:
            results_dict['PropertyURL'] = result_url
            property_html = response.text
            soup = BeautifulSoup(property_html, features="html.parser")

            # Get Property Address from title
            title_text = soup.find("title").string.strip()
            match = re.match(r'^.+[0-9]+', title_text, re.I)
            if match:
                title_text = match.group()

            results_dict['Address'] =  title_text

            # Get all the pictures for the property
            image_urls = []
            image_elements = soup.find_all("i", {"class" : "ln-icon-zooming"})
            for image_element in image_elements:
                url = image_element.parent.find("img").get("src")
                image_urls.append(url)
                
            # Use first image as result image for now
            if len(image_urls) > 0:
                results_dict['ImageURL'] = image_urls[0]
            
            # Process attribute data for the result
            property_data_table = soup.find("table", {"class" : "property-data"})
            for row in property_data_table.find_all('tr'):
                try:
                    cells = row.find_all('td')
                    for i in range(len(cells)):
                        # The cells follow a pattern of Property Name --> Property Value
                        if i % 2 != 0: # Property Title 
                            results_dict[cells[i-1].string.strip()] = cells[i].string.strip()
                except:
                    continue

            # Process Unit Mix Information Section
            property_unit_mix_table = soup.find("table", {"class" : "property-data summary"})
            if property_unit_mix_table:
                unit_mix_table_headers = property_unit_mix_table.find_all("th")
                unit_mix_table_values = property_unit_mix_table.find_all("td")
                for header_index in range(len(unit_mix_table_headers)):
                    header_name = unit_mix_table_headers[header_index].text.strip()
                    header_value = unit_mix_table_values[header_index].text.strip()
                    results_dict['MIX_INFO_%s' % header_name] = header_value

        else:
            # Failed to parse, just return None and proceed
            print("Failed to parse property for %s" % result_url)

        result = Result(results_dict)
        return result

    def result_to_slack_message(self, result):
        # Generate the fields for the slack message
        fields = []
        fields.append(slack.Field("Price", result.price)) if result.price is not None else None
        fields.append(slack.Field("No. Units", result.num_units)) if result.num_units is not None else None
        fields.append(slack.Field("Building Class", result.building_class)) if result.building_class is not None else None
        fields.append(slack.Field("Cap Rate", result.cap_rate)) if result.cap_rate is not None else None
        fields.append(slack.Field("Year Built", result.year_built)) if result.year_built is not None else None
        fields.append(slack.Field("Average Occupancy", result.avg_occupancy)) if result.avg_occupancy is not None else None
        fields.append(slack.Field("Avg. Rent/Mo", result.avg_rent)) if result.avg_rent is not None else None
        fields.append(slack.Field("Average Unit Size (Sq Ft)", result.avg_unit_size)) if result.avg_unit_size is not None else None

        attachments = []
        attachments.append(slack.Attachment('<%s|%s>' % (result.property_url, result.address), "#3AA3E3", fields=fields, image_url=result.image_url))

        message = slack.Message("LoopNet Scraper", "", emoji=":moneybag:", attachments=attachments)
        message.send('https://hooks.slack.com/services/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', username='ScraperBot', channel="test")

    def save_result_to_sdb(self, result):
        attributes = []
        for attr_name, attr_value in result.results_dict.items():
            if attr_name is not None and attr_name is not '':
                attribute = { 'Name': attr_name, 'Value': attr_value, 'Replace': False }
                attributes.append(attribute)

        response = self.sdb_client.put_attributes(
            DomainName=self.simple_db_domain,
            ItemName=result.address,
            Attributes=attributes
        )            

    def property_exists_in_db(self, result):
        # Try to get the property from SDB
        response = self.sdb_client.get_attributes(
            DomainName=self.simple_db_domain,
            ItemName=result.address,
        )

        # If the response dictionary has an Attributes key,
        # then the property was found in the DB
        if 'Attributes' in response:
            return True
        else:
            return False