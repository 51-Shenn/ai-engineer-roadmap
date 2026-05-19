from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("CS50_LANG")

print(api_key)
