''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project (other than constants) to avoid ciruclar import
'''

import flet as ft
import os
import json
from constants import data_paths

class Story:
    # Constructor for when new story is created
    def __init__(self, title: str):
       
        self.title = title # Gives our story a title when its created

        # Declare our active rail, but the this will be set in main since it needs a page reference
        self.active_rail = None     # Is a ft.Container

        data_paths.set_active_story_path(title)  # Set our active story path to the newly created story
        
        # Set the file path to the active story path
        self.file_path = data_paths.active_story_path

        # Our folder structure for the story
        story_folders = [
            "content",
            "characters",
            "plot_and_timeline",
            "worldbuilding",
            "drawing_board",
            "notes",
        ]
        
        # Actually creates the folders in our story path
        for folder in story_folders:
            folder_path = os.path.join(data_paths.active_story_path, folder)
            os.makedirs(folder_path, exist_ok=True)

        # Metadata for the story
        self.metadata = {
            "title": title,
            "top_pin_height": 0,
            "left_pin_width": 0,
            "main_pin_height": 0,
            "right_pin_width": 0,
            "bottom_pin_height": 0,
            "created_at": None,
            "last_modified": None
        }

        # Create story metadata file
        self.metadata_path = os.path.join(data_paths.active_story_path, "story_info.json")

        # Creates our 5 pin locations for our widgets. Initially set heights and widths for comparison logic when rendering
        self.top_pin = ft.Row(height=0, spacing=0, controls=[])
        self.left_pin = ft.Column(width=0, spacing=0, controls=[])
        self.main_pin = ft.Row(expand=True, spacing=0, controls=[])
        self.right_pin = ft.Column(width=0, spacing=0, controls=[])
        self.bottom_pin = ft.Row(height=0, spacing=0, controls=[])

        # Our master row that holds all our widgets
        self.widgets = ft.Row(spacing=0, expand=True, controls=[])

        # Master stack that holds our widgets ^ row. We add our drag targets overtop our widgets, so we use a stack here
        # And our drag targets when we start dragging widgets.
        # We use global stack like this so there is always a drag target, even if a pin is empty
        self.master_stack = ft.Stack(expand=True, controls=[self.widgets])

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters
        
        
    # Called from main when our program starts up. Needs a page reference, thats why not called here
    def startup(self, page: ft.Page):
        ''' Loads all our objects from storage (characters, chapters, etc.) and saves them to the story object'''

        print("startup called")

        # Loads our characters from file storage into our characters list
        self.load_characters(page)

        
    # Called when saving new objects to the story (characters, chapters, etc.)
    def save_object(self, obj):
        ''' Handles logic on where to save the new object in our live story object.
        Whenever a new object is created, it loads its data using its given path.
        If it has no data, it creates a new file to store data, so we don't need to save the data here.'''

        print("Save object called")

        # Called if we're saving a character object
        def save_character(obj):
            self.characters.append(obj) # Save to our characters list

        # Called if saving a chapter object
        def save_chapter(obj):
            print(obj)  # WIP

        # Handles our logic for saving objects. Checks the tag of the object to route it to correct save function
        if hasattr(obj, 'tag'):

            # Characters
            if obj.tag == "character":
                save_character(obj)

            # Chapters
            elif obj.tag == "chapter":
                save_chapter(obj)
            
            else:
                print("object does not have a valid tag dummy")

        # If no tag exists, we do nothing
        else:
            print("object has no tag at all you even bigger dummy")


    # Called when deleting an object from the story (character, chapter, etc.)
    def delete_object(self, obj):
        ''' Deletes the object from our live story object and its reference in the pins.
        We then remove its storage file from our file storage as well. '''

        print("Delete object called")

        # Called inside the delete_object method to remove the file from storage
        def delete_object_file(obj):
            ''' Grabs our objects path, and removes the associated file from storage '''

            print("delete object from file called")
            
            try:
                
                # Check if the file exists before attempting to delete
                if os.path.exists(obj.path):
                    os.remove(obj.path)
                    print(f"Successfully deleted file: {obj.path}")
                else:
                    print(f"File not found: {obj.path}")
                    
            except (OSError, IOError) as e:
                print(f"Error deleting file {obj.title}.json: {e}")
            except AttributeError as e:
                print(f"Object missing required attributes (title or path): {e}")

        # Remove from characters list if it is a character
        if hasattr(obj, 'tag') and obj.tag == "character":
            # Remove object from the characters list
            if obj in self.characters:
                self.characters.remove(obj)
    
        # Find our objects reference in the pins and remove it
        if hasattr(obj, 'pin_location'):
            if obj.pin_location == "top" and obj in self.top_pin.controls:
                self.top_pin.controls.remove(obj)
            elif obj.pin_location == "left" and obj in self.left_pin.controls:
                self.left_pin.controls.remove(obj)
            elif obj.pin_location == "main" and obj in self.main_pin.controls:
                self.main_pin.controls.remove(obj)
            elif obj.pin_location == "right" and obj in self.right_pin.controls:
                self.right_pin.controls.remove(obj)
            elif obj.pin_location == "bottom" and obj in self.bottom_pin.controls:
                self.bottom_pin.controls.remove(obj)
            else:
                print("Object not found in any pin location, cannot delete")

        # Remove the objects storage file as well
        if hasattr(obj, 'path'):
            delete_object_file(obj)

    # Called as part of the startup method during program launch
    def load_characters(self, page: ft.Page):
        ''' Loads all our characters from our characters folder and adds them to the live story object'''

        print("load characters called")
        
        # Check if the characters folder exists. Creates it if it doesn't. Handles errors on startup
        if not os.path.exists(data_paths.characters_path):
            print("Characters folder does not exist, creating it.")
            os.makedirs(data_paths.characters_path)
            return
        
        # Iterate through all files in the characters folder
        # Future needs to scan all sub categories (folders) inside the characters folder for files to load
        for filename in os.listdir(data_paths.characters_path):

            # All our objects are stored as JSON
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
                
                # Handle errors if the path is wrong
                except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                    print(f"Error loading character from {filename}: {e}")

