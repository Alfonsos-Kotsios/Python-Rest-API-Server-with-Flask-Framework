from typing import List, Union
import uuid

class Answer:
    def __init__(self, question_num: int, content: Union[str, float]):
        self.question_num = question_num
        self.content = content

    def to_dict(self):
        return {
            "question_num": self.question_num,
            "content": self.content,
        }

    @staticmethod
    def from_dict(data):
        return Answer(
            question_num=data["question_num"],
            content=data["content"]
        )


class AnsweredQuestionnaire:
    def __init__(self, questionnaire_id: int, from_student: bool, answers: List[Answer]):
        self.id = str(uuid.uuid4())
        self.questionnaire_id = questionnaire_id
        self.from_student = from_student
        self.answers = answers  

    def to_dict(self):
        return {
            "id": self.id,
            "questionnaire_id": self.questionnaire_id,
            "from_student": self.from_student,
            "answers": [a.to_dict() for a in self.answers]
        }

    @staticmethod
    def from_dict(data):
        answers = [Answer.from_dict(a) for a in data.get("answers", [])]
        return AnsweredQuestionnaire(
            questionnaire_id=data["questionnaire_id"],
            from_student=data["from_student"],
            answers=answers
        )
