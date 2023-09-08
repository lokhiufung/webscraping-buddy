import pandas as pd
from bs4 import BeautifulSoup

from crawler.core.page import Page


def get_investor_name(row):
    return row.find('td', {'data-label': 'Investor name'}).text.strip()


def get_modal_path(row):
    return row.find('td', {'data-label': 'Investor name'}).find('a')['href']


def get_check_size(row):
    return row.find('td', {'data-label': 'Check size'}).text.strip()


class HomePage(Page):

    def get_table(self):

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(self.response.content, 'html.parser')

        # Find the table using its id or class
        table = soup.find('table', {'id': 'results_tb'})

        # Initialize a list to store the rows
        table_rows = []

        # Loop through each row in the table
        for row in table.find_all('tr'):
            if row['class'] and row['class'][0] == "sponsorRow":
                continue
            try:
                table_rows.append({
                    'investor_name': get_investor_name(row),
                    'modal_url': '{}/{}'.format(self.base_url, get_modal_path(row)),
                    'check_size': get_check_size(row),
                })
            except:
                print(row)

        df = pd.DataFrame(table_rows)
        return df
