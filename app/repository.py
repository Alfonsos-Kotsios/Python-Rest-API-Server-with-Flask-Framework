import pymongo
import os
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
        # Υλοποίηση Singleton pattern για να υπάρχει μόνο ένα Repository στην εφαρμογή
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            mongo_host = os.environ.get("MONGO_HOST", "localhost")
            mongo_db_name = os.environ.get("MONGO_DATABASE", "ERGASIA")
            # Δημιουργία σύνδεσης με τη βάση MongoDB
            client = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")
            cls._instance.db = client[mongo_db_name]
        return cls._instance

    def __init__(self) -> None:
        # Αποτρέπει την απευθείας δημιουργία αντικειμένου (χρησιμοποιείται το instance())
        raise RuntimeError('Call instance() instead')

    def get_Students(self) -> List[Student]:
        # Επιστρέφει λίστα με όλους τους φοιτητές από τη βάση
        students = self.db["Students"].find()
        return [Student.from_dict(student) for student in students]
    
    def get_student_by_username(self, username: str) -> Optional[Student]:
        # Επιστρέφει φοιτητή με βάση το username ή None αν δεν βρεθεί
        students = self.db["Students"].find_one({"username": username})
        if students:
            return Student.from_dict(students)
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        # Επιστρέφει χρήστη (User) με βάση το username ή None αν δεν βρεθεί
        user_data = self.db["Users"].find_one({"username": username})
        if user_data:
            return User.from_dict(user_data)
        return None

    def get_questionnaires(self) -> List[Questionnaire]:
        # Επιστρέφει λίστα με όλα τα ερωτηματολόγια από τη βάση
        questionnaires = self.db["Questionnaires"].find()
        return [Questionnaire.from_dict(questionnaire) for questionnaire in questionnaires]
    

    
    def search_questionnaires(self, min_answers=None, max_answers=None, title=None, student_name=None, department=None,sort_by_answer_count=False, descending=True):
        query = {}

        # Φίλτρο για πλήθος απαντήσεων
        if min_answers or max_answers:
            query["answer_count"] = {}
            if min_answers:
                query["answer_count"]["$gte"] = int(min_answers)
            if max_answers:
                query["answer_count"]["$lte"] = int(max_answers)

        # Φίλτρο για τίτλο (αναζήτηση με regex)
        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        # Φίλτρο για όνομα φοιτητή ή τμήμα
        if student_name or department:
            student_filter = {}
            if student_name:
                student_filter["$or"] = [
                    {"name": {"$regex": student_name, "$options": "i"}},
                    {"surname": {"$regex": student_name, "$options": "i"}}
                ]
            if department:
                student_filter["department"] = {"$regex": department, "$options": "i"}

            # Βρίσκει τους φοιτητές που ταιριάζουν και φτιάχνει λίστα με reg_number
            matched = list(self.db["Students"].find(student_filter))
            reg_numbers = [s["reg_number"] for s in matched]
            query["student_id"] = {"$in": reg_numbers}

        # Εκτελεί το query στη συλλογή Questionnaires
        cursor = self.db["Questionnaires"].find(query)

        # Ταξινόμηση με βάση το πλήθος απαντήσεων αν ζητηθεί
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
        # Ενημερώνει τον κωδικό του χρήστη με το δοσμένο username
        result = self.db["Users"].update_one(
            {"username": username},
            {"$set": {"password": new_password}}
        )
        return result.modified_count > 0

    def get_questionnaires_by_student(self, reg_number: int) -> List[Questionnaire]:
        # Επιστρέφει όλα τα ερωτηματολόγια που έχει δημιουργήσει ο φοιτητής με το συγκεκριμένο reg_number
        questionnaires = self.db["Questionnaires"].find({"student_id": reg_number})
        return [Questionnaire.from_dict(questionnaire) for questionnaire in questionnaires]

    def update_questionnaire_title(self, questionnaire_id: int, new_title: str) -> bool:
        # Ενημερώνει τον τίτλο ενός ερωτηματολόγιου με βάση το id του
        result = self.db["Questionnaires"].update_one(
            {"questionnaire_id": int(questionnaire_id)},
            {"$set": {"title": new_title}}
        )
        return result.modified_count > 0

    def delete_questionnaire_and_answers(self, questionnaire_id: int) -> tuple[bool, int]:
        # Διαγράφει το ερωτηματολόγιο και όλες τις απαντήσεις του
        q_deleted = self.db["Questionnaires"].delete_one({"questionnaire_id": questionnaire_id})
        a_deleted = self.db["Answered_questionnaires"].delete_many({"questionnaire_id": questionnaire_id})
        # Επιστρέφει αν διαγράφηκε το ερωτηματολόγιο και πόσες απαντήσεις διαγράφηκαν
        return (q_deleted.deleted_count == 1, a_deleted.deleted_count)
            
    def create_questionnaire(self, questionnaire_data: dict) -> bool:
        # Εισάγει νέο ερωτηματολόγιο στη βάση
        try:
            self.db["Questionnaires"].insert_one(questionnaire_data)
            return True
        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    def get_next_questionnaire_id(self) -> int:
        # Βρίσκει το επόμενο διαθέσιμο id για νέο ερωτηματολόγιο (αυξανόμενος ακέραιος)
        last = self.db["Questionnaires"].find().sort("questionnaire_id", -1).limit(1)
        for doc in last:
            return doc["questionnaire_id"] + 1
        return 1  
    
    def get_questionnaire_answers(self, questionnaire_id: int) -> dict:
        # Επιστρέφει στατιστικά και όλες τις απαντήσεις για συγκεκριμένο ερωτηματολόγιο
        answered = list(self.db["Answered_questionnaires"].find({"questionnaire_id": questionnaire_id}))

        total = len(answered)
        students = sum(1 for a in answered if a["from_student"])
        users = total - students
        percent_users = (users / total * 100) if total > 0 else 0

        return {
            "total": total,
            "student_answers": students,
            "user_answers": users,
            "user_percentage": round(percent_users, 2),
            "answers": [AnsweredQuestionnaire.from_dict(a) for a in answered]
        }
    
    def create_student(self, student_data: dict) -> bool:
        # Δημιουργεί νέο φοιτητή και αντίστοιχο χρήστη στη βάση
        if self.db["Students"].find_one({"username": student_data["username"]}):
            return False  # Username already exists

        self.db["Students"].insert_one(student_data)

        self.db["Users"].insert_one({
            "id": student_data["id"],
            "username": student_data["username"],
            "password": student_data["password"],
            "type": "student"
        })

        return True
    
    def delete_student_by_reg_number(self, reg_number: int) -> bool:
        # Διαγράφει φοιτητή με βάση τον αριθμό μητρώου και όλα τα σχετικά δεδομένα του
        student = self.db["Students"].find_one({"reg_number": reg_number})
        if not student:
            # Αν δεν βρεθεί φοιτητής, επιστρέφει False
            return False

        # Παίρνει το username του φοιτητή για να διαγράψει και τον χρήστη
        username = student["username"]
        # Βρίσκει όλα τα ερωτηματολόγια που έχει δημιουργήσει ο φοιτητής
        questionnaire = list(self.db["Questionnaires"].find({"student_id": reg_number}))

        # Διαγράφει τον φοιτητή από τη συλλογή Students
        self.db["Students"].delete_one({"reg_number": reg_number})
        # Διαγράφει τον χρήστη από τη συλλογή Users
        self.db["Users"].delete_one({"username": username})
        # Διαγράφει όλα τα ερωτηματολόγια που έχει δημιουργήσει ο φοιτητής
        self.db["Questionnaires"].delete_many({"student_id": reg_number})

        # Για κάθε ερωτηματολόγιο που είχε δημιουργήσει ο φοιτητής,
        # διαγράφει όλες τις απαντήσεις που έχουν δοθεί σε αυτό
        for q in questionnaire:
            self.db["Answered_questionnaires"].delete_many({"questionnaire_id": q["questionnaire_id"]})  
        # Επιστρέφει True αν ολοκληρώθηκε η διαδικασία διαγραφής
        return True
