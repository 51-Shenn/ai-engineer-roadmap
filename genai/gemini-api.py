from dotenv import load_dotenv
import google.genai as genai
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY_1"))

file_path = "files/gemini-models.txt"
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        for model in client.models.list():
            f.write(model.name + "\n")

res = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="What does token means in a simple term?"
)

# response.text                  # text string
# response.candidates            # list of candidate responses
# response.candidates[0].content # content object
# response.usage_metadata        # token usage info

# print(res)
print(res.text)

with open("files/res.txt", "w") as f:
    f.write(str(res))

with open("files/res.md", "w") as f:
    f.write(res.text)

res_dict = res.model_dump()
with open("files/res.json", "w") as f:
    json.dump(res_dict, f, indent=2)
