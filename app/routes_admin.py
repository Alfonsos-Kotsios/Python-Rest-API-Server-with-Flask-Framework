from flask import request
import pymongo
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from populate_db import main
import uuid

rep = Repository.instance()
server.secret_key = 'a_random_key'  # Needed to use sessions

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.UniQ


@server.route("/admin/create_student", methods=["GET", "POST"])
def create_student():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    error, success = None, None

    if request.method == "POST":
        data = {
            "id": str(uuid.uuid4()),
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "reg_number": int(request.form.get("reg_number")),
            "department": request.form.get("department"),
            "name": request.form.get("name"),
            "surname": request.form.get("surname")
        }

        if rep.create_student(data):
            success = "Ο φοιτητής δημιουργήθηκε επιτυχώς."
        else:
            error = "Το username χρησιμοποιείται ήδη."

    return render_template("create_student.html", error=error, success=success)

@server.route("/admin/delete_student", methods=["GET", "POST"])
def delete_student():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    error = None
    success = None

    if request.method == "POST":
        reg_number = request.form.get("reg_number")
        
        if reg_number and reg_number.isdigit():
            if rep.delete_student_by_reg_number(int(reg_number)):
                success = f"Ο φοιτητής με AM {reg_number} διαγράφηκε επιτυχώς."
            else:
                error = "Δεν βρέθηκε φοιτητής με αυτό τον αριθμό."
        else:
            error = "Μη έγκυρος αριθμός μητρώου."

    return render_template("delete_student.html", error=error, success=success)
