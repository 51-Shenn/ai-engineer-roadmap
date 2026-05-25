from dotenv import load_dotenv
import google.genai as genai
import chromadb

# client = chromadb.Client()
client = chromadb.PersistentClient(path="files/chromadb")

# collection = client.get_collection("testing")
# collection = client.create_collection("testing")
collection = client.get_or_create_collection("testing")

if collection.count() == 0:
    collection.add(
        documents=["the sky is blue", "cats love napping", "python is great"],
        metadatas=[{"source": "facts"}, {"source": "pets"}, {"source": "dev"}],
        ids=["id1", "id2", "id3"]
    )

print(collection.get(ids=["id1"]))
collection.update(ids=["id1"], documents=["Blue sky."])
# print(collection.delete(ids=["id1"]))
print(collection.count())
print(client.list_collections())
# client.delete_collection("testing")

results = collection.query(
    query_texts=["what color is the sky?"],
    n_results=3
)

print(results)