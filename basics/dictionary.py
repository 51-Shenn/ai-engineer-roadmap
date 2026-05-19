contact = {
    "name": "Kyle",
    "age": 18,
    "email": "kyle@gmail.com",
    "isFriend": True,
}

print(contact)
# print(contact["name"])
# print(contact["age"])
# print(contact["email"])
# print(contact["isFriend"])

for c in contact:
    print(c, end=": ") # this will print the key of the dictionary only
    print(contact[c]) # value

print()
print(contact.items())
print()

for key, value in contact.items():
    print(f"key: {key}, value: {value}")
