import pymongo
import json
import os

from app.model.student import Student
from app.model.answered_questionnaires import AnsweredQuestionnaire , Answer
from app.model.questionnaires import Questionnaire, Question
from app.model.user import User

def main():

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    db = client.UniQ

    with open(os.path.join("assets","students.json"), "r") as students_file:
        raw_students = json.load(students_file)
        students = [Student(**s) for s in raw_students]
    db["Students"].delete_many({})
    result = db["Students"].insert_many([s.to_dict() for s in students])
    print(len(result.inserted_ids), "Students created")

    with open(os.path.join("assets","answered_questionnaires.json"), "r") as answered_questionnaires_file:
        answered_questionnaires:list[AnsweredQuestionnaire] = json.load(answered_questionnaires_file)
    db["Answered_questionnaires"].delete_many({})
    result = db["Answered_questionnaires"].insert_many(answered_questionnaires)
    print(len(result.inserted_ids), "Answered_questionnaires created")

    with open(os.path.join("assets","questionnaires.json"), "r") as questionnaires_file:
        questionnaires:list[Questionnaire] = json.load(questionnaires_file)
    db["Questionnaires"].delete_many({})
    result = db["Questionnaires"].insert_many(questionnaires)
    print(len(result.inserted_ids), "Questionnaires created")
    


    users = [User(s.username, s.password, "student").to_dict() for s in students]
    users.append(User("admin", "admin123", "admin").to_dict())
    db["Users"].delete_many({})
    db["Users"].insert_many(users)
    print(len(users), "users created (students + admin)")


if __name__ == "__main__":
    main()
