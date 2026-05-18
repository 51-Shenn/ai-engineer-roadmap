from dotenv import load_dotenv
import google.genai as genai
import os

class Embeddings:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)

    def read_file(self, filepath: str="files/trading.md"):
        if not os.path.exists(filepath):
            print("Unable to read file. Please try again.")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("Error: ", e)
            return

    def fixed_chunk(self, text, chunk_size: int=200, overlap: int=30) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            chunks.append(text[start : start + chunk_size])
            start += chunk_size - overlap

        return chunks

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        vectors = []

        try:
            for chunk in chunks:
                res = self.client.models.embed_content(
                    model="gemini-embedding-2-preview",
                    contents=chunk
                )
                vectors.append(res.embeddings[0].values)

            return vectors
        except Exception as e:
            print("Error: ", e)
            return []

def main():
    load_dotenv()

    session = Embeddings(os.getenv("GEMINI_API_KEY_2"))

    file_content = session.read_file()
    if not file_content:
        return

    chunks = session.fixed_chunk(file_content)
    vectors = session.embed_chunks(chunks)

    print("Total chunks:", len(chunks))
    print("Total vectors:", len(vectors))
    print("First vector preview:", vectors[0][:5])

if __name__ == "__main__":
    main()
