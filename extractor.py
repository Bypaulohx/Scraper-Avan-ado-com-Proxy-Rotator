from bs4 import BeautifulSoup

def extract_title_and_meta(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else ''
    metas = {}
    for m in soup.find_all('meta'):
        key = m.get('name') or m.get('property')
        if key and m.get('content'):
            metas[key] = m.get('content')
    return {"title": title, "meta": metas}
