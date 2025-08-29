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
    ''' Loads our saved stories from the json files in story folders within the stories directory. If none exist, do nothing '''
    
    from constants import data_paths
    from models.app import app
    
    
    # Check if stories directory exists
    if not os.path.exists(data_paths.stories_directory_path):
        print("Stories directory does not exist, creating it.")
        os.makedirs(data_paths.stories_directory_path)
        return

    # Iterate through all items in the stories directory
    for item in os.listdir(data_paths.stories_directory_path):
        item_path = os.path.join(data_paths.stories_directory_path, item)
        
        # Check if the item is a directory (story folder)
        if os.path.isdir(item_path):
            story_title = item
            
            # Look for JSON files within this story folder (ignore subdirectories)
            try:
                for file in os.listdir(item_path):
                    file_path = os.path.join(item_path, file)
                    
                    # Only process JSON files (not subdirectories)
                    if os.path.isfile(file_path) and file.endswith(".json"):
                        # Create story object - this will load its data automatically
                        story = Story(story_title, page)
                        app.stories[story_title] = story
                        #print(f"Loading story: {story_title} from {file_path}")
                        
                        #break  # Only need one JSON file per story folder
                        
            except Exception as e:
                print(f"Error loading story {story_title}: {e}")
        
        # Also handle legacy JSON files directly in the stories directory for backward compatibility
        elif item.endswith(".json"):
            story_title = item.replace(".json", "")
            
            try:
                # Create story object - this will load its data automatically
                story = Story(story_title, page)
                app.stories[story_title] = story
                #print(f"Loaded legacy story: {story_title}")
                
            except Exception as e:
                print(f"Error loading legacy story {story_title}: {e}")

    # Initialize each story's UI componenets
    for story in app.stories.values():
        story.startup()
        #print(f"Initialized story: {story.title}")
        if story.title == app.settings.data.get('active_story', None):
            page.route = story.route    # This will call our route change function and set our story view

    page.update()

    
    

