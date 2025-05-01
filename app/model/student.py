# app/models/student.py
import uuid

class Student:
    def __init__(self, username: str, password: str, reg_number: int,
                 department: str, name: str, surname: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.reg_number = reg_number
        self.department = department
        self.name = name
        self.surname = surname

    def __eq__(self, other):
        return self.reg_number == other.reg_number

    def __str__(self):
        return f"{self.reg_number} - {self.name} {self.surname} ({self.username})"

    def __repr__(self):
        return (f"Student('{self.id}', '{self.username}', '{self.password}', "
                f"{self.reg_number}, '{self.department}', '{self.name}', '{self.surname}')")

    def to_dict(self):
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
        student = Student(
            username=data.get("username"),
            password=data.get("password"),
            reg_number=data.get("reg_number"),
            department=data.get("department"),
            name=data.get("name"),
            surname=data.get("surname")
        )
        student.id = data.get("id", student.id)
        return student