''' All the global variables and functions that are used to initialize the app '''

from models.story import Story
import flet as ft
import os
import json

# Called on app startup in main
def init_settings(page: ft.Page):
    ''' Loads our settings from a JSON file into our rendered settings control. If none exist, creates default settings '''
    from models.widgets.settings import Settings
    from models.app import app
    from constants import data_paths

    # Path to our settings file
    settings_file_path = os.path.join(data_paths.app_data_path, "settings.json")

    # Create settings.json with empty dict if it doesn't exist
    if not os.path.exists(settings_file_path):
        with open(settings_file_path, "w", encoding='utf-8') as f:
            json.dump({}, f)
    
    try:
        # Read the JSON file
        with open(settings_file_path, "r", encoding='utf-8') as f:
            settings_data = json.load(f)

    # If no file exists, create one with default settings
    except(FileNotFoundError):
        print("Settings file not found, creating default settings.")
        settings_data = None  # If there's an error, we will create default settings
            
    # Other errors
    except Exception as e:
        print(f"Error loading settings {settings_file_path}: {e}")
        settings_data = None  # If there's an error, we will create default settings

    # Sets our app settings to our loaded settings. If none were loaded (I.E. first launch), Settings with create its own defaults
    app.settings = Settings(page, data_paths.app_data_path, data=settings_data)


# Called on app startup in main
def init_load_saved_stories(page: ft.Page):
    ''' Loads our saved stories from the json files in story folders within the stories directory. If none exist, do nothing '''
    
    from constants import data_paths
    from models.app import app
    
    # Create the stories directory if it doesnt exist already
    os.makedirs(data_paths.stories_directory_path, exist_ok=True)
        
    # Iterate through all items in the stories directory
    for story_folder in os.listdir(data_paths.stories_directory_path):

        story_directory = os.path.join(data_paths.stories_directory_path, story_folder)
            
        # Look for JSON files within this story folder (ignore subdirectories)
        try:
            
            # Check every item (folder and file) in this story folder
            for item in os.listdir(story_directory):

                # Check for the story json data file. If it is, we'll load our story around this file data
                if item.endswith(".json"):

                    # Set the file path to this json file so we can open it
                    file_path = os.path.join(story_directory, item)

                    # Read the JSON file
                    with open(file_path, "r", encoding='utf-8') as f:
                        # Set our data to be passed into our objects
                        story_data = json.load(f)

                    # Our story title is the same as the folder
                    story_title = story_data.get("title", file_path.replace(".json", ""))
                        
                    app.stories[story_title] = Story(story_title, page, data=story_data)

                    break
                # Else, continue through the next story folder
                else:
                    continue
                    
        except Exception as e:
            print(f"Error loading story {story_title}: {e}. May not be a directory")
        

    # Initialize and load all our stories data and UI elements
    for story in app.stories.values():
        # Sets our active story to the page route. The route change function will load the stories data and UI
        if story.title == app.settings.data.get('active_story', None):
            app.settings.story = story  # Gives our settings widget the story reference it needs
            page.route = story.route    # This will call our route change function and set our story view

    page.update()

    
    

