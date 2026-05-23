from dotenv import load_dotenv
import google.genai as genai
import json
import math
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY_1")

client = genai.Client(api_key=API_KEY)
VECTOR_STORE_FILE = "files/vector-store.json"

def read_file_content(file_path: str="files/trading.md") -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunking(text: str=read_file_content(), size: int=200, overlap: int=30) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start : start+size])
        start += size - overlap

    return chunks

def embed_chunks(chunks: list[str]=chunking()) -> list[list[float]]:
    vectors = []

    for chunk in chunks:
        res = client.models.embed_content(
            model="gemini-embedding-2-preview",
            contents=chunk
        )

        vectors.append(res.embeddings[0].values)

    return vectors

def cosine_similarity(a: list[float], b: list[float]):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(y ** 2 for y in b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)

def vector_store(chunks: list[str]=None, embeddings: list[list[float]]=None) -> list[dict]:
    if chunks is None:
        chunks = chunking()
    if embeddings is None:
        embeddings = embed_chunks(chunks)

    store = [
        {"id": i, "chunk": chunk, "embedding": embedding}
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

    return store

def search(query: str, store: list[dict], top_k: int=3) -> list[dict]:
    res = client.models.embed_content(
        model="gemini-embedding-2-preview",
        contents=query
    )

    query_vector = res.embeddings[0].values

    scored = [
        {
            "id": entry["id"],
            "chunk": entry["chunk"],
            "similarity": cosine_similarity(query_vector, entry["embedding"])
        }
        for entry in store
    ]

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]

if __name__ == "__main__":
    print("Building vector store…")
    store = vector_store()
    print(f"Stored {len(store)} chunks.\n")

    query = "What is a stop-loss order?"
    results = search(query, store, top_k=3)

    print(f"Top results for: '{query}'\n" + "─" * 40)
    for r in results:
        print(f"[{r['id']}] similarity={r['similarity']:.4f}\n{r['chunk']}\n")