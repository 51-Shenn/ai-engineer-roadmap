import json

file_path = 'files/data.json'

with open(file_path, 'r', encoding='utf-8') as f:
    a = json.load(f)

text = '{ "hello": "world" }'
b = json.loads(text) # b becomes a dictionary from a string

print(a == b)

# write dictionary into json file
dct = {'string': 'Hello World!', 'boolean': 'True'}

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(dct, f, indent=4)

with open(file_path, 'r', encoding='utf-8') as f:
    content = json.load(f)

data = {'a': 1, 'b': 2, 'c': 3}
text = json.dumps(data)

print(content, type(content)) # <class 'dict'>
print(text, type(text)) # <class 'str'>

# load: file => python
# loads: str => python
# dump: python => file
# dumps: python => str
