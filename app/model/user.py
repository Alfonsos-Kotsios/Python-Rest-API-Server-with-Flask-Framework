# app/models/user.py

import uuid

class User:
    def __init__(self, username: str, password: str, user_type: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.type = user_type  # "admin", "student", or "user"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "type": self.type
        }

    @staticmethod
    def from_dict(data):
        user = User(
            username=data["username"],
            password=data["password"],
            user_type=data["type"]
        )
        user.id = data.get("id", str(uuid.uuid4()))
        return user
