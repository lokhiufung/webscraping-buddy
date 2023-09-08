import os

from tqdm import tqdm
import pandas as pd

from crawler.core.page import Page
from crawler.core.base_crawler import BaseCrawler
from crawler.vcsheet.investors_page import InvestorsPage
from crawler.logger import get_logger


INVESTORS_FILE_NAME = 'investors.csv'
INVESTOR_CONTACTS_FILE_NAME = 'investor_contacts.csv'


logger = get_logger('vc_sheet_crawler', 'debug')


class VcsheetCrawler(BaseCrawler):
    def run(self):
        investor_file_path = os.path.join(self.store_directories['cache'], INVESTORS_FILE_NAME)
        if not os.path.exists(investor_file_path):
            investors_page = InvestorsPage()
            df_investors = investors_page.get_investors()
            self.write_df('cache', df_investors, INVESTORS_FILE_NAME)
        else:
            df_investors = pd.read_csv(investor_file_path)

        emails = []
        for record in tqdm(df_investors.to_dict('records')):
            email = None
            if record['website'] and isinstance(record['website'], str):
                try:
                    website = record['website']
                    website_page = Page(url=website)
                    email = website_page.get_email()
                except Exception as err:
                    logger.error(f'Unexpected error when downloading websites: {website=} {err=}')
            emails.append(email)
        df_investors['emails'] = emails
        df_investors = df_investors[~df_investors['emails'].isnull()]
        self.write_df('data', df_investors, INVESTOR_CONTACTS_FILE_NAME)

        return df_investors
    



