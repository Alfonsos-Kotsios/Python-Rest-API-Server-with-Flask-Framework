from flask import Flask
from pymongo import MongoClient
from flask import render_template

app = Flask(__name__)

    # MongoDB Setup (χωρίς χρήση .env)
mongo_url = "mongodb://mongo:27017"
client = MongoClient(mongo_url)
app.db = client["UniQ"]

app.run(host="localhost", port=5000, debug=True)


