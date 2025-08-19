'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model.
All other files can import the user variable
'''
from models.story import Story
import flet as ft
import os
from constants.data_paths import app_data_path, stories_path, settings_path, active_story_path

class User:
    def __init__(self):
        

        # initialize the settings, before creating them in main
        # Also an extended flet container, so it shows up in the pins
        
        # Sets our settings to empty, and we create them in main.py since we need page reference
        self.settings = None 
        
        # Dict of all our stories. Starts with an 'empty_story'
        self.stories = {
            
        }


        self.create_new_story("default_story")
        
        # The selected story. Many part of the program call this selection
        self.active_story = self.stories['default_story']  # Default to empty story. Make this fetch a story from function in future

        # Saves our all_workspaces_rail to the user so it will always look how it was before closing the app
        # Saves their reorder, if collapsed or not, etc.
        # Main builds the actual rail, but it is an extended flet container
        self.all_workspaces_rail = ft.Container()

        self.workspace = ft.Container()

    def create_new_story(self, title: str):
        print("Create new story called")
        # Create a new story object and add it to our stories dict
        new_story = Story(title, os.path.join(stories_path, title))
        self.stories[title] = new_story
        return new_story

    

def load_user() -> User:
    # Check our user path. Active user variable??
    # If there is an active user, load them
    # Else, create a new user
    os.path.join(stories_path, user.active_story.title)

    print("load user called")
    return create_user()

def create_user() -> User:
    user = User()
    return user



user = User()