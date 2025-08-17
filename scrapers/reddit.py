from .common import soup_from_url

def fetch_leads(query, max_results=20):
    url = f"https://www.reddit.com/search/?q={query}"
    soup = soup_from_url(url)
    results = []
    for post in soup.select('h3'):
        title = post.get_text(" ", strip=True)
        link = post.find_parent('a')
        href = link.get('href') if link else None
        if not href:
            continue
        if href.startswith('/'):
            href = f"https://www.reddit.com{href}"
        results.append({
            "title": title,
            "snippet": title,
            "url": href
        })
        if len(results) >= max_results:
            break
    return results
