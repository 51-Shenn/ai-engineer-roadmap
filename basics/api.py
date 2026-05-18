import requests
import json

file_path = 'files/wttr.json'
res = requests.get('https://wttr.in?format=j1')

print(res) # <Response [200]>
print(res.status_code) # 200
print(type(res))

data = json.dumps(res.json(), indent=2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(data)

with open(file_path, 'r', encoding='utf-8') as f:
    js = json.load(f)

print(type(data) == type(js)) # False because data <str>, js <dict>

# turn data into dict
data = json.loads(data)
print(f'Dictionary comparison: {data == js}') # True

# turn js into str
data = json.dumps(data)
js = json.dumps(js)
print(f'String comparison: {data == js}')
