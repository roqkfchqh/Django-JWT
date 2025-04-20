class InMemoryUserStore:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password, nickname):
        if username in self.users:
            return False
        self.users[username] = {
            "id": len(self.users) + 1,
            "username": username,
            "password": password,
            "nickname": nickname
        }
        return True
    
    def get_user(self, username):
        return self.users.get(username)
    
    def validate_credentials(self, username, password):
        user = self.get_user(username)
        return user if user and user["password"] == password else None
    
user_store = InMemoryUserStore()