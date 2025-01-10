import json
from typing import Dict

USERS_FILE = "data/users.json"

# Role Definitions
class Role:
    ADMIN = "Admin"
    USER = "User"

# Custom Exceptions
class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass

class User:
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role

    def verify_password(self, password: str) -> bool:
        return self.password == password

class AuthenticationManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> Dict[str, User]:
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
            return {
                username: User(username, user_data["password"], user_data["role"])
                for username, user_data in data.items()
            }
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self):
        with open(USERS_FILE, "w") as f:
            json.dump(
                {
                    username: {"password": user.password, "role": user.role}
                    for username, user in self.users.items()
                },
                f,
            )

    def register_user(self, username: str, password: str, role: str = Role.USER, current_user_role: str = None):
        if username in self.users:
            raise ValueError("Username already exists.")
        if role == Role.ADMIN and current_user_role != Role.ADMIN:
            raise AuthorizationError("Only admins can create admin accounts.")
        self.users[username] = User(username, password, role)
        self.save_users()

    def authenticate_user(self, username: str, password: str) -> User:
        if username not in self.users:
            raise AuthenticationError("User not found.")
        user = self.users[username]
        if not user.verify_password(password):
            raise AuthenticationError("Incorrect password.")
        return user
