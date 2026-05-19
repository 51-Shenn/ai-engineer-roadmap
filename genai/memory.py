from dotenv import load_dotenv
import google.genai as genai
from google.genai import errors
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY_1")
if not api_key:
    raise ValueError("API key not found!")

client = genai.Client(api_key=api_key)

conversation_history = []
MAX_HISTORY = 20  # keep last 20 messages

def trim_history():
    if len(conversation_history) > MAX_HISTORY:
        conversation_history[:] = conversation_history[-MAX_HISTORY:]

def chat(user_message):
    conversation_history.append(
        {
            "role": "user",
            "parts": [{"text": user_message}]
        }
    )

    trim_history()

    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=conversation_history,
            config={
                "system_instruction": """
                You are a senior AI engineer working at a tech company.
                Never mention you are a language model or AI system.
                Always answer from the perspective of an experienced engineer.
                Keep responses technical and concise.
                """
            }
        )

        print("\nGemini: " + res.text)
        conversation_history.append(
            {
                "role": "model",
                "parts": [{"text": res.text}]
            }
        )

    except errors.APIError as e:
        print(f"API error {e.code}: {e.message}")
        conversation_history.pop()

    except Exception as e:
        print(f"Unexpected error: {e}")
        conversation_history.pop()

while True:
    prompt = input("\nYou: ")

    if (prompt.lower() == "/exit" or prompt.lower() == "/quit"):
        break

    chat(prompt)
