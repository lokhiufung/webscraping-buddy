import re
import json

import scrapy


class OpenvcInvestorsSpider(scrapy.Spider):
    name = 'openvc_investors'
    base_url = "https://www.openvc.app"

    def start_requests(self):
        url = f"{self.base_url}/country/USA"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table = response.css('table#results_tb')
        for row in table.css('tr'):
            if 'sponsorRow' in row.css('::attr(class)').get():
                continue
            
            investor_name = row.css('td[data-label="Investor name"] a::text').get(default=None)
            modal_path = row.css('td[data-label="Investor name"] a::attr(href)').get(default=None)
            check_size = row.css('td[data-label="Check size"]::text').get(default=None)
            
            item = {
                'investor_name': investor_name,
                'modal_url': f"{self.base_url}/{modal_path}",
                'check_size': check_size,
            }
            # yield item
            yield scrapy.Request(url=item['modal_url'], callback=self.parse_modal, meta={'item': item})
            
    def parse_modal(self, response):
        item = response.meta['item']
        # extract investor details
        # linkedin
        linkedin = response.css('div#fundHeader a[data-original-title="LinkedIn page"]::attr(href)').get(default=None)
        # website
        website = response.css('div#fundHeader a[data-original-title="Website"]::attr(href)').get(default=None)
        # team details
        team_details = []
        team_rows = response.css('div#teamCont table.table.fundDetail tr')
        for row in team_rows:
            name = row.css('a.profileCont.text-nowrap::text').get().strip()
            profile_url_path = row.css('a.profileCont.text-nowrap::attr(href)').get()
            team_details.append({
                'name': name,
                'profile_url': profile_url_path,
            })
        team_details = [{'investor_name': item['investor_name'], **detail} for detail in team_details]

        investor_details = {
            'investor_name': item['investor_name'],
            'linkedin': linkedin,
            'website': website,
            'team_details': json.dumps(team_details)
        }
        # yield investor_details
        yield scrapy.Request(url=investor_details['website'], callback=self.parse_website, meta={'item': item, 'investor_details': investor_details})

    def parse_website(self, response):
        item = response.meta['item']
        investor_details = response.meta['investor_details']

        # extract email
        email = self.extract_email(text=response.body.decode('utf-8'))
        yield {
            "investor_name": item['investor_name'],
            "email": email,
            "check_size": item['check_size'],
            "linkedin": investor_details['linkedin'],
            "website": investor_details['website'],
            "team_details": investor_details['team_details'],
        }
        
    def extract_email(self, text):
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        if match:
            return match.group()

        
