from flask import request
import pymongo
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from populate_db import main
rep = Repository.instance()
server.secret_key = 'a_random_key'  # Needed to use sessions

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.UniQ


@server.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
       
        user = rep.get_user_by_username(username)

        if user is not None and password == user.password:
            session['username'] = username
            session['role'] = user.type
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@server.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@server.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    error = None
    success = None

    if request.method == 'POST':
        old_pass = request.form.get("old_password")
        new_pass = request.form.get("new_password")

        user = rep.get_user_by_username(session['username'])

        if user and old_pass == user.password:
            rep.update_user_password(user.username, new_pass)
            success = "Ο κωδικός άλλαξε επιτυχώς."
        else:
            error = "Ο τρέχων κωδικός είναι λάθος."

    return render_template('change_password.html', error=error, success=success)

@server.route('/my_questionnaires')
def my_questionnaires():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    student = rep.get_student_by_username(session['username'])
    
    if not student:
        flash("Student not found", "error")
        return redirect(url_for('home'))
    questionnaires = rep.get_questionnaires_by_student(student.reg_number)
    
    return render_template('my_questionnaires.html', questionnaires=questionnaires)



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
            # Update the questionnaire title in the database
            result = rep.update_questionnaire_title(questionnaire_id, new_title)
            print("result", result)
            if result:
                success = "✅ Ο τίτλος του ερωτηματολογίου άλλαξε επιτυχώς!"
                
        else:
            error = "Σφάλμα στην εισαγωγή Τίτλου"
        print("new_title", new_title)
    return render_template("edit_title_questionnaire.html", questionnaire_id=questionnaire_id, error=error, success=success)


@server.route("/questionnaire/create", methods=["GET", "POST"])
def create_questionnaire():
    if 'username' not in session:
        return redirect(url_for('login'))

    student = rep.get_student_by_username(session['username'])
    error = None
    success = None
    

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        num_questions = int(request.form.get("num_questions"))
        questions = []

        for i in range(1, num_questions + 1):
            q_type = request.form.get(f"type_{i}")
            q_text = request.form.get(f"text_{i}")
            questions.append({
                "type": q_type,
                "description": q_text,
                "question_num": i
            })

        questionnaire_id = rep.get_next_questionnaire_id()  # implement if needed
        url = f"localhost:5000/questionnaire/{questionnaire_id}"

        questionnaire = {
            "student_id": student.reg_number,
            "questionnaire_id": questionnaire_id,
            "title": title,
            "description": description,
            "unique_url": url,
            "questions": questions,
            "answer_count": 0
        }

        if rep.create_questionnaire(questionnaire):
            success = "✅ Το ερωτηματολόγιο δημιουργήθηκε επιτυχώς!"
        else:
            error = "❌ Αποτυχία κατασκευής"

    return render_template("create_questionnaire.html" , error=error, success=success)

@server.route("/questionnaire/<questionnaire_id>/delete" )
def delete_questionnaire(questionnaire_id):
    print("questionnaire_id", questionnaire_id)
    
    if rep.delete_questionnaire_and_answers(questionnaire_id):
         return redirect(url_for("my_questionnaires"))
    else:
        
        return "Error deleting questionnaire", 500
   
@server.route("/questionnaire/<int:questionnaire_id>/answers")
def view_answers(questionnaire_id):
    if "username" not in session:
        return redirect(url_for("login"))
    

    stats = rep.get_questionnaire_answers(questionnaire_id)
    return render_template("questionnaire_answers.html", stats=stats, questionnaire_id=questionnaire_id)

