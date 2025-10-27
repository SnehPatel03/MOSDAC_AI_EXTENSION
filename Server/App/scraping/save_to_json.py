import json
import os
from typing import List,Dict


def save_to_json(chunks: List[Dict], filename: str = "scraped_data.json"):
    """Save chunks into a JSON file."""
    output_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    print(f"✅ Data saved successfully to {filepath}")
