import scrapy
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod

from investors_crawler.extractors import extract_email  # Make sure this function is correctly implemented


class VcsheetInvestorsSpider(scrapy.Spider):
    name = 'vcsheet_investors'
    start_urls = ['https://www.vcsheet.com/investors']
    
    custom_settings = {
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                'playwright': True,
                'playwright_page_methods': [
                    # PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                    # PageMethod('wait_for_selector', 'div[role="list"]'),
                ],
                'playwright_include_page': True
            },
            callback=self.parse,
            errback=self.errback,
        )

    async def parse(self, response):
        # scroll the page to the bottom
        page = response.meta['playwright_page']
        for i in range(2, 10):
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            item_count = 10*i
            # await page.wait_for_selector(f'div[role="listitem"]:nth-child({item_count})')
        await page.close()

        selector = Selector(text=await page.content())
        investor_elements = selector.css('div.collection-list-2.w-dyn-items div[role="listitem"]')
        for element in investor_elements:
            investor_name = element.css('h3.list-heading.list-pages::text').get().strip() if element else None
            linkedin_url = element.css('a.contact-icon.linkedin.w-inline-block::attr(href)').get() if element else None
            website_url = element.css('a.contact-icon.site-link.w-inline-block::attr(href)').get() if element else None

            item = {
                'investor_name': investor_name,
                'linkedin': linkedin_url,
                'website': website_url,
            }
            yield item
            # yield scrapy.Request(
            #     website_url,
            #     callback=self.parse_website,
            #     errback=self.errback,
            #     meta={
            #         'playwright': True,
            #         'playwright_include_page': False,
            #         'item': item
            #     }
            # )

    def errback(self, failure):
        page = failure.request.meta['playwright_page']
        page.close()
        print(
            "Handling failure in errback, request=%r, exception=%r", failure.request, failure.value
        )

    def parse_website(self, response):
        item = response.meta['item']

        email = extract_email(text=response.body.decode('utf-8'))
        yield {
            'email': email,
            **item
        }
        
