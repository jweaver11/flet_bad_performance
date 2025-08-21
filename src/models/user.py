'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model.
All other files can import the user variable
'''
from models.story import Story

class User:
    def __init__(self):

        # Sets some global variables that we access elsewhere, but need to be declared here.
        # They require a page reference upon creations, so main.py creates them everytime
        self.settings = None
        self.all_workspaces_rail = None   # All workspaces rail
        
        # Dict of all our stories. Starts with an 'empty_story'
        self.stories = {
            
        }

        self.create_new_story("default_story")
        
        # The selected story. Many part of the program call this selection
        self.active_story = self.stories['default_story']  # Default to empty story. Make this fetch a story from function in future


       

    # Called when user creates a new story
    def create_new_story(self, title: str):
        
        # Create a new story object and add it to our stories dict
        new_story = Story(title)
        self.stories[title] = new_story
        return new_story


    

def load_user() -> User:
    # Check our user path. Active user variable??
    # If there is an active user, load them
    # Else, create a new user

    print("load user called")
    return create_user()

def create_user() -> User:
    
    user = User()
    
    return user



user = User()