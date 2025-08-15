'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model.
All other files can import the user variable
'''
from models.story import Story
import flet as ft
import os

class User:
    def __init__(self, username: str, email: str):
        # Email and Username
        self.username = username
        self.email = email

        # Saving objects locally - Create project structure
        self.app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        
        # If FLET_APP_STORAGE_DATA is not set, use a default path
        if self.app_data_path is None:
            # Use the storage directory in the project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.app_data_path = os.path.join(project_root, "storage", "data")
        
        print(f"Using app data path: {self.app_data_path}")
        
        # Create main project structure
        self.stories_path = os.path.join(self.app_data_path, "stories")
        self.settings_path = os.path.join(self.app_data_path, "settings")
        # Makes our initial default story the active one on creation
        self.active_story_path = os.path.join(self.stories_path, "default_story") 
        
        # Create directories if they don't exist
        os.makedirs(self.stories_path, exist_ok=True)
        os.makedirs(self.settings_path, exist_ok=True)
        
        # Create empty_story folder structure
        #self.default_story_path = os.path.join(self.stories_path, "empty_story")
        #os.makedirs(self.default_story_path, exist_ok=True)
        
        # Create Story object structure folders inside empty_story
        story_folders = [
            "characters",
            "scenes", 
            "plotlines",
            #"settings",
            "notes"
        ]
        
        # Creates our folders in the active story path
        for folder in story_folders:
            folder_path = os.path.join(self.active_story_path, folder)
            os.makedirs(folder_path, exist_ok=True)
        
        # Create story metadata file
        self.story_metadata_path = os.path.join(self.active_story_path, "story_info.json")

        # initialize the settings, before creating them in main
        # Also an extended flet container, so it shows up in the pins
        self.settings = ft.Container()
        
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
        new_story = Story(title, os.path.join(self.stories_path, title))
        self.stories[title] = new_story
        self.active_story_path = new_story.file_path # Set new story as the active story path
        return new_story

    # Called when we switch to another story
    # Switches our file path to the new story
    def set_active_story_path(self, story: Story):
        story_title = Story.title
        
        print("Sett active story path called")
        if os.path.exists(self.stories_path.story_title):
            #self.active_story_path = path
            print(f"Active story path set to: {self.active_story_path}")
        else:

            print(f"Path does not exist:")


    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username and self.email == other.email
    
user = User("exp_user", "exp_email")
