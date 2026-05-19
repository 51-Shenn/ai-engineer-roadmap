from dotenv import load_dotenv
import google.genai as genai
import json
import os

load_dotenv()

API_KEY_1 = os.getenv("GEMINI_API_KEY_2")
API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
if not API_KEY_1 or not API_KEY_2:
    raise ValueError("API key not found.")

client_1 = genai.Client(api_key=API_KEY_1)
client_2 = genai.Client(api_key=API_KEY_2)

conversation_history = []
MAX_HISTORY = 6
MEMORY_FILE = "files/session-memory.json"

def load_memory():
    """Load previous session history from disk into conversation_history"""
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
    """Persist current conversation_history to disk"""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"history": conversation_history}, f, indent=2)

def clear_memory():
    """Wipe session memory both in-memory and on disk"""
    conversation_history.clear()
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    print("[Memory cleared]")

def summarize_history():
    """
    Collapse old turns into a single summary message.
    Call this instead of trim_history() to improve continuity over compression.
    """
    if len(conversation_history) < MAX_HISTORY:
        return

    cutoff = len(conversation_history) // 2
    old_turns = conversation_history[:cutoff]
    recent_turns = conversation_history[cutoff:]

    history_text = "\n".join(
        f"{turn["role"].upper()}: {turn["parts"][0]["text"]}"
        for turn in old_turns
    )

    try:
        res = client_1.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=(
                "Summarize this conversation in 3-5 bullet points. "
                "Preserve key facts, decisions, and user intent.\n\n"
                + history_text
            )
        )
        summary_text = res.text

        summary_turn = {
            "role": "user",
            "parts": [{"text": f"[Summary of earlier conversation]\n{summary_text}"}]
        }

        conversation_history[:] = [summary_turn] + recent_turns
        print("[Conversation summarized to save context space]")

    except Exception as e:
        # Fallback to hard trim if summarization fails
        print(f"[Summarization failed ({e}), trimming instead]")
        trim_history()

def read_txt(file):
    if not os.path.exists(file):
        print("File path does not exists. Please try again.")
        return None

    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        print("Error: ", e)
        return None

def trim_history():
    """Hard truncate: keep only the most recent MAX_HISTORY turns"""
    if len(conversation_history) >= MAX_HISTORY:
        conversation_history[:] = conversation_history[-MAX_HISTORY:]

def chat(user_msg, context=None):
    file_content = read_txt(context) if context else ""

    prompt = f"""
    You must answer ONLY using the context below.

    Context:
    {file_content}

    User Question:
    {user_msg}
    """ if file_content else user_msg

    conversation_history.append(
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    )

    # trim_history()
    summarize_history()

    try:
        stream = client_2.models.generate_content_stream(
            model="gemini-2.5-flash-lite",
            contents=conversation_history,
            config={
                "system_instruction": (
                "You are required to answer strictly based on the provided context."
                "If the user asks about previous messages, you may answer based on conversation history."
                "Do not answer unrelated personal questions beyond the conversation context."
                "Keep answers short."
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

        # trim_history()
        save_memory()

    except Exception as e:
        print("Error: ", e)

def main():
    load_memory()

    context = input("Enter file path (or press Enter to skip): ").strip() or None

    while True:
        prompt = input("\nYou: ").strip()

        if prompt.lower() == "/exit":
            break
        elif prompt.lower() == "/clear":
            clear_memory()
            continue
        elif prompt.lower() == "/history":
            print(f"[{len(conversation_history)} turns in memory]")
            continue

        chat(prompt, context)

if __name__ == "__main__":
    main()
