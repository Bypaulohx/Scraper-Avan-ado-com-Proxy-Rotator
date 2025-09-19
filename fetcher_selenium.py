from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class SeleniumFetcher:
    def __init__(self, driver_path, user_agent=None, timeout=30):
        self.driver_path = driver_path
        self.user_agent = user_agent
        self.timeout = timeout

    def _build_options(self, proxy=None):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        if self.user_agent:
            options.add_argument(f'--user-agent={self.user_agent}')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        return options

    def fetch(self, url, proxy=None):
        options = self._build_options(proxy)
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        try:
            driver.set_page_load_timeout(self.timeout)
            driver.get(url)
            return driver.page_source
        finally:
            driver.quit()
