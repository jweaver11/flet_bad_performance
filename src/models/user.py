
# yada yadda
class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.email == other.email
    
    settings = {

    }

    workspaces_order = {
        
    }