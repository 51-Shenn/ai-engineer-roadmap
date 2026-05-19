import os

def read_file(file_path="files/trading.md") -> str:
    if not os.path.exists(file_path):
        print("Unable to read file, please try again.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("Error: ", e)

def fixed_chunk(text, chunk_size: int = 200, overlap: int = 30) -> None:
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start : start+chunk_size])
        start += chunk_size - overlap

    return chunks

def main():
    chunks = fixed_chunk(read_file())

    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} ({len(chunk)} chars) ---")
        print(f"\"{chunk}\"")
        print("-" * 30 + "\n")

    print(f"Amount of chunks: {len(chunks)}")
    print(f"Chars per chunk: {len(chunks[0])}")
    print(f"Chars for the last chunk: {len(chunks[len(chunks) - 1])}")
    
if __name__ == "__main__":
    main()