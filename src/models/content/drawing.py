import flet as ft
from models.widget import Widget
from models.story import Story


# Our widget class that displays our world building and lore information
class Drawing(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "chapter",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
        )


    def save_dict(self):
        pass

    def load_from_dict(self, directory_path: str):
        pass

    def reload_widget(self):
        pass



# Display our drawings in the rail
# drawings = {}
    # - editable = bool
    # - filters (whitewash, greyscale, invert, etc.)