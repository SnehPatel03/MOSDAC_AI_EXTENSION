import os
import sys
import time
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from App.scraping.crawler import crawl_url
from App.scraping.scraper import extract_text_from_url
from App.scraping.preprocess import chuncking
from App.services.embeddings import embed_texts
from App.vector_db.qdrant_db import init_collection, upsert_chunks


def run_scraper():
    base_url = "https://www.mosdac.gov.in"
    print(f"Scraping website: {base_url}")

    start_time = time.time()
    urls = crawl_url(base_url)
    print("Crawl done, first 3 URLs:", urls[:3])
    print(f"Found {len(urls)} pages to scrape")

    all_chunks = []
    successful_urls = 0

    for url in tqdm(urls, desc="Scraping pages"):
        page_data = extract_text_from_url(url)
        if not page_data:
            continue

        chunks = chuncking(page_data, chunk_size=200)
        all_chunks.extend(chunks)
        successful_urls += 1

    print(f"Scraped {successful_urls}/{len(urls)} pages, total chunks: {len(all_chunks)}")

    if not all_chunks:
        print("No content scraped. Exiting.")
        return

    texts = [c["content"] for c in all_chunks]
    try:
        embeddings = embed_texts(texts)
        print(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return

    try:
        init_collection(len(embeddings[0]))
        upsert_chunks(all_chunks, embeddings)
        print("Data stored in vector database")
    except Exception as e:
        print(f"Database operation failed: {e}")
        return

    print(f"Scraping pipeline completed in {time.time() - start_time:.2f} seconds")
    print("Sample chunks:")
    for i, chunk in enumerate(all_chunks[:3]):
        print(f"{i+1}. {chunk['content'][:100]}...")


if __name__ == "__main__":
    run_scraper()
