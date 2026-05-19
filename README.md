# Roadmap to AI Engineer

This repository follows a personal AI engineering roadmap suggested by Claude Chat. It is designed to guide my learning from Python fundamentals to LLM basics, Gemini API usage, RAG development, and other AI engineering topics through practical tasks and projects.

## Week 1 — Core syntax

**Day 1:** Variables & data types. Learn strings, integers, floats, booleans. Print values, try type() on everything.

**Day 2:** Lists & loops. Create a list, loop through it with for. Try append() and len().

**Day 3:** Dictionaries. Store key-value pairs, loop through .items(). Build a simple contact with name, age, email.

**Day 4:** If / else logic. Write if, elif, else. Build a grade checker (90+ = A, 80+ = B, etc).

**Day 5:** Functions. Write functions with def, use parameters and return. Refactor your grade checker into a function.

**Day 6:** Mini project. Build a to-do list in the terminal — add, view, and remove tasks using lists and functions.

**Day 7:** Rest. Re-read your own code, fix anything that felt unclear.

---

## Week 2 — Real-world skills

**Day 8:** Reading files. Open a .txt file, read its contents, print each line. Write text back to a new file.

**Day 9:** JSON. Load JSON with json.loads(), access nested values, save data back. This pattern appears everywhere in AI work.

**Day 10:** Calling an API. Install the requests library, call a free public API like wttr.in for weather, print the response.

**Day 11:** Error handling. Wrap your API call in try/except. Handle failed requests and bad data gracefully.

**Day 12:** Packages & pip. Install a package, learn what a virtual environment is, use python-dotenv to hide API keys.

**Day 13:** Final project. Build a weather CLI tool — takes a city name as input, calls the weather API, prints a friendly summary. This combines everything from both weeks.

**Day 14:** Rest & reflect. Push your projects to GitHub. Write down 3 things you learned. You're ready for the next step.

---

## Week 3 — LLM Basics with Gemini

**Day 15:** Setup. Get your Gemini API key from aistudio.google.com, install google-generativeai with pip, store your key in a .env file using python-dotenv. Never hardcode API keys.

**Day 16:** First API call. Send a simple text prompt to Gemini and print the response. Just get it working — one prompt, one response.

**Day 17:** Prompt engineering basics. Experiment with how differently worded prompts give different results. Try giving Gemini a role ("you are a helpful assistant that..."). Notice how the output changes.

**Day 18:** Conversation history. Learn how to pass previous messages so Gemini remembers context. This is what makes a chatbot feel like a real conversation.

**Day 19:** Build a simple chatbot. Terminal-based, loops until the user types "exit". Maintains conversation history. Similar structure to your weather CLI.

**Day 20:** System prompts. Give your chatbot a personality or a specific job — like a Python tutor, or a Malaysian food recommender. Control its behavior through the system prompt.

**Day 21:** Rest. Review and clean up your chatbot code.

---

## Week 4 — Build Something Real

**Day 22:** File input. Let your chatbot read a .txt file and answer questions about it. This is the foundation of RAG.

**Day 23:** Structured output. Ask Gemini to respond in JSON format. Parse it and display it nicely. This is how AI apps extract usable data.

**Day 24:** Streaming responses. Instead of waiting for the full response, print it word by word as it arrives. Makes the app feel much more natural.

**Day 25:** Simple memory. Save and load conversation history from a JSON file so the chatbot remembers between sessions.

**Day 26:** Build a CLI AI assistant. Combine everything — system prompt, conversation history, file reading, streaming, saved memory. One clean tool.

**Day 27:** Polish & README. Clean up your code, add comments, write a simple README. Push everything to GitHub. This is now a real portfolio project.

**Day 28:** Rest & reflect. You just went from basic Python to building an AI-powered application in 4 weeks.

---

## Week 5-6 — RAG foundations:

**Day 29:** Understand what RAG actually is. Read one article, watch one short video. Draw the flow on paper: document → chunks → embeddings → vector store → retrieval → LLM. Just understand the concept before touching code.

**Day 30:** Text chunking. Take a long .txt file and split it into smaller chunks using Python. No libraries yet — just string splitting and logic. Understand why we chunk (LLMs have context limits).

**Day 31:** Embeddings. Use Gemini's embedding API to convert a text chunk into a vector (a list of numbers). Print it. Just understand what an embedding is and what it looks like.

**Day 32:** Similarity search. Learn cosine similarity — how we compare two vectors to find how "related" they are. Implement it manually with basic math before using any library.

**Day 33:** Build a basic vector store. Store your chunks and their embeddings in a list of dictionaries. Write a search function that takes a query, embeds it, and returns the most similar chunks.

**Day 34:** Connect it to Gemini. Take the retrieved chunks, pass them as context to Gemini, and get an answer. This is your first working RAG pipeline — no frameworks, pure Python.

**Day 35:** Rest. You just built RAG from scratch. That's a big deal.

---

**Day 36:** Introduce ChromaDB. Replace your manual vector store with ChromaDB, a proper local vector database. Notice how much easier it is now that you understand what it's doing under the hood.

**Day 37:** PDF support. Use pymupdf to extract text from PDFs. Feed a real document into your RAG pipeline.

**Day 38:** Better chunking. Implement overlapping chunks so context isn't lost at chunk boundaries. Small change, big improvement in quality.

**Day 39:** Multi-document support. Let the user load multiple files. Store all of them in ChromaDB with metadata so you know which chunk came from which file.

**Day 40:** Source citation. When Gemini answers, also tell the user which chunk and which file the answer came from. This makes RAG responses trustworthy.

**Day 41:** Final project. Build a "chat with your documents" CLI tool. User drops files into a folder, your tool indexes them, and they can ask questions about any of them. Push to GitHub with a proper README.

**Day 42:** Rest and reflect. You now have a project that is genuinely impressive to show in an interview.