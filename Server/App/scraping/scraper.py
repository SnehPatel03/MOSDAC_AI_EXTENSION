from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings
import requests
from pdfminer.high_level import extract_text as pdf_extract_text
from io import BytesIO

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MOSDACBot/1.0)"
}

def extract_text_from_url(url: str):
    try:
        response = requests.get(url, timeout=(5, 15), headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"[Fetch Error] {url} → {e}")
        return None

    content_type = response.headers.get("Content-Type", "").lower()

    if "application/pdf" in content_type or url.endswith(".pdf"):
        try:
            pdf_text = pdf_extract_text(BytesIO(response.content))
            if not pdf_text or len(pdf_text.strip()) < 100:
                return None

            return {
                "url": url,
                "title": url.split("/")[-1],
                "content": pdf_text.strip()
            }
        except Exception as e:
            print(f"[PDF Error] {url} → {e}")
            return None

    elif "xml" in content_type or url.endswith((".xml", ".rss")):
        try:
            soup = BeautifulSoup(response.text, "xml")
        except Exception:
            soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)
        if len(text) < 100:
            return None

        return {
            "url": url,
            "title": soup.title.string.strip() if soup.title else "No Title",
            "content": text
        }

    elif "text/html" in content_type:
        try:
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup([
                "script", "style", "noscript", "form",
                "input", "button", "label", "nav", "footer", "header"
            ]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            if len(text) < 200:
                return None

            return {
                "url": url,
                "title": soup.title.string.strip() if soup.title else "No Title",
                "content": text
            }

        except Exception as e:
            print(f"[HTML Error] {url} → {e}")
            return None

    else:
        return None
