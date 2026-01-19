from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

EXCLUDE_KEYWORDS = [
    "login",
    "signup",
    "register",
    "sso",
    "gallery",
    "wp-admin",
    "javascript:",
    "#"
]

PRIORITY_KEYWORDS = [
    "data",
    "product",
    "satellite",
    "mission",
    "documentation",
    "manual",
    "api",
    "pdf"
]


def is_valid_url(url: str, base_domain: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in ("http", "https")
        and base_domain in parsed.netloc
    )


def is_excluded(url: str) -> bool:
    url_lower = url.lower()
    return any(k in url_lower for k in EXCLUDE_KEYWORDS)


def is_priority(url: str) -> bool:
    url_lower = url.lower()
    return any(k in url_lower for k in PRIORITY_KEYWORDS)


def crawl_url(base_url: str, max_pages: int = 50):
    visited = set()
    to_visit_priority = [base_url]
    to_visit_normal = []

    base_domain = urlparse(base_url).netloc

    while (to_visit_priority or to_visit_normal) and len(visited) < max_pages:

        if to_visit_priority:
            url = to_visit_priority.pop(0)
        else:
            url = to_visit_normal.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=(5, 15))
            response.raise_for_status()
        except Exception as e:
            print(f"Fetch failed: {url}")
            continue

        visited.add(url)

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            new_url = urljoin(url, link["href"])
            new_url = new_url.split("#")[0]  

            if not is_valid_url(new_url, base_domain):
                continue

            if is_excluded(new_url):
                continue

            if new_url in visited:
                continue

            if is_priority(new_url):
                to_visit_priority.append(new_url)
            else:
                to_visit_normal.append(new_url)

        time.sleep(0.8)

    return list(visited)


if __name__ == "__main__":
    urls = crawl_url("https://www.mosdac.gov.in", max_pages=50)
    print(f"\nTotal URLs collected: {len(urls)}\n")

    for u in urls:
        print(u)
