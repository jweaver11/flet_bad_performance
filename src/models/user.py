from models.story import Story
import flet as ft
# yada yadda

class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        
        self.stories = {
            'empty_story': Story("Story Title") 
        }
        self.active_story = self.stories['empty_story']  # Default to empty story. Make this fetch a story from function in future

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.email == other.email
    

    # Settings the user can change
    settings = {

    }

    workspaces_order = {
        
    }




user = User("exp_user", "exp_email")
