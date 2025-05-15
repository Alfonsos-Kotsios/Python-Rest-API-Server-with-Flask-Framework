from flask import request
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

rep = Repository.instance()
server.secret_key = 'a_random_key'  # Needed to use sessions


@server.route('/')
def home():
   
    print("session", session)
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

    sort_flag = sort in ["answer_count", "answer_count_desc"]
    descending = (sort == "answer_count")  # descending=True only if sort=answer_count

    if min_answers:
        
        if int(min_answers) < 0 or int(max_answers) < 0:
            return render_template("error.html", message="⚠ Ο αριθμός απαντήσεων δεν μπορεί να είναι αρνητικός."), 400
    
    if max_answers:
        
        if  int(max_answers) < 0:
            return render_template("error.html", message="⚠ Ο αριθμός απαντήσεων δεν μπορεί να είναι αρνητικός."), 400

    results = rep.search_questionnaires(
        min_answers=min_answers,
        max_answers=max_answers,
        title=title,
        student_name=student_name,
        department=department,
        sort_by_answer_count=sort_flag,
        descending=descending
    )

    
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

    # Χωρίς login -> ελέγχει αν είναι student μέσω session (αν υπάρχει), αλλιώς False
    if session.get("role") == "student":
        from_student = True
        print("session", session)
    else:
        from_student = False
        print("session", session)

    print("from_student", from_student)

    answered_doc = {
        "questionnaire_id": questionnaire_id,
        "from_student": from_student,
        "answers": answers
    }

    rep.db["Answered_questionnaires"].insert_one(answered_doc)

    rep.db["Questionnaires"].update_one(
        {"questionnaire_id": questionnaire_id},
        {"$inc": {"answer_count": 1}}
    )

    return render_template("success.html", message="Η απάντηση καταχωρήθηκε με επιτυχία!")


