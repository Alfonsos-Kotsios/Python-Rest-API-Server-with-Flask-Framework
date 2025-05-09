import pymongo

from typing import List, Optional
from app.model.questionnaires import Questionnaire, Question
from app.model.student import Student 
from app.model.answered_questionnaires import AnsweredQuestionnaire, Answer
from app.model.user import User
from bson import ObjectId


class Repository:
    _instance = None # Singleton instance


    @classmethod
    def instance(cls):
        
        if cls._instance is None:
            cls._instance = cls.__new__(cls)  # Create the object
            client = pymongo.MongoClient("localhost", 27017)
            cls._instance.db = client["UniQ"] 
        return cls._instance


    def __init__(self) -> None:
        
        raise RuntimeError('Call instance() instead')

    
    
    def get_Students(self) -> List[Student]:
        students = self.db["Students"].find()
        
        return [Student.from_dict(student) for student in students]
    
    def get_student_by_username(self, username: str) -> Optional[Student]:
        students = self.db["Students"].find_one({"username": username})
        if students:
            return Student.from_dict(students)
        return None
        
       
    
    
    def get_questionnaires(self) -> List[Questionnaire]:

        questionnaires = self.db["Questionnaires"].find()
        
        return [Questionnaire.from_dict(questionnaire) for questionnaire in questionnaires]
    

    
    def search_questionnaires(self, min_answers=None, max_answers=None, title=None, student_name=None, department=None,sort_by_answer_count=False, descending=True):
        query = {}

        if min_answers or max_answers:
            query["answer_count"] = {}
            if min_answers:
                query["answer_count"]["$gte"] = int(min_answers)
            if max_answers:
                query["answer_count"]["$lte"] = int(max_answers)

        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        if student_name or department:
            student_filter = {}
            if student_name:
                student_filter["$or"] = [
                    {"name": {"$regex": student_name, "$options": "i"}},
                    {"surname": {"$regex": student_name, "$options": "i"}}
                ]
            if department:
                student_filter["department"] = {"$regex": department, "$options": "i"}

            matched = list(self.db["Students"].find(student_filter))
            reg_numbers = [s["reg_number"] for s in matched]
            query["student_id"] = {"$in": reg_numbers}

        cursor = self.db["Questionnaires"].find(query)

        if sort_by_answer_count:
            sort_order = pymongo.DESCENDING if descending else pymongo.ASCENDING
            cursor = cursor.sort("answer_count", sort_order)

        return [Questionnaire.from_dict(q) for q in cursor]



    def get_user_by_username(self, username: str) -> Optional[User]:
            user_data = self.db["Users"].find_one({"username": username})
            if user_data:
                return User.from_dict(user_data)
            return None
    
    def update_user_password(self, username: str, new_password: str) -> bool:
        result = self.db["Users"].update_one(
            {"username": username},
            {"$set": {"password": new_password}}
        )
        return result.modified_count > 0
    
    def get_questionnaires_by_student(self, reg_number: int) -> List[Questionnaire]:

        questionnaires = self.db["Questionnaires"].find({"student_id": reg_number})
        
        return [Questionnaire.from_dict(questionnaire) for questionnaire in questionnaires]
    
    def update_questionnaire_title(self, questionnaire_id: str, new_title: str) -> bool:
        result = self.db["Questionnaires"].update_one(
            {"questionnaire_id": questionnaire_id},
            {"$set": {"description": new_title}}
        )
        return result.modified_count > 0
    
    def create_questionnaire(self, questionnaire_data: dict) -> bool:
        try:
            self.db["Questionnaires"].insert_one(questionnaire_data)
            return True
        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    def get_next_questionnaire_id(self) -> int:
        last = self.db["Questionnaires"].find().sort("questionnaire_id", -1).limit(1)
        for doc in last:
            return doc["questionnaire_id"] + 1
        return 1  
    
   