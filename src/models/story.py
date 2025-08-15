''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project, or things will ciruclar import
'''

import flet as ft


class Story:
    # Constructor for when new story is created
    def __init__(self, title: str, file_path: str):
       
        self.title=title # Gives our story a title when its created
        self.file_path=file_path  # Gives us a path to save/load the story

        self.load_object_from_file("", "")


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
        


    # Add our created object to story. This will add it to any lists it should be in, pin location, etc.
    # All our story objects are extended flet containers, and require a title, pin location, tag,...
    def add_object_to_story(self, obj):
        print("Adding object in story: " + obj.title)

        # Runs to save our character to our story object, and save it to file
        def save_character(obj):
            print("save character called")
            self.characters.append(obj)
            self.save_object_to_file(obj)

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


    # Called when we need to save new objects or changes to existing objects
    # Handles saving our object to a file for permanent data storage
    # Updates existing objects, creates new objects if they don't exist
    def save_object_to_file(self, obj):
        print("object saved to file called")

        
    # Load an object from file
    def load_object_from_file(self, file_path, page_reference):
        """Load a saved object from file"""
        print("load object from file called")



    # Delete an object from the story. Only works for certain objects
    def delete_object_from_story(self, obj):
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
            

        # delete_from_file()




# Add all this to user file??
# Save stories locally - folder structure:
# user/stories/story_name/
# - characters/character
# - workspace_name/...