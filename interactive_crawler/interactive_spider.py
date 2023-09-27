from playwright.sync_api import sync_playwright
import random


class InteractiveSpider:
    OPTIONS = [
        '--disable-blink-features=AutomationControlled',
        '--disable-popup-blocking',
        '--start-maximized',
        '--disable-extensions',
        '--no-sandbox',
        '--disable-dev-shm-usage',
    ]
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    def __init__(self, headless=True, options=None, user_agent=None, randomize_user_agent=False, config=None):
        self.config = config if config is not None else {}
        # headless mode
        self.headless = headless
        # add more options to be more human
        self.options = list(set(self.OPTIONS + options)) if isinstance(options, list) else self.OPTIONS
        # set User-Agent
        if user_agent:
            # set by the user
            self.user_agent = user_agent
        elif randomize_user_agent:
            self.user_agent = random.choice(self.USER_AGENTS)
        else:
            self.user_agent = self.USER_AGENTS[0]
    
    def start(self):
        # start the playwright    
        self.p = sync_playwright().start()  # MUST call stop when closed
        self.browser = self.p.chromium.launch(
            headless=self.headless,
            args=self.OPTIONS
        )
        self.context = self.browser.new_context(user_agent=self.user_agent)
    
    def close_browser(self):
        self.browser.close()

    def stop(self):
        self.context.close()
        self.browser.close()
        self.p.stop()

    def parse(self):
        # a page must be navigate and control within a function
        # start your page here!
        # page = self.context.new_page()
        raise NotImplementedError
    
        