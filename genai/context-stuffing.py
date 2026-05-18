from dotenv import load_dotenv
import google.genai as genai
import os

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY_1')
if not API_KEY:
    raise ValueError('API key not found!')

client = genai.Client(api_key=API_KEY)
conversation_history = []
MAX_HISTORY = 6

def read_txt(file_path):
    if not os.path.exists(file_path):
        print('File path does not exists. Please try again.')
        return

    contents = ''

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()

        return contents

    except Exception as e:
        print('Error: ', e)

def trim_history():
    if len(conversation_history) >= MAX_HISTORY:
        conversation_history[:] = conversation_history[-MAX_HISTORY:]

def chat(user_msg, context=None):
    file_content = ''

    if context:
        file_content = read_txt(context) or ''

    prompt = f"""
    You must answer ONLY using the context below.

    Context:
    {file_content}

    User Question:
    {user_msg}
    """

    conversation_history.append(
        {
            'role': 'user',
            'parts': [{'text': prompt}]
        }
    )

    trim_history()

    try:
        stream = client.models.generate_content_stream(
            model='gemini-2.5-flash-lite',
            contents=conversation_history,
            config={
                'system_instruction': f"""
                You are an experienced trader in the stock market.
                You are required to answer strictly based on the provided context.
                If the user asks about previous messages, you may answer based on conversation history.
                Do not answer unrelated personal questions beyond the conversation context.
                Keep answers short.
                """
            }
        )

        full_response = ''
        print('\nGemini: ', end='', flush=True)

        for chunk in stream:
            if chunk.text:
                print(chunk.text, end='', flush=True)
                full_response += chunk.text

        print()

        conversation_history.append(
            {
                'role': 'model',
                'parts': [{'text': full_response}]
            }
        )

        trim_history()

    except Exception as e:
        print('Error: ', e)

def main():
    context = input('Enter file path (or press Enter to skip): ')

    while True:
        prompt = input('\nYou: ')

        if prompt.lower() == '/exit':
            break

        chat(prompt, context)

if __name__ == '__main__':
    main()
