''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project, or things will ciruclar import
'''

import os
import flet as ft

# Saving objects locally
app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
my_file_path = os.path.join(app_data_path, "characters.json")
#with open(my_file_path, "w") as f:
    #f.write(obj.title)  # Need to write object to json

class Story:
    # Constructor for when new story is created
    def __init__(self, title: str):
       
       # Gives our story a title when its created
        self.title=title
       

        # Hold a reference object (pointer) of our story objects (Which are all extended flet containers)
        # The pins are rows/columns that need to hold tabs, that then hold our objects, which are extended flet tabs
        #self.top_pin = ft.Row(spacing=0, height=0, controls=[],)
        #self.left_pin = ft.Column(spacing=0, width=0, controls=[])
        #self.main_pin = ft.Row(spacing=0, expand=True, controls=[ft.Tabs()])
        #self.right_pin = ft.Column(spacing=0, width=0, controls=[])
        #self.bottom_pin = ft.Row(spacing=0, height=0, controls=[])

        self.top_pin = ft.Tabs(selected_index=0, height=0)
        self.left_pin = ft.Tabs(selected_index=0, width=0)
        self.main_pin = ft.Tabs(selected_index=0)
        self.right_pin = ft.Tabs(selected_index=0, width=0)
        self.bottom_pin = ft.Tabs(selected_index=0, height=0)

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

            # Checks our pin location and then adds it to a pin
            if hasattr(obj, 'pin_location'):  
                self.add_object_to_pin(obj)

            # If object has no pin location, we don't pin it anywhere
            else:
                print("Object does not have a pin location, did not pin to story")

        # If no tag exists, we do nothing
        else:
            print("obj has no tag, did not save it")


    # Adds our object to one of our five pin locations
    def add_object_to_pin(self, obj):
        print("add object to pin called")

        # check objects pin and that its not already in that pin
        if obj.pin_location == "top" and obj not in self.top_pin.controls:
            self.top_pin.controls.append(obj)
        elif obj.pin_location == "left" and obj not in self.left_pin.controls:
            self.left_pin.controls.append(obj)
        elif obj.pin_location == "main" and obj not in self.main_pin.tabs:
            self.main_pin.tabs.append(obj)
        elif obj.pin_location == "right" and obj not in self.right_pin.controls:
            self.right_pin.controls.append(obj)
        elif obj.pin_location == "bottom" and obj not in self.bottom_pin.controls:
            self.bottom_pin.controls.append(obj)
        else:
            print("object has an invalid pin location")

    # Handles saving our object to a file for permanent data storage, not just client
    def save_object_to_file(self, obj):
        print("object saved to file called")


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


    # Workspaces within each story object
    # Description
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??



# Add all this to user file??
# Save stories locally - folder structure:
# user/stories/story_name/
# - characters/character
# - workspace_name/...