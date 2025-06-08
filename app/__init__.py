# Αρχείο αρχικοποίησης της εφαρμογής Flask

from flask import Flask

# Δημιουργία αντικειμένου Flask για την εφαρμογή
server = Flask(__name__)

# Εισαγωγή των routes της εφαρμογής (βασικά, χρήστη, διαχειριστή)
from app import routes, routes_user, routes_admin

