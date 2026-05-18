from dotenv import load_dotenv
import google.genai as genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY_1'))

res = client.models.generate_content(
    model='gemini-2.5-flash-lite',
    config={
        'system_instruction': 'You are a chef. Keep answers short and simple. DO NOT answer unrelated to your role of cooking, give a reason to the user.'
    },
    contents=[
        {
            'role': 'user',
            'parts': [{'text': 'How do i make a good pizza'}]
        }
    ]
)

print(res.text)
