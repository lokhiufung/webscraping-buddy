import time
import random

from interactive_crawler.interactive_spider import InteractiveSpider


class InfluencersSpider(InteractiveSpider):
    """
    The engagement rate is calculated as the total number of interactions your content receives divided by your total number of followers, multiplied by 100%
    """
    N_SCROLLS = 1

    def parse(self):
        # a page must be navigate and control within a function
        page = self.context.new_page()
        page.goto('https://www.instagram.com')
        
        # Wait for the selectors to be available
        page.wait_for_selector('input[name="username"]')
        page.wait_for_selector('input[name="password"]')
        
        # Fill in the login credentials and submit
        page.fill('input[name="username"]', self.config['credentials']['username'])
        page.fill('input[name="password"]', self.config['credentials']['password'])
        page.click('button[type="submit"]')
        
        page.wait_for_timeout(10000)
        
        time.sleep(5)

        for query in self.config['queries']:
            query = '%20'.join(query.split(' '))  # combine the keywords to a single query
            page.goto(f'https://www.instagram.com/explore/search/keyword/?q={query}')
            
            anchors = []
            for _ in range(self.N_SCROLLS):
                page.wait_for_selector('a[href^="/p/"]')

                elements = page.query_selector_all('a[href^="/p/"]')
                anchors += ['https://www.instagram.com{}'.format(element.get_attribute('href')) for element in elements]

                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(2)

            # get info of anchors
            for anchor in anchors:

                # 1. go to the post
                page.goto(anchor)
                page.wait_for_selector('section main')
                element = page.query_selector_all('section main span a[role="link"]')
                profile_url = 'https://www.instagram.com' + element[0].get_attribute('href')
                
                page.goto(profile_url)
                page.wait_for_selector('header')
                
                # extract the profile image
                img = page.query_selector('header img')
                image_url = img.get_attribute('src')
                # extract the user name
                user_name = page.query_selector('main header section a[href="#"]').text_content()
                # extract the number of profile details
                details = []
                lis = page.query_selector_all('main header section ul li')
                for li in lis:
                    detail = li.text_content()
                    value, key = detail.split(' ')
                    details.append({ key: value })
                # extract description
                element_des = page.query_selector_all('header section > div')[-1]
                description = element_des.text_content()
                # divs = element_des.query_selector_all('div')
                # descripiton = '\n'.join([div.text_content() for div in divs])
                yield {
                    'image_url': image_url,
                    'user_name': user_name,
                    'details': details,
                    'description': description,
                }
                time.sleep(random.uniform(2, 3))

            time.sleep(random.uniform(5, 7))

