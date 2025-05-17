
class User:
    def __init__(self, user_id, name, email, role='student'):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def __repr__(self):
        return f"User({self.name}, {self.email}, {self.role})"