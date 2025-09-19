import threading
import time
from collections import deque

class ProxyManager:
    """Gerencia um pool simples de proxies. Marca falhas e faz rotacionamento."""
    def __init__(self, proxies_list=None, cooldown_seconds=60):
        self.lock = threading.Lock()
        self.pool = deque(proxies_list or [])
        self.failed = {}
        self.cooldown = cooldown_seconds

    def get_proxy(self):
        with self.lock:
            if not self.pool:
                return None
            proxy = self.pool[0]
            self.pool.rotate(-1)
            return proxy

    def report_failure(self, proxy):
        with self.lock:
            if not proxy:
                return
            self.failed[proxy] = time.time()
            try:
                self.pool.remove(proxy)
            except ValueError:
                pass

    def recover_proxies(self):
        with self.lock:
            now = time.time()
            to_recover = [p for p, t in self.failed.items() if now - t > self.cooldown]
            for p in to_recover:
                self.pool.append(p)
                del self.failed[p]
