import os
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from crawler.core.page import Page


def extract_investor_name(item):
    return item.find('h3', {'class': 'list-heading list-pages'}).text.strip()


def extract_linkedin(item):
    a_tag = item.find('a', {'contact-icon linkedin w-inline-block'})
    if a_tag:
        return a_tag['href']
    return None


def extract_website(item):
    a_tag = item.find('a', {'class': 'contact-icon site-link w-inline-block'})
    if a_tag:
        return a_tag['href']
    return None


class InvestorsPage(Page):
    def __init__(self):
        super().__init__(url='https://www.vcsheet.com/investors')

    def get_investors(self):
        # selenium 4    
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Open the website
        driver.get(self.url)  # Change this URL to the website you want to scrape
        # Scroll
        lenOfPage = 0
        match=False
        while match==False:
            lastCount = lenOfPage
            time.sleep(3)  # Let the page load
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match=True
        page_source = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(page_source, 'html.parser')
        column = soup.find('div', {'class': 'collection-list-2 w-dyn-items'})

        df = []
        for item in column.find_all('div', {'role': 'listitem'}):
            investor_name = extract_investor_name(item)
            linkedin = extract_linkedin(item)
            website = extract_website(item)

            df.append((investor_name, linkedin, website))
        
        df = pd.DataFrame(df, columns=['investor_name', 'linkedin', 'website'])
        return df
    