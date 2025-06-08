import os
from app import server                    
from populate_db import populate_if_needed #

# Το σημείο εκκίνησης της εφαρμογής
if __name__ == "__main__":
    # Ελέγχει αν χρειάζεται να γίνει populate η βάση και το κάνει αν χρειάζεται
    populate_if_needed()  

    # Εκκινεί τον Flask server στο host 0.0.0.0 (για να είναι προσβάσιμος από άλλα containers/μηχανήματα) και port 5000

    server.run(host="0.0.0.0", port=5000) 
