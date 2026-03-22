from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of roughly chunk_size characters with overlap.
    A more sophisticated version would use tokenization, but character-based
    is a good production-start baseline.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        
        # Move start forward by chunk_size minus overlap
        start += (chunk_size - overlap)
        
        # Safety break to avoid infinite loop
        if start >= len(text) or chunk_size <= overlap:
            break
            
    return chunks

def clean_text(text: str) -> str:
    """
    Basic text cleaning: remove extra whitespace and normalize line endings.
    """
    if not text:
        return ""
    # Replace multiple newlines/spaces with single ones
    import re
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
