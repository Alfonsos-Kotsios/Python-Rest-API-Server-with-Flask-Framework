# UniQ - Πληροφοριακό Σύστημα Ερωτηματολογίων


## 📑 Περιεχόμενα

- [🎯 Περιγραφή Έργου](#περιγραφή-έργου)
- [📌 Επιπλέον Παραδοχές και Παρεκκλίσεις](#επιπλέον-παραδοχές-και-παρεκκλίσεις)
- [🛠️ Τεχνολογίες που Χρησιμοποιήθηκαν](#τεχνολογίες-που-χρησιμοποιήθηκαν)
- [📂 Δομή Αρχείων](#δομή-αρχείων)
- [🗃️ Περιγραφή Βάσης Δεδομένων](#περιγραφή-βάσης-δεδομένων)
- [🚀 Εκκίνηση Συστήματος](#εκκίνηση-συστήματος)
- [🧪 Παραδείγματα Χρήσης](#παραδείγματα-χρήσης)
- [📚 Αναφορές](#αναφορές)


---

## 🎯 Περιγραφή Έργου

- Το **UniQ** είναι ένα πλήρες Πληροφοριακό Σύστημα διαχείρισης και συμπλήρωσης ερωτηματολογίων φοιτητών. Αναπτύχθηκε με την χρήση Python REST API Server και Flask microframework και το σύστημα επικοινωνεί με μία βάση δεδομένων για την αποθήκευση των δεδομένων του . Αυτό το Πληροφοριακό Σύστημα λοιπόν επιτρέπει στους φοιτητές να δημιουργούν και να οργανώνουν τα ερωτηματολόγια τους , στους επισκέπτες να απαντούν εύκολα στα ερωτηματολόγια και επιτρέπει μια κεντρική διαχείριση για όλο το σύστημα μέσω ενός Admin.
---

## 📌 Επιπλέον Παραδοχές και Παρεκκλίσεις

- Προστέθηκε collection 'Users' για την καλύτερη διαχείριση του συστήματος.
- Προστέθηκε style μέσω css για την σωστή εμφάνιση του Π.Σ
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
## 🚀 Εκκίνηση Συστήματος

Για να εκκινήσετε το σύστημα δημιουργήστε έναν φάκελο και στην συνέχεια στο cmd του φακέλου ακολουθήστε τις 
παρακάτω εντολές.

```bash
git clone https://github.com/Alfonsos-Kotsios/UNIQ.git
cd UNIQ
docker compose up -d --build
```
Αυτό:
- Φορτώνει MongoDB και Flask API server.
- Εκτελεί `populate_db.py` ΜΟΝΟ αν η βάση δεν έχει δεδομένα.

## 🧪 Παραδείγματα Χρήσης

Το λειτουργικό σύστημα έχει τρεις τρόπους χρήσης :
- Απλός χρήστης
- Student
- Admin

### Ας αρχίσουμε με το παράδειγμα χρήσης για έναν **Απλό Χρήστη**:

#### Μόλις ένας χρήστης μπει στην σελίδα έχει την δυνατότητα να δει τα διαθέσιμα ερωτηματολόγια και φυσικά μπορεί να προσθέσει φίλτρα αναζήτησης για να βρει το ερωτηματολόγιο που θέλει.

![image](https://github.com/user-attachments/assets/c934ec5a-0a97-450e-81aa-2e47137dd277)

![image](https://github.com/user-attachments/assets/bb154dc5-623e-48bb-a9ac-b64fd0b62abc)

![image](https://github.com/user-attachments/assets/f886e68c-d526-4b58-9557-daa97d72ec51)

#### Φυσικά έχει τις επιλογές να κατατάξει τα ερωτηματολόγια σε αύξουσα ή σε φθίνουσα σειρά με βάση τις απαντήσεις του.

![image](https://github.com/user-attachments/assets/c2125a9a-95ef-4bd3-a222-8b8b87196aac) ![image](https://github.com/user-attachments/assets/a89f674a-0c19-474f-a3f4-24d6534d58c5)



#### Αφού βρει το ερωτηματολόγιο που τον ενδιαφέρει μπορεί να πατήσει προβολή και να προχωρήσει στην συμπλήρωση των απαντήσεων.

![image](https://github.com/user-attachments/assets/8b0d94a3-f5d4-40ee-93b2-3dacc1e992d7)

![image](https://github.com/user-attachments/assets/0d933aac-ca1e-4509-a887-359ed0a5e8b7)

![image](https://github.com/user-attachments/assets/1fe041bf-4ed5-43c4-9437-6d9fb4047c5a)

### Παράδειγμα χρήσης για έναν **Student**:

#### Ένας student πρέπει να μεταβεί στην επιλογή είσοδος ώστε να συνδεθεί με τα στοιχεία του. Στην συνέχεια εμφανίζονται όλες οι πρόσθετες επιλογές που έχει. Φυσικά μπορεί να πραγματοποιήσει όλες τις ενέργειες ενός απλού χρήστη.

#### Επιπλέον ενέργειες: 
- Αλλαγή Κωδικού
- Κατασκευή Ερωτηματολογίου
- Προβολή ερωτηματολογίων Φοιτητή

![image](https://github.com/user-attachments/assets/cdc38d5a-faec-420e-99bc-dbfa0797beb4)
![image](https://github.com/user-attachments/assets/4c3512cc-4a78-46a7-a7a1-12056450172d)

#### Στην  επιλογή "αλλαγή κωδικού" ο χρήστης εισάγει των τρέχων κωδικό του και στην συνέχεια έναν καινούριο ώστε να γίνει η αλλαγή.

![image](https://github.com/user-attachments/assets/49c5b240-76f6-4ffe-b272-964599c191c2)

#### Στην  επιλογή "Προβολή ερωτηματολογίων Φοιτητή" ο χρήστης μπορεί να δει τα ερωτηματολόγια του , να αλλάξει τον τίτλο τους , να προβάλει τις απαντήσεις που έχει λάβει και να τα διαγράψει.

![image](https://github.com/user-attachments/assets/55327ab3-90b0-4291-82f2-6752c4303f52)

![image](https://github.com/user-attachments/assets/5d13cd2c-4e00-4951-aa6b-a57455c8c3b3)

![image](https://github.com/user-attachments/assets/3cff014e-a561-49ab-833e-b4c70036c5aa)

#### Στην  επιλογή "Κατασκευή Ερωτηματολογίου" ο χρήστης μπορεί να Κατασκευάσει ένα νέο ερωτηματολόγιο και να το προσθέσει στην συλλογή του , στην συνέχεια μπορεί να πραγματοποίηση όλες τις παραπάνω ενέργειες.

![image](https://github.com/user-attachments/assets/7a290066-772d-42a8-b6cb-fea4e298794c)

![image](https://github.com/user-attachments/assets/5550f06c-ac0b-4596-a204-9d2dd479d530)

![image](https://github.com/user-attachments/assets/f27b55d9-d5fe-4f33-a6e6-4d67a90a7783)

![image](https://github.com/user-attachments/assets/85ea5dc2-3733-4667-9156-d795ceab7ef1)


### Παράδειγμα χρήσης για έναν **Admin**:

#### Για να συνδεθεί ο Admin στο σύστημα πρέπει να εισάγει τα στοιχεία username: Admin , password: admin123 . O Admin μπορεί να πραγματοποιήσει όλες τις λειτουργείες του student και του απλού χρήστη αλλά έχει και επιπλέον επιλογές.

#### Επιπλέον ενέργειες: 
- Διαγραφή ερωτηματολογίων όλων των φοιτητών
- Δημιουργία νέου φοιτητή
- Διαγραφή φοιτητή

####  Μπορεί να μεταβεί στην επιλογή "Προβολή Ερωτηματολογίων" και από εκεί να διαγράψει όποιο ερωτηματολόγιο θέλει.

![image](https://github.com/user-attachments/assets/aa1ffd08-b03b-4534-8a59-6ef25533a6df)

![image](https://github.com/user-attachments/assets/8e1de0d1-c288-4579-818b-45af8d85f775)

#### Στην επιλογή "Δημιουργία Νέου Φοιτητή" δημιουργεί έναν νέο φοιτητή με όλα τα απαραίτητα στοιχεία. 

![image](https://github.com/user-attachments/assets/ebc822db-814d-4d72-9ae7-9257509a4417)

![image](https://github.com/user-attachments/assets/1c7c4e7e-75a0-4664-ba65-a88d7a8576f6)

![image](https://github.com/user-attachments/assets/a0f5ee25-1437-42a1-954e-f31fa5f11bc8)

#### Στην επιλογή "Διαγραφή Φοιτητή"  ο Admin με βάση τον αριθμό μητρώου διαγράφει όποιον φοιτητή θέλει. 

![image](https://github.com/user-attachments/assets/8fc2404a-1d39-4755-a20b-8e7051ea7822)


## 📚 Αναφορές

Η υλοποίηση του συστήματος βασίστηκε στις παρακάτω αναφορές:
- [Infrmation System Lab](https://github.com/karamolegkos/Information-Systems-Lab)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB with PyMongo](https://pymongo.readthedocs.io/)
- [Docker + Compose](https://docs.docker.com/compose/)
- [Jinja2 Templating](https://jinja.palletsprojects.com/)
















