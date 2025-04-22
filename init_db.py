# init_db.py
import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["UniQ"]

def load_collection(file_path, collection_name):
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    db[collection_name].delete_many({})
    db[collection_name].insert_many(data)

load_collection("init_data/students.json", "students")
load_collection("init_data/questionnaires.json", "questionnaires")
load_collection("init_data/answered_questionnaires.json", "answered_questionnaires")

print("✔ Database initialized.")
