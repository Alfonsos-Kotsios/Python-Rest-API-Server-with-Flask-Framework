import uuid

class Student:
    def __init__(self, username: str, password: str, reg_number: int,
                 department: str, name: str, surname: str):
        # Αρχικοποιεί ένα αντικείμενο Student με τα βασικά στοιχεία του φοιτητή
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.reg_number = reg_number
        self.department = department
        self.name = name
        self.surname = surname

    def __eq__(self, other):
        # Ελέγχει αν δύο αντικείμενα Student έχουν τον ίδιο αριθμό μητρώου
        return self.reg_number == other.reg_number

    def __str__(self):
        # Επιστρέφει αναπαράσταση του φοιτητή ως string για ευανάγνωστη εμφάνιση
        return f"{self.reg_number} - {self.name} {self.surname} ({self.username})"

    def __repr__(self):
        # Επιστρέφει αναλυτική αναπαράσταση του φοιτητή για debugging
        return (f"Student('{self.id}', '{self.username}', '{self.password}', "
                f"{self.reg_number}, '{self.department}', '{self.name}', '{self.surname}')")

    def to_dict(self):
        # Επιστρέφει τα στοιχεία του φοιτητή ως dictionary
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "reg_number": self.reg_number,
            "department": self.department,
            "name": self.name,
            "surname": self.surname,
        }

    @staticmethod
    def from_dict(data):
        # Δημιουργεί αντικείμενο Student από dictionary δεδομένων
        student = Student(
            username=data["username"],
            password=data["password"],
            name=data["name"],
            surname=data["surname"],
            reg_number=data["reg_number"],
            department=data["department"]
        )
        # Ενημερώνει το id αν υπάρχει στο dictionary
        student.id = data.get("id", student.id)
        return student