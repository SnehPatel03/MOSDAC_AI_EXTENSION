MOSDAC-Extension/
│
├── venv/                            # Virtual environment (created using `python -m venv venv`)
│
├── requirements.txt                 # All dependencies
├── main.py                          # Entry point (your run_scraper script)
│
├── app/
│   ├── __init__.py
│   │
│   ├── scraping/
│   │   ├── __init__.py
│   │   ├── crawler.py               # Collect all URLs from base domain
│   │   ├── scraper.py               # Extract and clean text from each URL
│   │   ├── preprocess.py            # clean_text() and chunk_text() functions
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py            # Generate embeddings using chosen model (e.g., SentenceTransformers)
│   │
│   ├── vector_db/
│   │   ├── __init__.py
│   │   ├── qdrant_client.py         # Initialize Qdrant and upsert chunks
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                # Custom logger for uniform print/log format
│   │   ├── config.py                # Centralized config (paths, API keys, constants)
│   │
│   └── api/
│       ├── __init__.py
│       ├── server.py                # FastAPI/Flask backend for chat/query interface (later)
│
└── data/
    ├── raw/                         # Optional: store raw HTML/PDFs temporarily
    ├── processed/                   # Optional: store cleaned and chunked JSONs
    └── embeddings/                  # Optional: store embeddings before upload
