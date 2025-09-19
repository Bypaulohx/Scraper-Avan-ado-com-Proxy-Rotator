import requests

class RequestsFetcher:
    def __init__(self, user_agent, timeout=30):
        self.headers = {"User-Agent": user_agent}
        self.timeout = timeout

    def fetch(self, url, proxy=None):
        session = requests.Session()
        if proxy:
            session.proxies.update({"http": proxy, "https": proxy})
        resp = session.get(url, headers=self.headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text
