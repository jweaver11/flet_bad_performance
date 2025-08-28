''' All the global variables and functions that are used to initialize the app '''

from models.story import Story
from models.settings import Settings
import flet as ft
import os

# Called on app startup in main
def init_settings(page: ft.Page):
    ''' Loads our settings from a JSON file into our rendered settings control. If none exist, creates default settings '''
    from models.settings import Settings
    from models.app import app

    # Sets our settings for our app. This will load the existing settings if they exist, otherwise create default settings
    if app.settings is None:
        app.settings = Settings(page)

# Called on app startup in main
def init_load_saved_stories(page: ft.Page):
    ''' Loads our saved stories from the json files in the stories directory. If none exist, do nothing '''
    
    from constants import data_paths
    from models.app import app
    
    
    # Check if stories directory exists
    if not os.path.exists(data_paths.stories_directory_path):
        print("Stories directory does not exist, creating it.")
        os.makedirs(data_paths.stories_directory_path)
        return

    # Iterate through all files in the stories directory
    for filename in os.listdir(data_paths.stories_directory_path):
        # For filetypes that end in .json inside of stories_directory_path
        if filename.endswith(".json"):
            # Create a new story object inside our self.stories with the title of the file (minus .json)
            story_title = filename.replace(".json", "")
            
            try:
                # Create story object - this will load its data automatically
                story = Story(story_title, page)
                app.stories[story_title] = story
                print(f"Loaded story: {story_title}")
                
            except Exception as e:
                print(f"Error loading story {story_title}: {e}")

    # Initialize each story's UI componenets
    for story in app.stories.values():
        story.startup()
        print(f"Initialized story: {story.title}")
        if story.title == app.settings.data.get('active_story', None):
            page.route = story.route    # This will call our route change function and set our story view

    page.update()

    
    

