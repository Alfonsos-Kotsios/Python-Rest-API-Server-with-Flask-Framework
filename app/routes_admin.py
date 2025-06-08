from flask import request
import pymongo
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

import uuid

# Παίρνουμε το singleton instance του Repository για πρόσβαση στη βάση
rep = Repository.instance()
# Ορίζουμε το secret key για τα sessions της Flask
server.secret_key = 'a_random_key'  # Needed to use sessions

# Route για δημιουργία νέου φοιτητή (μόνο για admin)
@server.route("/admin/create_student", methods=["GET", "POST"])
def create_student():
    # Έλεγχος αν ο χρήστης είναι admin, αλλιώς redirect στη login
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    error, success = None, None

    # Αν το request είναι POST, επεξεργαζόμαστε τα δεδομένα της φόρμας
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

        # Προσπαθούμε να δημιουργήσουμε τον φοιτητή στη βάση
        if rep.create_student(data):
            success = "Ο φοιτητής δημιουργήθηκε επιτυχώς."
        else:
            error = "Το username χρησιμοποιείται ήδη."

    # Επιστρέφει το template με τα κατάλληλα μηνύματα
    return render_template("create_student.html", error=error, success=success)

# Route για διαγραφή φοιτητή (μόνο για admin)
@server.route("/admin/delete_student", methods=["GET", "POST"])
def delete_student():
    # Έλεγχος αν ο χρήστης είναι admin, αλλιώς redirect στη login
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    error = None
    success = None

    # Αν το request είναι POST, επεξεργαζόμαστε τα δεδομένα της φόρμας
    if request.method == "POST":
        reg_number = request.form.get("reg_number")
        
        # Έλεγχος εγκυρότητας αριθμού μητρώου
        if reg_number and reg_number.isdigit():
            # Προσπαθούμε να διαγράψουμε τον φοιτητή από τη βάση
            if rep.delete_student_by_reg_number(int(reg_number)):
                success = f"Ο φοιτητής με AM {reg_number} διαγράφηκε επιτυχώς."
            else:
                error = "Δεν βρέθηκε φοιτητής με αυτό τον αριθμό."
        else:
            error = "Μη έγκυρος αριθμός μητρώου."

    # Επιστρέφει το template με τα κατάλληλα μηνύματα
    return render_template("delete_student.html", error=error, success=success)
