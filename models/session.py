
class Session:
    def __init__(self, session_id, title, coach, price):
        self.session_id = session_id
        self.title = title
        self.coach = coach
        self.price = price

    def __repr__(self):
        return f"Session({self.title}, {self.coach}, ${self.price})"