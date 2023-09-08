import requests
from requests import Response
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from crawler.core.extractors import extract_emails, extract_email
from crawler.core.errors import DownloadError
from crawler.core.headers import headers_list


def extract_root_url(url):
    parsed_url = urlparse(url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return root_url


class Page:
    def __init__(self, url):
        self.url = url
        self.base_url = extract_root_url(self.url)
        self.response: Response = self._fetch(headers=headers_list[0])
    
    def _fetch(self, headers):
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            raise DownloadError(f"Error when downloading a page: {self.url}")
        return response
    
    @property
    def full_text(self):
        return self.response.text
    
    def get_tags(self, tags):
        soup = BeautifulSoup(self.response.content, 'html.parser')
        tags = soup.find_all(tags)
        return tags
    
    def get_nav_links(self):
        nav_links = []
        a_tags = self.get_tags(['a'])
        for a_tag in a_tags:
            if 'href' in a_tag.attrs and (not a_tag['href'].startswith('http') or a_tag['href'].startswith('/')):
                path = '/' + a_tag['href'] if not a_tag['href'].startswith('/') else a_tag['href']
                nav_links.append('{}{}'.format(self.base_url, path))
        return nav_links

    def get_external_links(self):
        external_links = []
        a_tags = self.get_tags(['a'])
        for a_tag in a_tags:
            if 'href' in a_tag.attrs and a_tag['href'].startswith('http'):
                external_links.append(a_tag['href'])
        return external_links

    def get_emails(self):
        return extract_emails(self.response.text)
    
    def get_email(self):
        return extract_email(self.response.text)