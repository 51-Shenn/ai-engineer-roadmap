# Generative Artificial Intelligence

## File Structure

```
genai/
├── README.md
├── gemini-api.py                   # basic api call
├── gemini-response.py              # api response output samples
├── system-prompt.py                # system instructions
├── memory.py                       # in-memory conversation history
├── session-memory.py               # persistent memory saved between runs
├── context-stuffing.py             # stuff full file content into prompt
├── character-based-chunking.py     # split text into fixed-size character chunks
├── embeddings.py                   # generate vector embeddings from text chunks
├── cosine-similarity.py            # algorithm to measure similarity between embeddings
├── vector-store.py                 # store and query vectors
└── vector-database.py              # examples of using chromadb as vector database
```

## Learning Outcomes

- Making basic API calls to Gemini
- Prompt engineering with system instructions
- Managing conversation memory (in-memory vs persistent)
- Text chunking strategies for large documents
- Generating and comparing vector embeddings
- Building a simple vector store