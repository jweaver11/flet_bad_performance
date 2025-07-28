''' Master Story class that contains data and methods for the entire story '''

import os
import flet as ft

# Saving objects locally
app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
my_file_path = os.path.join(app_data_path, "characters.json")
#with open(my_file_path, "w") as f:
    #f.write(obj.title)  # Need to write object to json

class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story

        # Hold a reference object (pointer) of our story objects (Which are all extended flet containers)
        self.top_pin = ft.Row(spacing=10, height=0, controls=[],)
        self.left_pin = ft.Column(spacing=10, width=0, controls=[])
        self.main_pin = ft.Row(spacing=10, expand=True, controls=[])   # no formatting needed
        self.right_pin = ft.Column(spacing=10, width=0, controls=[])
        self.bottom_pin = ft.Row(spacing=10, height=0, controls=[])

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters

    # Add our created object to story. This will add it to any lists it should be in, pin location, etc.
    # All our story objects are extended flet containers, and require a title, pin location, tag,...
    def add_object_to_story(self, obj):
        print("Adding object in story: " + obj.title)

        # Checks our pin location and then adds it to a pin
        if hasattr(obj, 'pin_location'):  
            self.add_object_to_pin(obj)
        else:
            print("Object does not have a pin location, did not pin to story")

        # Checks our objects tag, then figures out what to do with it
        if obj.tag == "character":
            self.characters.append(obj)

        # Saves our object permanently
        self.save_object_to_file(obj)


    # Handles saving our object to a file for permanent data storage, not just client
    def save_object_to_file(self, obj):
        print("object saved to file called")

    # Handles where to pin newly added objects to our story
    def add_object_to_pin(self, obj):
        # check objects pin and that its not already in that pin
        if obj.pin_location == "top" and obj not in self.top_pin.controls:
            self.top_pin.controls.append(obj)
        elif obj.pin_location == "left" and obj not in self.left_pin.controls:
            self.left_pin.controls.append(obj)
        elif obj.pin_location == "main" and obj not in self.main_pin.controls:
            self.main_pin.controls.append(obj)
        elif obj.pin_location == "right" and obj not in self.right_pin.controls:
            self.right_pin.controls.append(obj)
        elif obj.pin_location == "bottom" and obj not in self.bottom_pin.controls:
            self.bottom_pin.controls.append(obj)

    # Delete an object from the story. Only works for certain objects
    def delete_object_from_story(self, obj):
        print("Removing object from story: " + obj.title)

        # Remove from characters list if it is a character
        if hasattr(obj, 'tag') and obj.tag == "character":
            if obj in self.characters:
                self.characters.remove(obj)

        # delete_from_pin()
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