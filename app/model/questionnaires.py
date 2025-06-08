from typing import List
import uuid


class Question:
    def __init__(self, type: str, description: str, question_num: int):
        self.type = type
        self.description = description
        self.question_num = question_num

    def to_dict(self):
        # Επιστρέφει την ερώτηση ως dictionary
        return {
            "type": self.type,
            "description": self.description,
            "question_num": self.question_num
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο Question από dictionary
        return Question(
            type=data["type"],
            description=data["description"],
            question_num=data["question_num"]
        )


class Questionnaire:
    def __init__(self, student_id: int, questionnaire_id: int, title: str,
                 description: str, unique_url: str, answer_count: int,
                 questions: List[Question]):
        self.id = str(uuid.uuid4())
        self.student_id = student_id
        self.questionnaire_id = questionnaire_id
        self.title = title
        self.description = description
        self.unique_url = unique_url
        self.answer_count = answer_count
        self.questions = questions

    def to_dict(self):
        # Επιστρέφει το ερωτηματολόγιο ως dictionary
        return {
            "id": self.id,
            "student_id": self.student_id,
            "questionnaire_id": self.questionnaire_id,
            "title": self.title,
            "description": self.description,
            "unique_url": self.unique_url,
            "answer_count": self.answer_count,
            "questions": [q.to_dict() for q in self.questions]
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο Questionnaire από dictionary
        questions = [Question.from_dict(q) for q in data.get("questions", [])]
        return Questionnaire(
            student_id=data["student_id"],
            questionnaire_id=data["questionnaire_id"],
            title=data["title"],
            description=data["description"],
            unique_url=data["unique_url"],
            answer_count=data["answer_count"],
            questions=questions
        )
