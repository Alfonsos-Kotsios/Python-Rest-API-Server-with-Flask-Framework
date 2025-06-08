from flask import request
import pymongo
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

# Παίρνουμε το singleton instance του Repository για πρόσβαση στη βάση
rep = Repository.instance()
# Ορίζουμε το secret key για τα sessions της Flask
server.secret_key = 'a_random_key'  # Needed to use sessions

# Route για login χρήστη (student, admin, user)
@server.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
       
        # Αναζήτηση χρήστη στη βάση
        user = rep.get_user_by_username(username)

        # Έλεγχος αν υπάρχει ο χρήστης και αν ο κωδικός είναι σωστός
        if user is not None and password == user.password:
            session['username'] = username
            session['role'] = user.type
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials'
    # Επιστροφή του template login με μήνυμα λάθους αν υπάρχει
    return render_template('login.html', error=error)

# Route για logout χρήστη (καθαρίζει το session)
@server.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# Route για αλλαγή κωδικού χρήστη
@server.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # Αν δεν είναι συνδεδεμένος ο χρήστης, redirect στο login
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    success = None

    if request.method == 'POST':
        old_pass = request.form.get("old_password")
        new_pass = request.form.get("new_password")

        # Παίρνουμε τον χρήστη από τη βάση
        user = rep.get_user_by_username(session['username'])

        # Έλεγχος αν ο παλιός κωδικός είναι σωστός
        if user and old_pass == user.password:
            rep.update_user_password(user.username, new_pass)
            success = "Ο κωδικός άλλαξε επιτυχώς."
        else:
            error = "Ο τρέχων κωδικός είναι λάθος."

    # Επιστροφή του template αλλαγής κωδικού με μηνύματα
    return render_template('change_password.html', error=error, success=success)

# Route για προβολή των ερωτηματολογίων του συνδεδεμένου φοιτητή ή admin
@server.route('/my_questionnaires')
def my_questionnaires():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    student = rep.get_student_by_username(session['username'])

    # Αν είναι admin, επιστρέφει τα ερωτηματολόγια του admin (student_id=0)
    if session['role'] == "admin":
       questionnaires = rep.get_questionnaires_by_student(0)
       return render_template('my_questionnaires.html', questionnaires=questionnaires)
    if not student:
        flash("Student not found", "error")
        return redirect(url_for('home'))
    # Επιστρέφει τα ερωτηματολόγια του φοιτητή
    questionnaires = rep.get_questionnaires_by_student(student.reg_number)
    
    return render_template('my_questionnaires.html', questionnaires=questionnaires)

# Route για αλλαγή τίτλου ερωτηματολογίου
@server.route("/questionnaire/<questionnaire_id>/edit_title", methods=['GET', 'POST'])
def edit_questionnaire_title(questionnaire_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    error = None
    success = None
    print("questionnaire_id", type(questionnaire_id))

    if request.method == 'POST':
        new_title = request.form.get("new_title")
        if new_title:
            # Ενημέρωση τίτλου στη βάση
            result = rep.update_questionnaire_title(questionnaire_id, new_title)
            print("result", result)
            if result:
                success = "✅ Ο τίτλος του ερωτηματολογίου άλλαξε επιτυχώς!"
        else:
            error = "Σφάλμα στην εισαγωγή Τίτλου"
        print("new_title", new_title)
    # Επιστροφή του template με τα κατάλληλα μηνύματα
    return render_template("edit_title_questionnaire.html", questionnaire_id=questionnaire_id, error=error, success=success)

# Route για δημιουργία νέου ερωτηματολογίου (student ή admin)
@server.route("/questionnaire/create", methods=["GET", "POST"])
def create_questionnaire():
    if 'username' not in session:
        return redirect(url_for('login'))

    student = rep.get_student_by_username(session['username'])
    user = rep.get_user_by_username(session['username'])
    error = None
    success = None
    

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        num_questions = int(request.form.get("num_questions"))
        questions = []

        # Συλλογή των ερωτήσεων από τη φόρμα
        for i in range(1, num_questions + 1):
            q_type = request.form.get(f"type_{i}")
            q_text = request.form.get(f"text_{i}")
            questions.append({
                "type": q_type,
                "description": q_text,
                "question_num": i
            })

        questionnaire_id = rep.get_next_questionnaire_id()  # Παίρνει το επόμενο διαθέσιμο id
        url = f"localhost:5000/questionnaire/{questionnaire_id}"

        # Αν είναι admin, το reg_number είναι 0, αλλιώς του φοιτητή
        if session.get("role") == "admin":
            reg_number = 0
        else:
            reg_number = student.reg_number

        # Δημιουργία dictionary για το νέο ερωτηματολόγιο
        questionnaire = {
            "student_id": reg_number,
            "questionnaire_id": questionnaire_id,
            "title": title,
            "description": description,
            "unique_url": url,
            "questions": questions,
            "answer_count": 0
        }

        # Εισαγωγή του ερωτηματολογίου στη βάση
        if rep.create_questionnaire(questionnaire):
            success = "✅ Το ερωτηματολόγιο δημιουργήθηκε επιτυχώς!"
        else:
            error = "❌ Αποτυχία κατασκευής"

    # Επιστροφή του template με τα κατάλληλα μηνύματα
    return render_template("create_questionnaire.html" , error=error, success=success)

# Route για διαγραφή ερωτηματολογίου και των απαντήσεών του
@server.route("/questionnaire/<int:questionnaire_id>/delete", methods=["POST"])
def delete_questionnaire(questionnaire_id):
    # Διαγράφει το ερωτηματολόγιο και τις απαντήσεις του
    success, deleted_answers = rep.delete_questionnaire_and_answers(questionnaire_id)

    if success:
        print(f"✅ Ερωτηματολόγιο #{questionnaire_id} διαγράφηκε. {deleted_answers} απαντήσεις αφαιρέθηκαν.")
        return redirect(url_for("my_questionnaires"))
    else:
        return render_template("error.html", message="⚠ Το ερωτηματολόγιο δεν βρέθηκε ή απέτυχε η διαγραφή."), 500

# Route για προβολή στατιστικών και απαντήσεων ενός ερωτηματολογίου
@server.route("/questionnaire/<int:questionnaire_id>/answers")
def view_answers(questionnaire_id):
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Παίρνει τα στατιστικά και τις απαντήσεις από το repository
    stats = rep.get_questionnaire_answers(questionnaire_id)
    return render_template("questionnaire_answers.html", stats=stats, questionnaire_id=questionnaire_id)

