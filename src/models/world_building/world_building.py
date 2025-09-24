import flet as ft
from models.widget import Widget
from models.story import Story
import os
import json


# Our widget class that displays our world building and lore information
class World_Building(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "world",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )
        self.visible = False

        self.locations = {}
        self.lore = {}
        self.power_systems = {}
        self.social_systems = {}
        self.geography = {}


        self.load_from_dict(directory_path)  # Loads our object from a dictionary (from json file)

        self.reload_widget()


    def save_dict(self):
        # Print(f"Saving plotline data to {self.data['file_path']}")
        file_path = os.path.join(self.directory_path, "world.json")

        try:
            # Create the directory if it doesn't exist
            os.makedirs(self.directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving world to {file_path}: {e}")
        pass

    def load_from_dict(self, directory_path: str):
        self.save_dict()

    def reload_widget(self):
        # Our column that will display our header filters and body of our widget
        body = ft.Text(f"hello from: {self.title}")


        # our tab.content is the column we build above.
        self.tab.content=body  # We add this in combo with our 'tabs' later

        # Sets our actual 'tabs' portion of our widget, since 'tab' needs to nest inside of 'tabs' in order to work
        content = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Content of our widget (ft.Container) is our created tabs content
        self.content = content




# Description of world
# Power systems (if any)
# Social systems
# Geography
# History
# ...