import re
import time
import random

from interactive_crawler.interactive_spider import InteractiveSpider


channel_ids = [
    'homefeed_recommed',
    'homefeed.fashion_v3',
    'homefeed.food_v3',
    'homefeed.cosmetics_v3',
    'homefeed.movie_and_tv_v3',
    'homefeed.career_v3',
    'homefeed.love_v3',
    'homefeed.household_product_v3',
    'homefeed.gaming_v3',
    'homefeed.travel_v3',
    'homefeed.fitness_v3',
]


class InfluencersSpider(InteractiveSpider):

    def parse(self):
        # a page must be navigate and control within a function
        page = self.context.new_page()
    
        for channel_id in channel_ids:
            page.goto(f'https://www.xiaohongshu.com/explore?channel_id={channel_id}')
            page.wait_for_selector("xpath=//div[contains(@class, 'login-container')]")
            close_button = page.wait_for_selector("xpath=//*[@data-v-7c2d5134]", state="attached")
            close_button.click()
            page.wait_for_selector("xpath=//div[contains(@class, 'feeds-container')]")

            n_scrolls = 10
            for _ in range(n_scrolls):
                post_elements = page.query_selector_all("xpath=//div[contains(@class, 'feeds-container')]/section")
                for post in post_elements:
                    profile_page = self.context.new_page()
                    try:
                        # profile url
                        author_tag = post.query_selector("css=a.author")
                        profile_url = author_tag.evaluate("element => element.href")

                        # go to the profile
                        profile_page.goto(profile_url)
                        profile_page.wait_for_selector("xpath=//div[contains(@class, 'user-info')]")

                        # Extract interactions
                        user_interactions = []
                        user_interactions_elements = profile_page.query_selector_all("div.user-interactions > div")
                        for element in user_interactions_elements:
                            count = element.query_selector("span.count").inner_text()
                            show = element.query_selector("span.shows").inner_text()
                            user_interactions.append({show: count})

                        n_followers = list(user_interactions[1].values())[0]
                        if re.search('[wkm]', n_followers.lower()):
                            # only extract the profile with followers > 1K
                            # Extracting data from the page
                            image_url = profile_page.query_selector("img.user-image").get_attribute("src")
                            user_name = profile_page.query_selector("div.user-name").inner_text()
                            user_id = profile_page.query_selector("span.user-redId").inner_text()

                            # Handle optional elements
                            user_ip = profile_page.query_selector("span.user-IP").inner_text()
                            user_desc = profile_page.query_selector("div.user-desc").inner_text()
                            
                            yield {
                                'url': profile_url,
                                'image_url': image_url,
                                'user_name': user_name,
                                'user_id': user_id,
                                'user_ip': user_ip,
                                'user_desc': user_desc,
                                'user_interactions': user_interactions,
                            }
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    finally:
                        profile_page.close()

                    time.sleep(random.uniform(2, 5))
                    
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(random.uniform(5, 7))
        page.close()

