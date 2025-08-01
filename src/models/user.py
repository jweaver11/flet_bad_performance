from models.story import Story
import flet as ft
# yada yadda

class User:
    def __init__(self, username: str, email: str):
        # Sets our username and email
        self.username = username
        self.email = email
        
        # Story related varaibles
        self.stories = {
            'empty_story': Story("Story Title") 
        }
        self.active_story = self.stories['empty_story']  # Default to empty story. Make this fetch a story from function in future

        # All workspaces rail on the left of screen related variables
        self.all_workspaces_rail = ft.Container()
        self.all_workspaces_rail_is_reorderable = False
        self.all_workspaces_rail_is_collapsed = False
        


    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.email == other.email
    

    # Settings the user can change
    settings = {

    }

    def test_function(self, page: ft.Page):
        print("test function was called")

# Loads our user, or creates a new one if we need to
def load_user():

    #if user == None:
        # create new user
    # else:
        #logic to load a user. For now, just create one and be done with it

    user = User("example_user", "example_email")

    return user


user = load_user()
