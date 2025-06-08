from typing import List, Union
import uuid

class Answer:
    def __init__(self, question_num: int, content: Union[str, float]):
        # Αριθμός ερώτησης και περιεχόμενο απάντησης (κείμενο ή αριθμός)
        self.question_num = question_num
        self.content = content

    def to_dict(self):
        # Επιστρέφει την απάντηση ως dictionary
        return {
            "question_num": self.question_num,
            "content": self.content,
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο Answer από dictionary
        return Answer(
            question_num=data["question_num"],
            content=data["content"]
        )


class AnsweredQuestionnaire:
    def __init__(self, questionnaire_id: int, from_student: bool, answers: List[Answer]):
        # Δημιουργεί μοναδικό id για το συμπληρωμένο ερωτηματολόγιο
        self.id = str(uuid.uuid4())
        # Το id του ερωτηματολογίου που απαντήθηκε
        self.questionnaire_id = questionnaire_id
        # Αν το ερωτηματολόγιο απαντήθηκε από φοιτητή ή όχι
        self.from_student = from_student
        # Λίστα με τις απαντήσεις
        self.answers = answers  

    def to_dict(self):
        # Επιστρέφει το συμπληρωμένο ερωτηματολόγιο ως dictionary
        return {
            "id": self.id,
            "questionnaire_id": self.questionnaire_id,
            "from_student": self.from_student,
            "answers": [a.to_dict() for a in self.answers]
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο AnsweredQuestionnaire από dictionary
        answers = [Answer.from_dict(a) for a in data.get("answers", [])]
        return AnsweredQuestionnaire(
            questionnaire_id=data["questionnaire_id"],
            from_student=data["from_student"],
            answers=answers
        )
