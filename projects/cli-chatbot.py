from dotenv import load_dotenv
import google.genai as genai
import os

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY_1')

if not API_KEY:
    raise ValueError('API Key Not Found!')

client = genai.Client(api_key=API_KEY)

conversation_history = []
MAX_HISTORY = 20

def trim_history():
    if (len(conversation_history) > MAX_HISTORY):
        conversation_history[:] = conversation_history[-MAX_HISTORY:]

def chat(user_msg):
    conversation_history.append({'role': 'user', 'parts': [{'text': user_msg}]})
    trim_history()

    try:
        stream = client.models.generate_content_stream(
            model= 'gemini-2.5-flash-lite',
            contents=conversation_history,
            config={
                'system_instruction': """
                You are a tourist guide in Malaysia.
                Answer travel-related questions.
                If the user asks about previous messages, you may answer based on conversation history.
                Do not answer unrelated personal questions beyond the conversation context.
                Keep answers short.
                """
            }
        )

        print('\nGemini: ', end='', flush=True)

        full_response = ''

        for chunk in stream:
            if chunk.text:
                print(chunk.text, end='', flush=True)
                full_response += chunk.text

        conversation_history.append({'role': 'model', 'parts': [{'text': full_response}]})
        trim_history()

    except Exception as e:
        print('Error: ', e)
        conversation_history.pop()

def main():
    while True:
        prompt = input('\nYou: ')

        if prompt.lower() == '/exit' or prompt.lower() == '/quit':
            break

        chat(prompt)

if __name__ == '__main__':
    main()
