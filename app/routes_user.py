from flask import request
from app import server
from app.repository import Repository
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient

rep = Repository.instance()




@server.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.args.get("username")
        password = request.args.get("password")
       

        if username == 'admin' and password == 'admin123':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@server.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


