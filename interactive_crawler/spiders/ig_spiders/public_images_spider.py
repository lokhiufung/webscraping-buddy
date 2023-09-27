import time

from interactive_crawler.interactive_spider import InteractiveSpider


class PublicImagesSpider(InteractiveSpider):

    N_SCROLLS = 10

    def parse(self):
        # 1. start by logging in instagram
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

        # 2. iterate each public account and browse the images
        for public_account in self.config['public_accounts']:
            page.goto(f'https://www.instagram.com/{public_account}/')
            # Adding a delay for demonstration purposes, you can use `wait_for_selector` or other waits to handle post-login behavior
            page.wait_for_timeout(10000)

            # 3. scroll to get more images
            for _ in range(self.N_SCROLLS):
                elements = page.query_selector_all('a[href^="/p/"]')
                for element in elements:
                    img = element.query_selector('img')
                    if img:
                        image_url = img.get_attribute('src')
                        if image_url:
                            yield {
                                "image_url": image_url,
                                "account": public_account,
                            }
                # scroll AFTER extracting
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)

        page.close()
