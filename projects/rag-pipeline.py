from dotenv import load_dotenv
import google.genai as genai
import json
import math
import os

load_dotenv()
API_KEY_1=os.getenv("GEMINI_API_KEY_3")
API_KEY_2=os.getenv("GEMINI_API_KEY_2")
if not API_KEY_1 or not API_KEY_2:
    raise ValueError("API Key Not Found")

client_1 = genai.Client(api_key=API_KEY_1)
client_2 = genai.Client(api_key=API_KEY_2)

conversation_history = []
MAX_HISTORY = 8
PRESERVE_TURNS = 2
MEMORY_FILE = "files/session-memory.json"
VECTOR_STORE_FILE = "files/vector-store.json"

def read_history():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        conversation_history[:] = json.load(f)

def save_history():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=2)

def read_file_content(file_path: str="files/trading.md") -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunking(text: str=None, chunk_size: int=500, overlap: int=60) -> list[str]:
    """fixed character-based chunking method"""
    if text is None:
        text = read_file_content()

    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap

    return chunks

def embed_chunks(chunks: list[str]=None) -> list[list[float]]: 
    if chunks is None:
        chunks = chunking()

    vectors = []

    for chunk in chunks:
        res = client_1.models.embed_content(
            model="gemini-embedding-2-preview",
            contents=chunk
        )
        vectors.append(res.embeddings[0].values)
    
    return vectors

def vector_store(chunks: list[str]=None, embeddings: list[list[float]]=None) -> list[dict]:
    if chunks is None:
        chunks = chunking()
    if embeddings is None:
        embeddings = embed_chunks(chunks)

    store = [
        {"id": i, "chunk": chunk, "embedding": embedding}
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    save_to_vector_store(store)

    return store

def save_to_vector_store(store: list[dict]) -> None:
    with open(VECTOR_STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)

def read_from_vector_store() -> list[dict]:
    if os.path.exists(VECTOR_STORE_FILE):
        with open(VECTOR_STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else: 
        print("[Vector Store Not Found. Building Now...]")
        return vector_store()

def search(query: str, store: list[dict], top_k=3) -> list[dict]:
    res = client_2.models.embed_content(
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

def summarize_history():
    summarize_turns = len(conversation_history) - PRESERVE_TURNS
    old_turns = conversation_history[:summarize_turns]
    recent_turns = conversation_history[summarize_turns:]
    history_text = "\n".join(
        f"{turn['role']}: {turn['parts'][0]['text']}"
        for turn in old_turns
    )

    summarized = client_2.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents= f"{history_text}",
        config={
            "system_instruction": (
                "You are given a conversation history that involves you and user."
                "You are required to summarize into key points and preserve key facts, user intent, and decisions."
            )
        }
    )

    summary_turns = {
        "role": "model",
        "parts": [{"text": f"[Previously Summarized Conversation]\n{summarized.text}"}]
    }

    conversation_history[:] = [summary_turns] + recent_turns
    save_history()

def cosine_similarity(a: list[float], b: list[float]):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(y ** 2 for y in b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

def chat(message: str, store: list[dict]):
    if len(conversation_history) > MAX_HISTORY: 
        summarize_history()

    # retrieve relavant chunks from vector store
    results = search(message, store, top_k=10)
    context = "\n\n".join(r["chunk"] for r in results)

    augmented_message = f"[Relevant Context]\n{context}\n\n[User Question]\n{message}"

    conversation_history.append(
        {
            "role": "user",
            "parts": [{"text": message}]
        }
    )

    augmented_contents = conversation_history[:-1] + [
        {
            "role": "user",
            "parts": [{"text": augmented_message}]
        }
    ]
    
    stream = client_1.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents=augmented_contents,
        config={
            "system_instruction": (
                "You are a trading professional."
                "Keep answer short and simple."
                "Don't answer unrelated questions."
            )
        }
    )

    full_response = ""
    print("\nGemini: ", end="", flush=True)

    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text

    print()

    conversation_history.append(
        {
            "role": "model",
            "parts": [{"text": full_response}]
        }
    )

    save_history()

def main():
    store = read_from_vector_store()

    name = input("Enter your name: ")
    name = name.strip()

    os.system("cls")
    print(f"Welcome, {name}")

    if os.path.exists(MEMORY_FILE):
        read_history()
        print(f"[Continued Previous Conversation: {len(conversation_history)} Messages]")

    while True:
        message = input("\nYou: ")
        message = message.strip()

        if not message:
            print("[Empty Message Detected. Please Try Again.]")
            continue

        if message.startswith("/"):
            if message == "/exit":
                break
            elif message == "/clear":
                os.system("cls")
                continue
            elif message == "/compact":
                summarize_history()
                print("[Conversation Compacted.]")
                continue
            elif message == "/status":
                print(f"[{len(conversation_history)} Messages]")
                continue
            else:
                print("[Instruction Not Found. Please Try Again.]")
                continue
        
        chat(message, store)

if __name__ == "__main__":
    os.system("cls")
    main()