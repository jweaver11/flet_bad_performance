''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project, or things will ciruclar import
'''

import flet as ft
import os
import json
from constants import data_paths

class Story:
    # Constructor for when new story is created
    def __init__(self, title: str):
       
        self.title=title # Gives our story a title when its created

        data_paths.set_active_story_path(title)  # Set our active story path to the newly created story
        
        # Set the file path to the active story path
        self.file_path = data_paths.active_story_path

        self.load_object_from_file("", "")

        # Create Story object structure folders inside empty_story
        story_folders = [
            "content",
            "characters",
            "plot_and_timeline",
            "worldbuilding",
            "drawing_board",
            "notes",
        ]
        
        # Creates our folders in the active story path
        for folder in story_folders:
            folder_path = os.path.join(data_paths.active_story_path, folder)
            os.makedirs(folder_path, exist_ok=True)



        # Metadata for the story
        self.metadata = {
            "title": title,
            "character_count": int,
            "created_at": None,
            "last_modified": None
        }
        # Create story metadata file
        self.metadata_path = os.path.join(data_paths.active_story_path, "story_info.json")


        self.top_pin = ft.Row(height=0, spacing=0, controls=[])
        self.left_pin = ft.Column(width=0, spacing=0, controls=[])
        self.main_pin = ft.Row(expand=True, spacing=0, controls=[])
        self.right_pin = ft.Column(width=0, spacing=0, controls=[])
        self.bottom_pin = ft.Row(height=0, spacing=0, controls=[])

        # Our master row that holds all our widgets
        self.widgets = ft.Row(spacing=0, expand=True, controls=[])

        # Master stack that holds our widgets
        # And our drag targets when we start dragging widgets.
        # We do this so there is a receiver (drag target) for the widget even if a pin is empty and hidden
        self.master_stack = ft.Stack(expand=True, controls=[self.widgets])


        # Default active workspace rail if none selected/on startup rn
        self.default_rail = [ft.TextButton("Select a workspace")]

        # Map of all the workspace rails - Rails must be a list of flet controls
        self.workspace_rails = {
            0: self.default_rail,
        }  

        # Format our active rail 
        self.active_rail = ft.Column(  
            spacing=0,
            controls=self.workspace_rails[0],    # On startup, set to char rail
        )  

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters
        
        # Store page reference for loading objects later
        self.page_reference = None

    # Called when a story is loaded. Loads all our objects from files
    def startup(self, page: ft.Page):
        print("startup called")
        self.load_characters(page)
        # Load all our objects from our story file.
        # For char in filepath/characters, append to self.characters
        #...
        


    # Add our created object to story. This will add it to any lists it should be in, pin location, etc.
    # All our story objects are extended flet containers, and require a title, pin location, tag,...
    def save_object(self, obj):
        print("Adding object in story: " + obj.title)

        # Runs to save our character to our story object, and save it to file
        def save_character(obj):
            print("save character called")
 
            self.characters.append(obj) # Saves 

        # Is called when the parent f
        def save_chapter(obj):
            print("save chapter called")
            print(obj)


        # Checks our objects tag, then figures out what to do with it
        if hasattr(obj, 'tag'):
            # Characters
            if obj.tag == "character":
                save_character(obj)
            # Chapters
            elif obj.tag == "chapter":
                save_chapter(obj)
            
            else:
                print("object does not have a valid tag")


        # If no tag exists, we do nothing
        else:
            print("obj has no tag, did not save it")

        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets()

    # Deletes an object from the story, and calls function to remove it from file
    def delete_object(self, obj):
        print("Removing object from story: " + obj.title)

    
        # Remove from characters list if it is a character
        if hasattr(obj, 'tag') and obj.tag == "character":
            # Chck our characters pin location, and remove its reference from there
            if hasattr(obj, 'pin_location'):
                if obj.pin_location == "top":
                    self.top_pin.controls.remove(obj)
                elif obj.pin_location == "left":
                    self.left_pin.controls.remove(obj)
                elif obj.pin_location == "main":
                    self.main_pin.controls.remove(obj)
                elif obj.pin_location == "right":
                    self.right_pin.controls.remove(obj)
                elif obj.pin_location == "bottom":
                    self.bottom_pin.controls.remove(obj)
            # Remove object from the characters list
            if obj in self.characters:
                self.characters.remove(obj)


    # Called by tthe save_object method to save the object to file storage
    def save_object_to_file(self, obj, file_path):
        print("object saved to file called")
        
    # Load an object from file
    def load_object_from_file(self, file_path, page_reference):
        print("load object from file called")

    # Called by the delete object method to permanently remove the object from file storage as well
    def delete_object_from_file(self, obj, file_path):
        print("delete object from file called")

    def load_characters(self, page: ft.Page):
        print("load characters called")
        
        
        # Check if the characters folder exists
        if not os.path.exists(data_paths.characters_path):
            print("Characters folder does not exist, creating it.")
            os.makedirs(data_paths.characters_path)
            return
        
        # Iterate through all files in the characters folder
        for filename in os.listdir(data_paths.characters_path):
            if filename.endswith(".json"):
                file_path = os.path.join(data_paths.characters_path, filename)
                
                try:
                    # Read the JSON file
                    with open(file_path, "r") as f:
                        character_data = json.load(f)
                    
                    # Extract the title from the data
                    character_title = character_data.get("title", filename.replace(".json", ""))
                    
                    # Create Character object with the title
                    from models.character import Character
                    character = Character(character_title, page)
                    self.characters.append(character)
                    
                    print(f"Loaded character: {character_title}")
                    
                except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                    print(f"Error loading character from {filename}: {e}")
                    # Optionally, you could still create a character with just the filename
                    # character_title = filename.replace(".json", "")
                    # character = Character(character_title, page)
                    # self.characters.append(character)

