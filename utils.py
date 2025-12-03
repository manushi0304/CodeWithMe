import json
import os

def load_user_data():
    if not os.path.exists("data/user_data.json"):
        return {}
    with open("data/user_data.json", "r") as f:
        return json.load(f)

def save_user_data(data):
    os.makedirs("data", exist_ok=True)
    with open("data/user_data.json", "w") as f:
        json.dump(data, f, indent=4)