from dotenv import load_dotenv
import google.genai as genai
import json
import os

load_dotenv()

API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
API_KEY_2 = os.getenv("GEMINI_API_KEY_1")
if not API_KEY_1 or not API_KEY_2:
    raise ValueError("API key not found.")

client_1 = genai.Client(api_key=API_KEY_1)
client_2 = genai.Client(api_key=API_KEY_2)

MAX_HISTORY = 10
conversation_history = []
MEMORY_FILE = "files/memory.json"

def load_memory():
    """Load previous memory from JSON file"""
    if not os.path.exists(MEMORY_FILE):
        return

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            conversation_history.extend(data.get("history", []))
            print(f"[Resumed session with {len(conversation_history)} messages]")
    except (json.JSONDecodeError, KeyError):
        print("[Could not load session memory — starting fresh]")

def save_memory():
    """Save current conversation history to JSON file"""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": conversation_history}, f, indent=2)
    except Exception as e:
        print("Error: ", e)

def clear_memory():
    """Clear all history from disk and in memory"""
    conversation_history.clear()
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    print("[Memory cleared]")

def read_file(file=None):
    if not os.path.exists(file):
        print("File does not exists. Please try again.")
        return False

    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("Error: ", e)

def summarize():
    if len(conversation_history) < MAX_HISTORY:
        return

    cutoff = len(conversation_history) // 2
    old_turns = conversation_history[:cutoff]
    recent_turns = conversation_history[cutoff:]

    history_text = "\n".join(
        f"{turn['role'].upper()}: {turn['parts'][0]['text']}"
        for turn in old_turns
    )

    try:
        res = client_2.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents= (
                "You are required to generate a conversation summary into bullet point"
                "Preserve key facts, decisions, user intent, and user information (if mentioned)"
                + history_text
            )
        )

        summary_turn = {
            "role": "user",
            "parts": [{"text": f"[Summary based on ealier conversation]:\n{res.text}"}]
        }

        conversation_history[:] = [summary_turn] + recent_turns
        print("[Conversation summarized to save context space]")

    except Exception as e:
        print(f"[Summarization failed ({e})]")

def chat(message, context=None):
    if context:
        data = read_file(context)

        if data is False:
            return
    else:
        data = None

    prompt_message = f"Context: {data}\n\nMessage: {message}"

    conversation_history.append({"role": "user", "parts": [{"text": prompt_message}]})

    summarize()

    try:
        stream = client_1.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=conversation_history,
            config={
                "system_instruction": (
                    "You are an AI ASSISTANT. You can also be anything (role) that user mentioned, but if user doesn't mention you are just assistant."
                    "You are required to answer question based on the given context."
                    "If context is None or does not exist, or you could not find related information in the context, ONLY you can answer based on your knowledge."
                    "But do mentioned that this is your knowledge, not based on the context itself."
                    "If the user asks about previous messages, you may answer based on conversation history."
                    "Do not answer unrelated personal questions beyond the conversation context."
                    "Keep your answer short and simple."
                    "Do not use emojis or don't use buzz word."
                )
            }
        )

        full_response = ""
        print("\nGemini:\n", end="", flush=True)

        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text

        print()

        conversation_history.append({"role": "model", "parts": [{"text": full_response}]})

        save_memory()

    except Exception as e:
        print("Error: ", e)

def main():
    os.system("clear")
    load_memory()

    while True:
        ctx = input("\nEnter file path (or press Enter to skip): ")
        ctx = ctx.strip() or None

        prompt = input("\nYou: ")
        prompt = prompt.strip()

        if prompt.lower() == "/exit":
            break
        elif prompt.lower() == "/save":
            save_memory()
            print(f"[Memory saved: {len(conversation_history)} turns in memory]")
            continue
        elif prompt.lower() == "/clear":
            clear_memory()
            continue
        elif prompt.lower() == "/history":
            print(f"[{len(conversation_history)} turns in memory]")
            continue

        chat(prompt, ctx)

if __name__ == "__main__":
    main()
