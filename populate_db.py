# populate_db.py
# Αρχείο για την αρχικοποίηση (populate) της βάσης δεδομένων με δεδομένα από αρχεία JSON

import pymongo
import json
import os

from app.model.student import Student
from app.model.answered_questionnaires import AnsweredQuestionnaire
from app.model.questionnaires import Questionnaire
from app.model.user import User

def populate_if_needed():
    # Παίρνει τα περιβαλλοντικά variables για host και όνομα βάσης (ή default τιμές)
    mongo_host = os.environ.get("MONGO_HOST", "localhost")
    mongo_db_name = os.environ.get("MONGO_DATABASE", "ERGASIA")

    # Δημιουργεί σύνδεση με τη MongoDB
    client = pymongo.MongoClient(f"mongodb://{mongo_host}:27017/")
    db = client[mongo_db_name]

    # ✅ Αν υπάρχουν ήδη φοιτητές στη βάση, δεν κάνει populate (αποφυγή διπλοεγγραφών)
    if db["Students"].count_documents({}) > 0:
        print("✅ Database already populated. Skipping.")
        return

    # --- Εισαγωγή φοιτητών από το students.json ---
    with open(os.path.join("assets", "students.json"), "r") as students_file:
        raw_students = json.load(students_file)  # Διαβάζει τα δεδομένα από το αρχείο
        students = [Student(**s) for s in raw_students]  # Δημιουργεί αντικείμενα Student
        db["Students"].insert_many([s.to_dict() for s in students])  # Εισάγει στη βάση
        print(len(students), "Students created")

    # --- Εισαγωγή απαντημένων ερωτηματολογίων από το answered_questionnaires.json ---
    with open(os.path.join("assets", "answered_questionnaires.json"), "r") as a_file:
        answered_questionnaires = json.load(a_file)
        db["Answered_questionnaires"].insert_many(answered_questionnaires)
        print(len(answered_questionnaires), "Answered_questionnaires created")

    # --- Εισαγωγή ερωτηματολογίων από το questionnaires.json ---
    with open(os.path.join("assets", "questionnaires.json"), "r") as q_file:
        questionnaires = json.load(q_file)
        db["Questionnaires"].insert_many(questionnaires)
        print(len(questionnaires), "Questionnaires created")

    # --- Εισαγωγή χρηστών (students + admin) στη βάση Users ---
    users = [User(s.username, s.password, "student").to_dict() for s in students]  # Δημιουργεί χρήστες για κάθε φοιτητή
    users.append(User("admin", "admin123", "admin").to_dict())  # Προσθέτει τον admin
    db["Users"].insert_many(users)
    print(len(users), "Users created (students + admin)")
