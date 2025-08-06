'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model.
All other files can import the user variable
'''
from models.story import Story
import flet as ft


class User:
    def __init__(self, username: str, email: str):
        # Email and Username
        self.username = username
        self.email = email

        # initialize the settings, before creating them in main
        # Also an extended flet container, so it shows up in the pins
        self.settings = ft.Container()
        
        # Dict of all our stories. Starts with an 'empty_story'
        self.stories = {
            'empty_story': Story("Story Title") 
        }
        
        # The selected story. Many part of the program call this selection
        self.active_story = self.stories['empty_story']  # Default to empty story. Make this fetch a story from function in future

        # Saves our all_workspaces_rail to the user so it will always look how it was before closing the app
        # Saves their reorder, if collapsed or not, etc.
        # Main builds the actual rail, but it is an extended flet container
        self.all_workspaces_rail = ft.Container()

        self.workspace = ft.Container()


    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.email == other.email
    
user = User("exp_user", "exp_email")
