import csv
import json
import sqlite3
import os
import psycopg2
from urllib.parse import urlparse

class Storage:
    def __init__(self, cfg):
        self.cfg = cfg
        t = cfg.get('type', 'csv')
        self.type = t.lower()
        if self.type in ('csv','json'):
            os.makedirs(os.path.dirname(cfg['path']), exist_ok=True)
        if self.type == 'sqlite':
            self.conn = sqlite3.connect(cfg['path'])
            self._ensure_table_sqlite()
        if self.type == 'postgres':
            # expects DATABASE_URL environment variable (e.g. postgres://user:pass@host:port/db)
            database_url = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URL'.upper())
            if not database_url:
                raise ValueError('DATABASE_URL env var not set for postgres storage')
            self.conn = psycopg2.connect(database_url)
            self._ensure_table_postgres()

    def _ensure_table_sqlite(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data (url TEXT PRIMARY KEY, json TEXT)''')
        self.conn.commit()

    def _ensure_table_postgres(self):
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS data (url TEXT PRIMARY KEY, json TEXT)''')
        self.conn.commit()
        cur.close()

    def save(self, url, payload):
        if self.type == 'csv':
            with open(self.cfg['path'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([url, json.dumps(payload, ensure_ascii=False)])
        elif self.type == 'json':
            with open(self.cfg['path'], 'a', encoding='utf-8') as f:
                f.write(json.dumps({"url": url, **payload}, ensure_ascii=False) + "\n")
        elif self.type == 'sqlite':
            c = self.conn.cursor()
            c.execute('INSERT OR REPLACE INTO data (url, json) VALUES (?, ?)', (url, json.dumps(payload, ensure_ascii=False)))
            self.conn.commit()
        elif self.type == 'postgres':
            cur = self.conn.cursor()
            cur.execute('INSERT INTO data (url, json) VALUES (%s, %s) ON CONFLICT (url) DO UPDATE SET json = EXCLUDED.json', (url, json.dumps(payload, ensure_ascii=False)))
            self.conn.commit()
            cur.close()
