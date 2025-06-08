import uuid

class User:
    def __init__(self, username: str, password: str, user_type: str):
        # Αρχικοποιεί ένα αντικείμενο User με username, password και τύπο χρήστη
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.type = user_type  # "admin", "student", or "user"

    def to_dict(self):
        # Επιστρέφει τα στοιχεία του χρήστη ως dictionary
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "type": self.type
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο User από dictionary δεδομένων
        user = User(
            username=data["username"],
            password=data["password"],
            user_type=data["type"]
        )
        # Ενημερώνει το id αν υπάρχει στο dictionary, αλλιώς δημιουργεί νέο
        user.id = data.get("id", str(uuid.uuid4()))
        return user
