import os

from tqdm import tqdm
import pandas as pd

from crawler.core.base_crawler import BaseCrawler
from crawler.openvc.fund_page import FundPage
from crawler.openvc.home_page import HomePage
from crawler.core.page import Page
from crawler.logger import get_logger


logger = get_logger('openvc_contact_crawler', 'debug')


VC_LIST_FILE_NAME = 'vc_list.csv'
INVESTOR_DETAILS_FILE_NAME = 'investor_details.csv'
INVESTOR_CONTACTS_FILE_NAME = 'investor_contacts.csv'
URL = "https://www.openvc.app"


class OpenvcContactCrawler(BaseCrawler):
    def run(self):
        vc_list_file_path = os.path.join(self.store_directories['cache'], VC_LIST_FILE_NAME)
        investor_details_file_path = os.path.join(self.store_directories['cache'], INVESTOR_DETAILS_FILE_NAME)

        if not os.path.exists(vc_list_file_path):
            # 1. get the table
            home_page = HomePage(url=f'{URL}/country/USA')
            df = home_page.get_table()
            self.write_df('cache', df, VC_LIST_FILE_NAME, index=False)
        else:
            df = pd.read_csv(vc_list_file_path)

        if not os.path.exists(investor_details_file_path):
            # 2. get the investor details
            df_investor_detail = []
            for i, record in enumerate(tqdm(df.to_dict('record'))):
                fund_page = FundPage(url=record['modal_url'])
                investor_detail = fund_page.get_investor_detail()
                df_investor_detail.append(investor_detail)

                if i > 0 and i % 20 == 0:
                    self.write_df('cache', df_investor_detail, INVESTOR_DETAILS_FILE_NAME, index=False)
            self.write_df('cache', df_investor_detail, INVESTOR_DETAILS_FILE_NAME, index=False)
        else:
            df_investor_detail = pd.read_csv(investor_details_file_path)

        # 3. get the emails fomr websites
        emails_list = []
        for record in tqdm(df_investor_detail.to_dict('records')):
            emails = None
            website = record['website']
            try:
                website_page = Page(url=record['website'])
                emails = website_page.get_emails()
                emails_list.append(emails)
            except Exception as err:
                logger.error(f'Error when extracting email from {website}: {err}')
        df_investor_detail['emails'] = emails
        self.write_df('data', df_investor_detail, INVESTOR_CONTACTS_FILE_NAME, index=False)


