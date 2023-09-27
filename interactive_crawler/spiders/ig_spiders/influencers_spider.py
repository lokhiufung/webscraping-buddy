import re
import time
import random

from interactive_crawler.interactive_spider import InteractiveSpider


class InfluencersSpider(InteractiveSpider):
    """
    The engagement rate is calculated as the total number of interactions your content receives divided by your total number of followers, multiplied by 100%
    """
    N_SCROLLS = 10

    def parse(self):
        # a page must be navigate and control within a function
        page = self.context.new_page()

        for query in self.config['queries']:
            query = '%20'.join(query.split(' '))  # combine the keywords to a single query
            page.goto(f'https://www.instagram.com/explore/search/keyword/?q={query}')
            
            anchors = []
            for _ in range(self.N_SCROLLS):
                elements = page.query_selector_all('a[href^="/p/"]')
                anchors += [element.get_attribute('href') for element in elements]

                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            
            # get info of anchors
            for anchor in anchors:
                page.goto(anchor)
                # TODO
                
            # time.sleep(random.uniform(5, 7))

