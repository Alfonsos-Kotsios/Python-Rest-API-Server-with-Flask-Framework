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

    def from_dict(self, data):
        self.id = data.get("id", self.id)
        self.username = data.get("username", self.username)
        self.password = data.get("password", self.password)
        self.reg_number = data.get("reg_number", self.reg_number)
        self.department = data.get("department", self.department)
        self.name = data.get("name", self.name)
        self.surname = data.get("surname", self.surname)
