# UniQ - Πληροφοριακό Σύστημα Ερωτηματολογίων

## 📑 Περιεχόμενα

- [🎯 Περιγραφή Έργου](#🎯-περιγραφή-έργου)
- [📌 Επιπλέον Παραδοχές και Παρεκκλίσεις](#📌-επιπλέον-παραδοχές-και-παρεκκλίσεις)
- [🛠️ Τεχνολογίες που Χρησιμοποιήθηκαν](#🛠️-τεχνολογίες-που-χρησιμοποιήθηκαν)
- [📂 Δομή Αρχείων](#📂-δομή-αρχείων)
- [🗃️ Περιγραφή Βάσης Δεδομένων](#🗃️-περιγραφή-βάσης-δεδομένων)
- [🚀 Εκκίνηση Συστήματος](#🚀-εκκίνηση-συστήματος)
- [🧪 Παραδείγματα Χρήσης](#🧪-παραδείγματα-χρήσης)
- [📚 Αναφορές](#📚-αναφορές)

---

## 🎯 Περιγραφή Έργου

- Το **UniQ** είναι ένα πλήρες Πληροφοριακό Σύστημα διαχείρισης και συμπλήρωσης ερωτηματολογίων φοιτητών. Αναπτύχθηκε με την χρήση Python REST API Server και Flask microframework και το σύστημα επικοινωνεί με μία βάση δεδομένων για την αποθήκευση των δεδομένων του . Αυτό το Πληροφοριακό Σύστημα λοιπόν επιτρέπει στους φοιτητές να δημιουργούν και να οργανώνουν τα ερωτηματολογιά τους , στους επισκέπτες να απαντούν εύκολα στα ερωτηματολόγια και επιτρέπει μια κεντρική διάχείρηση για όλο το σύστημα μέσω ενώς admin.
---

## 📌 Επιπλέον Παραδοχές και Παρεκκλίσεις

- Προσθέθηκε collection 'Users' για την καλύτερη διαχείρηση του συστήματος.
- Προσθέθηκε style μέσω css για την σωστή εμφάνιση του Π.Σ
- Το σύστημα επιτρέπει ανώνυμη συμπλήρωση ερωτηματολογίων.

---

## 🛠️ Τεχνολογίες που Χρησιμοποιήθηκαν

| Τεχνολογία | Περιγραφή |
|-----------|-----------|
| Python 3.11 | Γλώσσα Υλοποίησης |
| Flask | Micro-framework για API και UI |
| MongoDB | NoSQL βάση δεδομένων |
| Docker | Containerization για Flask + Mongo |
| HTML/CSS | Flask templates |
| Jinja2 | Template Engine |


---

## 📂 Δομή Αρχείων
```plaintext
📁 project_root/
│
├── app/
│   ├── model/          # Κλάσεις Python για Student, Questionnaire, Answer κ.ά.
│      ├── student.py
│      ├── user.py
│      ├── questionnaires.py
|      └── answered_questionnaires.py
|   ├── static/
│   	  ├── css/
│      		  ├── home.css
│      		  ├── questionnaires.css
│       	  └── ...
|   ├──  templates/         # HTML αρχεία Flask (Jinja2)
│         ├── home.html
│         ├── login.html
│         └── ...
│   ├── _init_.py
|   ├── repository.py   
│   ├── routes.py                # Κοινά endpoints
│   ├── routes_user.py           # Endpoints φοιτητών / χρηστών
│   └── routes_admin.py          # Endpoints διαχειριστή
│
|
├── assets/               # JSON αρχικά δεδομένα
│   ├── students.json
│   ├── questionnaires.json
│   └── answered_questionnaires.json
│
├── main.py                   # Εκκίνηση Flask app και Populate
├── populate_db.py            # Εισαγωγή αρχικών δεδομένων
├── Dockerfile                # Ορισμός Flask image
├── compose.yaml              # Εκκίνηση Flask + MongoDB
├── requirements.txt          # Python dependencies
└── README.md                 
```

## 🧩 Περιγραφή Βάσης Δεδομένων
-  Χρησιμοποιούμε την NoSql **MongoDB** για την αποθήκευση των δεδομένων μας.
- Οι βασικές συλλογές είναι:
  - `Students` (id, username, password, reg_number, department, name, surname)
  - `Users` (id, username, password, type)
  - `Questionnaires` (id, student_id, questionnaire_id, title, description, unique_url, questions[], answer_count)
  - `Answered_questionnaires` (id, questionnaire_id, from_student, answers[])

### Δομές Συλλογών
 Student
| Key | Value |
|-----------|-----------|
| id | str |
| username | str |
| password | str |
| reg_number | int |
| department | str |
| name | str |
| surname | str |

 Users
| Key | Value |
|-----------|-----------|
| id | str |
| username | str |
| password | str |
| type | str |

Questionnaires
| Key | Value |
|-----------|-----------|
| id | str |
| student_id | str |
| questionnaire_id | str |
| title  | int |
| description | str |
| unique_url | str |
| answer_count | str |
| questions | Array[question] |

Question
| Key | Value |
|-----------|-----------|
| type | str |
| description  | str |
| question_num | int |

Answered_questionnaires
| Key | Value |
|-----------|-----------|
| questionnaire_id | int |
| from_student | boolean |
| answers | Array[answer] |

Answer
| Key | Value |
|-----------|-----------|
| question_num | int |
| content | enum[ str | float ]|


### Παράδειγμα Εγγραφής Questionnaires
```json
{
  "questionnaire_id": 1,
  "title": "Wellness Survey",
  "student_id": 123,
  "questions": [
    {"type": "Numeric", "question_num": 1, "description": "How often..." }
  ],
  "answer_count": 4
}
```
### Παράδειγμα Εγγραφής Student
```json
{
  "password": "pass2",
  "reg_number": 2,
  "department": "Economics",
  "name": "Alice",
  "surname": "Smith",
  "username": "user2"
}
```
### Παράδειγμα Εγγραφής User
```json
{
  "id": "f84ee6d5-81f1-40bb-80de-3d5d6ee01a46",
  "username": "user2",
  "password": "pass2",
  "type": "student"
}
```
### Παράδειγμα Εγγραφής Answered_questionnaires
```json
{
  "questionnaire_id": 1,
  "from_student": true,
  "answers": [
    {
      "question_num": 1,
      "content": 45
    },
    {
      "question_num": 2,
      "content": 4
    }
  ]
}
```

