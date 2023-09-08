import json

from bs4 import BeautifulSoup

from crawler.core.page import Page


def get_company_linkedin(fund_body):
    try:
        link_tags = fund_body.find('div', {'id': 'fundHeader'}).find('a', {'data-original-title': 'LinkedIn page'})
        return link_tags['href']
    except:
        return None

def get_company_website(fund_body):
    try:
        link_tags = fund_body.find('div', {'id': 'fundHeader'}).find('a', {'data-original-title': 'Website'})
        return link_tags['href']
    except:
        return None

def get_team_detail(fund_body):
    table_rows = []
    team_container = fund_body.find('div', {'id': 'teamCont'})
    if team_container:
        table = team_container.find('table', {'class': 'table fundDetail'})
        for row in table.find_all('tr'):
            name = row.find('a', {'class': 'profileCont text-nowrap'}).text.strip()
            profile_url_path = row.find('a', {'class': 'profileCont text-nowrap'})['href']
            table_rows.append({
                'name': name,
                'profile_url': profile_url_path,
            })
    return table_rows


class FundPage(Page):
    def get_investor_detail(self, record):
        soup = BeautifulSoup(self.response.content, 'html.parser')
        fund_body = soup.find('div', {'id': 'fundBody'})
        
        linkedin = get_company_linkedin(fund_body)
        website = get_company_website(fund_body)
        team_detail = get_team_detail(fund_body)
        team_detail = [{'investor_name': record['investor_name'], **item} for item in team_detail]

        return {
            'investor_name': record['investor_name'],
            'linkedin': linkedin,
            'website': website,
            'team_detail': json.dumps(team_detail)
        }

