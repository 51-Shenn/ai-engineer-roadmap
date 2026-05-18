The main differences lie in their **ecosystem**, **authentication methods**, and **data structure**.

Google recently introduced the **`google-genai`** package (replacing the older `google-generativeai`), which unifies their personal (AI Studio) and enterprise (Vertex AI) platforms. OpenAI remains the industry standard with the most "copied" API structure, while Anthropic focuses on a strict "messages" format and safety-first parameters.

### 1. Comparison Overview

| Feature | **Google (`google-genai`)** | **OpenAI (`openai`)** | **Anthropic (`anthropic`)** |
| :--- | :--- | :--- | :--- |
| **Package Name** | `google-genai` | `openai` | `anthropic` |
| **Primary Method** | `models.generate_content` | `chat.completions.create` | `messages.create` |
| **System Prompt** | Passed in `config` | Passed as a "system" role message | Passed as a top-level `system` parameter |
| **Token Limit Param** | `max_output_tokens` | `max_tokens` (or `max_completion_tokens`) | `max_tokens` |
| **Best For** | Multimodality & Google Cloud integration | General purpose & ecosystem support | Complex reasoning & long-form writing |

---

### 2. How to Call Them (Python Examples)

#### **Google Gemini (`google-genai`)**
Google's new SDK uses a `Client` object that automatically handles switching between AI Studio (API Key) and Vertex AI (Google Cloud credentials).
```python
# pip install google-genai
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain quantum physics in one sentence.",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful physics professor.",
        max_output_tokens=100,
        temperature=0.7
    )
)

print(response.text)
```

#### **OpenAI ChatGPT (`openai`)**
The OpenAI SDK is the most common pattern. It uses a `messages` list where the first item is typically the system instruction.
```python
# pip install openai
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum physics in one sentence."}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
```

#### **Anthropic Claude (`anthropic`)**
Anthropic requires a `system` parameter outside the `messages` list, and `max_tokens` is **mandatory** for every request.
```python
# pip install anthropic
import anthropic

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024, # Required
    system="You are a helpful assistant.", # Top-level parameter
    messages=[
        {"role": "user", "content": "Explain quantum physics in one sentence."}
    ]
)

print(message.content[0].text)
```

---

### 3. Key Architectural Differences

1.  **Response Objects**:
    *   **Google**: Returns a Pydantic-based object. You access text via `response.text`.
    *   **OpenAI**: Returns a nested object. You access text via `response.choices[0].message.content`.
    *   **Anthropic**: Returns a list of "content blocks." You access text via `message.content[0].text`.
2.  **Streaming**:
    *   Google uses `models.generate_content_stream`.
    *   OpenAI uses `stream=True` and iterates over chunks.
    *   Anthropic uses a specialized context manager: `with client.messages.stream(...) as stream:`.
3.  **Tool Use (Function Calling)**:
    *   **OpenAI** uses the `tools` parameter with JSON schemas.
    *   **Google** uses a similar `tools` array but supports "Google Search" as a built-in tool easily.
    *   **Anthropic** uses the `tools` parameter but is known for being very strict about the schema and XML-like tags in the background.
