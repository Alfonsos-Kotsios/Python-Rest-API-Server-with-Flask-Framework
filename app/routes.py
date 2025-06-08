from flask import request
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

# Παίρνουμε το singleton instance του Repository για πρόσβαση στη βάση
rep = Repository.instance()
# Ορίζουμε το secret key για τα sessions της Flask
server.secret_key = 'a_random_key'  # Needed to use sessions

# Αρχική σελίδα της εφαρμογής
@server.route('/')
def home():
    # Εμφανίζει το session για debugging και επιστρέφει το template της αρχικής σελίδας
    print("session", session)
    return render_template('home.html')

# Route για προβολή όλων των ερωτηματολογίων με δυνατότητα ταξινόμησης
@server.route('/questionnaires', )
def get_questionnaires():
    # Παίρνει το query param για ταξινόμηση
    sort1 = request.args.get("sort")
    # Παίρνει όλα τα ερωτηματολόγια και τους φοιτητές από τη βάση
    questionnaires = rep.get_questionnaires()
    students = rep.get_Students()
    
    # Ταξινόμηση με βάση το πλήθος απαντήσεων (φθίνουσα ή αύξουσα)
    if sort1 == "answer_count":
        questionnaires = sorted(questionnaires, key=lambda q: q.answer_count, reverse=True)
    if sort1 == "answer_count_desc":
        questionnaires = sorted(questionnaires, key=lambda q: q.answer_count, reverse=False)
    
    # Επιστρέφει το template με τα ερωτηματολόγια και τους φοιτητές
    return render_template("questionnaires.html", questionnaires=questionnaires, students=students)

# Route για αναζήτηση ερωτηματολογίων με φίλτρα και ταξινόμηση
@server.route("/questionnaires/search")
def search_questionnaires():
    students = rep.get_Students()
    # Παίρνει τα φίλτρα από τα query params
    title = request.args.get("title")
    min_answers = request.args.get("min_answers")
    max_answers = request.args.get("max_answers")
    student_name = request.args.get("student_name")
    department = request.args.get("department")
    sort = request.args.get("sort")

    # Ορισμός flags για ταξινόμηση
    sort_flag = sort in ["answer_count", "answer_count_desc"]
    descending = (sort == "answer_count")  # descending=True μόνο αν sort=answer_count

    # Έλεγχος εγκυρότητας για αρνητικούς αριθμούς απαντήσεων
    if min_answers:
        if int(min_answers) < 0 or int(max_answers) < 0:
            return render_template("error.html", message="⚠ Ο αριθμός απαντήσεων δεν μπορεί να είναι αρνητικός."), 400
    
    if max_answers:
        if  int(max_answers) < 0:
            return render_template("error.html", message="⚠ Ο αριθμός απαντήσεων δεν μπορεί να είναι αρνητικός."), 400

    # Κλήση της search_questionnaires του repository με τα φίλτρα
    results = rep.search_questionnaires(
        min_answers=min_answers,
        max_answers=max_answers,
        title=title,
        student_name=student_name,
        department=department,
        sort_by_answer_count=sort_flag,
        descending=descending
    )

    # Επιστρέφει το template με τα αποτελέσματα αναζήτησης
    return render_template("search_results.html", questionnaires=results, students=students)

# Route για προβολή ενός συγκεκριμένου ερωτηματολογίου
@server.route('/questionnaire/<int:questionnaire_id>')
def view_questionnaire(questionnaire_id):
    # Βρίσκει το ερωτηματολόγιο με βάση το id
    q = rep.db["Questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    if not q:
        # Αν δεν βρεθεί, επιστρέφει σελίδα λάθους
        return render_template("error.html", message="⚠ Το ερωτηματολόγιο δεν βρέθηκε."), 404

    # Βρίσκει τον φοιτητή-δημιουργό του ερωτηματολογίου
    student = rep.db["Students"].find_one({"reg_number": q["student_id"]})
    q["student_name"] = f"{student['name']} {student['surname']}" if student else "Άγνωστος"

    # Επιστρέφει το template προβολής ερωτηματολογίου με τα δεδομένα
    return render_template("questionnaire_view.html", questionnaire=q)

# Route για υποβολή απαντήσεων σε ερωτηματολόγιο (μέθοδος POST)
@server.route("/questionnaire/<int:questionnaire_id>", methods=["POST"])
def submit_questionnaire(questionnaire_id):
    # Βρίσκει το ερωτηματολόγιο με βάση το id
    q = rep.db["Questionnaires"].find_one({"questionnaire_id": questionnaire_id})
    if not q:
        # Αν δεν βρεθεί, επιστρέφει σελίδα λάθους
        return render_template("error.html", message="Το ερωτηματολόγιο δεν βρέθηκε."), 404

    answers = []
    # Για κάθε ερώτηση του ερωτηματολογίου, παίρνει την απάντηση από τη φόρμα
    for question in q["questions"]:
        key = f"answer_{question['question_num']}"
        raw_value = request.form.get(key)

        # Αν η ερώτηση είναι αριθμητική, μετατρέπει την απάντηση σε float
        if question["type"] == "Numeric":
            try:
                content = float(raw_value)
            except ValueError:
                return render_template("error.html", message=f"Μη έγκυρη αριθμητική τιμή για την ερώτηση {question['question_num']}."), 400
        else:
            # Αλλιώς παίρνει το string (ανοικτού τύπου)
            content = raw_value.strip()
        
        answers.append({
            "question_num": question["question_num"],
            "content": content
        })

    # Ελέγχει αν ο χρήστης είναι φοιτητής (μέσω session), αλλιώς θεωρείται απλός χρήστης
    if session.get("role") == "student":
        from_student = True
        print("session", session)
    else:
        from_student = False
        print("session", session)

    print("from_student", from_student)

    # Δημιουργεί το έγγραφο απάντησης για εισαγωγή στη βάση
    answered_doc = {
        "questionnaire_id": questionnaire_id,
        "from_student": from_student,
        "answers": answers
    }

    # Εισάγει την απάντηση στη συλλογή Answered_questionnaires
    rep.db["Answered_questionnaires"].insert_one(answered_doc)

    # Αυξάνει το πλήθος απαντήσεων του ερωτηματολογίου κατά 1
    rep.db["Questionnaires"].update_one(
        {"questionnaire_id": questionnaire_id},
        {"$inc": {"answer_count": 1}}
    )

    # Επιστρέφει σελίδα επιτυχίας
    return render_template("success.html", message="Η απάντηση καταχωρήθηκε με επιτυχία!")


