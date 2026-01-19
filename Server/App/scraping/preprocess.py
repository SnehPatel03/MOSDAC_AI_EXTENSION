import re
from typing import List,Dict

def clean_text(text: str):
    """
    Removes extra spaces
    """
    return re.sub(r"\s+"," ",text).strip()

def chuncking(content: Dict , chunk_size: int=500) -> List[Dict]:
    cleaned_content = clean_text(content["content"])
    words = cleaned_content.split()
    chunks =[]
    
    for i in range(0,len(words),chunk_size):
        chunk_words = words[i : i + chunk_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(
            {
                "url" : content["url"],
                "title" :  content["title"],
                "chunk_id" : i,
                "content" : chunk_text
            }
        )
    return chunks
    
