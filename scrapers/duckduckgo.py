
from .common import soup_from_url

def search(query, site=None, max_results=20):
    q = query
    if site:
        q = f"site:{site} {query}"
    url = f"https://duckduckgo.com/html/?q={q}"
    soup = soup_from_url(url)
    results = []
    for res in soup.select('.result'):
        title_el = res.select_one('.result__a')
        snippet_el = res.select_one('.result__snippet')
        link_el = res.select_one('.result__a')
        if not (title_el and link_el):
            continue
        title = title_el.get_text(" ", strip=True)
        snippet = (snippet_el.get_text(" ", strip=True) if snippet_el else "")[:280]
        href = link_el.get("href")
        results.append({
            "title": title,
            "snippet": snippet,
            "url": href
        })
        if len(results) >= max_results:
            break
    return results
