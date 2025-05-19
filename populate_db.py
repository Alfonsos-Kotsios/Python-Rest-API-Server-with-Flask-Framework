# populate_db.py

import pymongo
import json
import os

from app.model.student import Student
from app.model.answered_questionnaires import AnsweredQuestionnaire
from app.model.questionnaires import Questionnaire
from app.model.user import User

def populate_if_needed():
    mongo_host = os.environ.get("MONGO_HOST", "localhost")
    mongo_db_name = os.environ.get("MONGO_DATABASE", "ERGASIA")

    client = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")
    db = client[mongo_db_name]

    # ✅ Skip population if Students already exist
    if db["Students"].count_documents({}) > 0:
        print("✅ Database already populated. Skipping.")
        return

    # Students
    with open(os.path.join("assets", "students.json"), "r") as students_file:
        raw_students = json.load(students_file)
        students = [Student(**s) for s in raw_students]
        db["Students"].insert_many([s.to_dict() for s in students])
        print(len(students), "Students created")

    # Answered
    with open(os.path.join("assets", "answered_questionnaires.json"), "r") as a_file:
        answered_questionnaires = json.load(a_file)
        db["Answered_questionnaires"].insert_many(answered_questionnaires)
        print(len(answered_questionnaires), "Answered_questionnaires created")

    # Questionnaires
    with open(os.path.join("assets", "questionnaires.json"), "r") as q_file:
        questionnaires = json.load(q_file)
        db["Questionnaires"].insert_many(questionnaires)
        print(len(questionnaires), "Questionnaires created")

    # Users (students + admin)
    users = [User(s.username, s.password, "student").to_dict() for s in students]
    users.append(User("admin", "admin123", "admin").to_dict())
    db["Users"].insert_many(users)
    print(len(users), "Users created (students + admin)")
