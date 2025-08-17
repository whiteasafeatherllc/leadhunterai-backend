from .common import soup_from_url

def search_posts(query, max_results=20):
    url = f"https://www.reddit.com/search/?q={query}"
    soup = soup_from_url(url)
    results = []

    # Reddit now uses a div with data-click-id="body" for post titles
    for post in soup.select('h3'):
        title = post.get_text(" ", strip=True)
        link_tag = post.find_parent('a')
        href = link_tag.get('href') if link_tag else None
        if not href:
            continue
        # Make href absolute if it's relative
        if href.startswith('/'):
            href = f"https://www.reddit.com{href}"
        results.append({
            "title": title,
            "snippet": title,  # you can update this to a summary later
            "url": href
        })
        if len(results) >= max_results:
            break

    return results
