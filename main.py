from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

file_path = "users.json"


@app.post("/user")
def create_user(name: str, age: int, text: str):
        
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    if len(users) == 0:
        new_id = 1
    else:
        new_id = len(users) + 1

    new_user ={
        "ID" : new_id,
        "Name" : name,
        "Age" :age,
        "Text" : text
    }
    users.append(new_user)

    with open(file_path, "w") as f:
        json.dump(users, f, indent=4)

    return {"message": "User added successfully", "User": new_user}



@app.get("/users")
def get_users():

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    return users


@app.get("/user/{user_id}")
def get_single_user(user_id: int):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    for user in users:
        if user["ID"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/user/{user_id}")
def delete_user(user_id : int):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    for user in users:
        if user["ID"] == user_id:
            users.remove(user)
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)

        return {"message": "User deleted successfully", "User": user_id}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/user/{user_id}")
def update_user(user_id: int, name: str = None, age: int = None, text: str = None):

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    for user in users:
        if user["ID"] == user_id:

            if name is not None:
                user["Name"] = name
            if age is not None:
                user["Age"] = age
            if text is not None:
                user["Text"] = text

            with open(file_path, "w") as f:
                json.dump(users, f, indent=4)

            return {"message": f"User with ID {user_id} updated successfully", "user": user}

    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{user_id}/analyze")
def analyze_user_text(user_id: int):

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                users = json.load(f)
            except:
                users = []
    else:
        users = []

    user_found = False
    for user in users:
        if user["ID"] == user_id:
            user_found = True
            user_text = user.get("Text", "")
            break

    if not user_found:
        raise HTTPException(status_code=404, detail="User not found")

    if user_text == "":
        raise HTTPException(status_code=400, detail="Text is empty")
    if len(user_text) > 200:
        raise HTTPException(status_code=400, detail="Text too long (max 200 chars)")

    words = user_text.split()
    word_count = len(words)

    uppercase_count = sum(1 for c in user_text if c.isupper())
    special_count = sum(1 for c in user_text if not c.isalnum() and not c.isspace())

    result = {
        "UserID": user_id,
        "Text": user_text,
        "WordCount": word_count,
        "UppercaseCount": uppercase_count,
        "SpecialCharacterCount": special_count
    }

    return result


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8501",  # Streamlit default port
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow Streamlit requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)