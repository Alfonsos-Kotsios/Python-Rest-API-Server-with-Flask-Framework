from flask import request
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

rep = Repository.instance()



@server.route('/')
def home():
    return render_template('home.html')

@server.route('/questionnaires', )
def get_questionnaires():
    sort1 = request.args.get("sort")
    questionnaires = rep.get_questionnaires()
    students = rep.get_Students()

    if sort1 == "answer_count":
        questionnaires = sorted(questionnaires, key=lambda q: q.answer_count, reverse=True)
    if sort1 == "answer_count_desc":
        questionnaires = sorted(questionnaires, key=lambda q: q.answer_count, reverse=False)
    

    return render_template("questionnaires.html", questionnaires=questionnaires, students=students)

@server.route("/questionnaires/search")
def search_questionnaires():
    students = rep.get_Students()
    title = request.args.get("title")
    min_answers = request.args.get("min_answers")
    max_answers = request.args.get("max_answers")
    student_name = request.args.get("student_name")
    department = request.args.get("department")
    sort = request.args.get("sort")

    

    results = rep.search_questionnaires(
       min_answers=min_answers,
       max_answers=max_answers, 
       title=title,
       student_name=student_name,
       department=department,
    )

    if sort == "answer_count":
        results = sorted(results, key=lambda q: q.answer_count, reverse=True)
    if sort == "answer_count_desc":
        results = sorted(results, key=lambda q: q.answer_count, reverse=False)

    return render_template("search_results.html", questionnaires=results, students=students)

@server.route('/questionnaire/<int:questionnaire_id>')
def view_questionnaire(questionnaire_id):
    q = rep.db["Questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    if not q:
        return render_template("error.html", message="⚠ Το ερωτηματολόγιο δεν βρέθηκε."), 404

    student = rep.db["Students"].find_one({"reg_number": q["student_id"]})
    q["student_name"] = f"{student['name']} {student['surname']}" if student else "Άγνωστος"

    return render_template("questionnaire_view.html", questionnaire=q)


@server.route("/questionnaire/<int:questionnaire_id>", methods=["POST"])
def submit_questionnaire(questionnaire_id):
    q = rep.db["Questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    if not q:
        return render_template("error.html", message="Το ερωτηματολόγιο δεν βρέθηκε."), 404

    answers = []
    for question in q["questions"]:
        key = f"answer_{question['question_num']}"
        raw_value = request.form.get(key)

        if question["type"] == "Numeric":
            try:
                content = float(raw_value)
            except ValueError:
                return render_template("error.html", message=f"Μη έγκυρη αριθμητική τιμή για την ερώτηση {question['question_num']}."), 400
        else:
            content = raw_value.strip()

        answers.append({
            "question_num": question["question_num"],
            "content": content
        })

    # Δημιουργία answered_questionnaire
    answered_doc = {
        "questionnaire_id": questionnaire_id,
        "from_student": False,  # Σε επόμενο βήμα μπορεί να γίνει δυναμικό
        "answers": answers
    }

    # Αποθήκευση απάντησης
    rep.db["Answered_questionnaires"].insert_one(answered_doc)

    # Ενημέρωση counter
    rep.db["Questionnaires"].update_one(
        {"questionnaire_id": questionnaire_id},
        {"$inc": {"answer_count": 1}}
    )

    return render_template("success.html", message="Η απάντηση καταχωρήθηκε με επιτυχία!")
