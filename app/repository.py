import pymongo

from typing import List, Optional
from app.model.questionnaires import Questionnaire, Question
from app.model.student import Student 
from app.model.answered_questionnaires import AnsweredQuestionnaire, Answer
from app.model.user import User


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
    
    
    def get_questionnaires(self) -> List[Questionnaire]:

        questionnaires = self.db["Questionnaires"].find()
        
        return [Questionnaire.from_dict(questionnaire) for questionnaire in questionnaires]
    

    
    def search_questionnaires(self, min_answers:int, max_answers:int, title=None, student_name=None, department=None ,sort_by_answer_count=False, descending=True):
        query = {}

        if min_answers  or max_answers :
            query["answer_count"] = {}
            if min_answers:
                 min_answers = int(min_answers)
                 if min_answers >= 0:
                     query["answer_count"]["$gte"] = min_answers
            if max_answers:
                max_answers = int(max_answers)
                if max_answers >= 0:
                    query["answer_count"]["$lte"] = max_answers
        
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

            matched_students = list(self.db["Students"].find(student_filter))
            reg_numbers = [s["reg_number"] for s in matched_students]
            query["student_id"] = {"$in": reg_numbers}


        # Ανάκτηση ερωτηματολογίων με ταξινόμηση από Mongo
        cursor = self.db["Questionnaires"].find(query)

        if sort_by_answer_count:
            order = pymongo.DESCENDING if descending else pymongo.ASCENDING
            cursor = cursor.sort("answer_count", order)

        return [Questionnaire.from_dict(r) for r in cursor]
  