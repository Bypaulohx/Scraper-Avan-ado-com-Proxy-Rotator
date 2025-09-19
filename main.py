import yaml
import time
import logging
from pathlib import Path
from urllib.parse import urlparse
import os

from proxy_manager import ProxyManager
from robots_checker import RobotsChecker
from fetcher_requests import RequestsFetcher
from fetcher_selenium import SeleniumFetcher
from extractor import extract_title_and_meta
from storage import Storage

logging.basicConfig(level=logging.INFO)

CONFIG_PATH = Path(__file__).parent / 'config.yaml'

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def domain_of(url):
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"

def main(urls=None):
    cfg = load_config()
    proxies = []
    proxies_file = Path(cfg.get('proxies_file'))
    if proxies_file.exists():
        proxies = [l.strip() for l in proxies_file.read_text().splitlines() if l.strip()]

    proxy_mgr = ProxyManager(proxies_list=proxies)
    robots = RobotsChecker(cfg.get('user_agent'))
    req_fetcher = RequestsFetcher(cfg.get('user_agent'), timeout=cfg.get('timeout'))
    sel_fetcher = SeleniumFetcher(cfg.get('chrome_driver_path'), user_agent=cfg.get('user_agent'), timeout=cfg.get('timeout'))

    storage = Storage(cfg['storage'])

    sample_urls = urls or ['https://example.com']

    for url in sample_urls:
        domain = domain_of(url)
        if cfg.get('respect_robots'):
            try:
                if not robots.can_fetch(domain, url):
                    logging.info(f"Bloqueado por robots.txt: {url}")
                    continue
            except Exception:
                logging.warning("Erro ao checar robots.txt; continuando com cautela")

        crawl_delay = robots.get_crawl_delay(domain) if cfg.get('respect_robots') else 0
        if crawl_delay:
            logging.info(f"Aplicando crawl-delay de {crawl_delay}s para {domain}")
            time.sleep(crawl_delay)

        proxy = proxy_mgr.get_proxy()
        try:
            html = req_fetcher.fetch(url, proxy=proxy)
        except Exception as e:
            logging.info(f"Requests falhou para {url}: {e}; tentando Selenium")
            try:
                html = sel_fetcher.fetch(url, proxy=proxy)
            except Exception as e2:
                logging.error(f"Falha ao buscar {url} com Selenium também: {e2}")
                proxy_mgr.report_failure(proxy)
                continue

        data = extract_title_and_meta(html)
        storage.save(url, data)
        time.sleep(1)

if __name__ == '__main__':
    main()
