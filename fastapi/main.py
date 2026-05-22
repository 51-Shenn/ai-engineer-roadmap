from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": "1", "name": "Ali", "email": "ali@gmail.com"},
    {"id": "2", "name": "Bibi", "email": "bibi@gmail.com"},
    {"id": "3", "name": "Carl", "email": "carl@gmail.com"},
    {"id": "4", "name": "Doggo", "email": "doggo@gmail.com"},
    {"id": "5", "name": "Eleve", "email": "eleve@gmail.com"},
]

@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/users")
def get_all_users():
    return users

@app.get("/users/{id}")
def get_user_by_id(id):
    for user in users:
        if user["id"] == str(id):
            return user