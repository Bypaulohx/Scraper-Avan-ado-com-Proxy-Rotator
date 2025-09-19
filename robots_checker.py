from urllib import robotparser
from urllib.parse import urljoin

class RobotsChecker:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.parsers = {}

    def can_fetch(self, base_url, path):
        parser = self._get_parser(base_url)
        return parser.can_fetch(self.user_agent, path)

    def get_crawl_delay(self, base_url):
        parser = self._get_parser(base_url)
        delay = parser.crawl_delay(self.user_agent)
        return delay or 0

    def _get_parser(self, base_url):
        if base_url in self.parsers:
            return self.parsers[base_url]
        rp = robotparser.RobotFileParser()
        robots_url = urljoin(base_url, '/robots.txt')
        rp.set_url(robots_url)
        try:
            rp.read()
        except Exception:
            rp.parse('')
        self.parsers[base_url] = rp
        return rp
