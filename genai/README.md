# Generative Artificial Intelligence

## File Structure

```
genai/
├── README.md
├── character-based-chunking.py     # split text into fixed-size character chunks
├── context-stuffing.py             # stuff full file content into prompt
├── cosine-similarity.py            # algorithm to measure similarity between embeddings
├── embeddings.py                   # generate vector embeddings from text chunks
├── gemini-api.py                   # basic api call
├── gemini-response.py              # api response output samples
├── memory.py                       # in-memory conversation history
├── session-memory.py               # persistent memory saved between runs
├── system-prompt.py                # system instructions
└── vector-store.py                 # store and query vectors
```

## Learning Outcomes

- Making basic API calls to Gemini
- Prompt engineering with system instructions
- Managing conversation memory (in-memory vs persistent)
- Text chunking strategies for large documents
- Generating and comparing vector embeddings
- Building a simple vector store