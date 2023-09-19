from scrapy.selector import Selector

from interactive_crawler.interactive_spider import InteractiveSpider
from interactive_crawler.extractors import extract_email


class VCSheetInvestorsSpider(InteractiveSpider):
    def parse(self):
        page = self.context.new_page()
        page.goto('https://www.vcsheet.com/investors')
        len_of_page = 0
        match = False

        while not match:
            last_count = len_of_page
            page.wait_for_timeout(3000)  # Wait for 3 seconds
            len_of_page = page.evaluate('''() => {
                window.scrollTo(0, document.body.scrollHeight);
                return document.body.scrollHeight;
            }''')
            if last_count == len_of_page:
                match = True

        page_source = page.content()
        selector = Selector(text=page_source)
        investor_elements = selector.css('div.collection-list-2.w-dyn-items div[role="listitem"]')
        for element in investor_elements:
            email = None  # otherwise the will bring the last email to the next one
            investor_name = element.css('h3.list-heading.list-pages::text').get().strip() if element else None
            linkedin_url = element.css('a.contact-icon.linkedin.w-inline-block::attr(href)').get() if element else None
            website_url = element.css('a.contact-icon.site-link.w-inline-block::attr(href)').get() if element else None

            if website_url and website_url.strip() != '#':
                website_page = self.context.new_page()
                try:
                    website_page.goto(website_url, timeout=10*1000)
                    website_content = website_page.content()
                    email = extract_email(website_content)
                except Exception as err:
                    print(f'An error occured while fetching {website_url}: {err}')
                finally:
                    website_page.close()
                yield {
                    'investor_name': investor_name,
                    'linkedin': linkedin_url,
                    'website': website_url,
                    'email': email,
                }
        page.close()