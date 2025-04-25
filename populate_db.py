import pymongo
import json
import os

from app.model.student import Student
from app.model.answered_questionnaires import AnsweredQuestionnaire , Answer
from app.model.questionnaires import Questionnaire, Question

def main():

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    db = client.UniQ

    with open(os.path.join("assets","students.json"), "r") as students_file:
        students:list[Student] = json.load(students_file)
    result = db["Students"].insert_many(students)
    print(len(result.inserted_ids), "Students created")

    with open(os.path.join("assets","answered_questionnaires.json"), "r") as answered_questionnaires_file:
        answered_questionnaires:list[AnsweredQuestionnaire] = json.load(answered_questionnaires_file)
    result = db["Answered_questionnaires"].insert_many(answered_questionnaires)
    print(len(result.inserted_ids), "Answered_questionnaires created")

    with open(os.path.join("assets","questionnaires.json"), "r") as questionnaires_file:
        questionnaires:list[Questionnaire] = json.load(questionnaires_file) 
    result = db["Questionnaires"].insert_many(questionnaires)
    print(len(result.inserted_ids), "Questionnaires created")
    

if __name__ == "__main__":
    main()
