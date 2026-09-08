"""
Write a simple fixed sliding chunk function split_chunk. It will take the parameter text, chunk_size=500, overlap=50 for document slicing suitable for RAG ingestion.
"""
from typing import List


def split_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    if overlap > chunk_size:
        raise ValueError("overlap should be smaller than chunk size")
    if not text or chunk_size <= 0:
        return []

    chunks = []
    step = chunk_size - overlap
    text_length = len(text)

    for i in range(0, text_length, step):
        chunk = text[i: i + chunk_size]
        chunks.append(chunk)
        if i + chunk_size >= text_length:
            break

    return chunks


if __name__ == "__main__":
    sample_text = "this is a sample test for chunking for rag mechanism"
    chunks = split_chunk(sample_text, chunk_size=500, overlap=50)
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}")