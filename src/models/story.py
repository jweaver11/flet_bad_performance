''' Master Story/Project class for projects'''

import os
import flet as ft

# Saving characters locally
app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
my_file_path = os.path.join(app_data_path, "characters.json")

# Class for each seperate story/project
# Only used for data storage, methods don't pass properly to update the UI
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story

        # Hold a copy of our story objects for rendering their widgets
        self.top_pin = ft.Row(spacing=10, controls=[], height=0)
        self.left_pin = ft.Column(spacing=10, controls=[])
        self.main_pin = ft.Row(expand=True, spacing=10, controls=[])   # no formatting needed
        self.right_pin = ft.Column(spacing=10, controls=[])
        self.bottom_pin = ft.Row(spacing=10, controls=[])

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters

    # Pass in our character object
    def create_character(self, character):
        self.characters.append(character)   # Add our character object to our story list

        # Write our character to a file
        with open(my_file_path, "w") as f:
            f.write(character.title)  # Need to write object to json
            print("Character created: " + character.title)
            print("Character created and saved to file:", my_file_path)

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