from handlers.create_widget_control import create_widget_control
import flet as ft
from models.story import story
from models.widget import Widget 

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name, page):
        self.name = name    # Name of our character
        self.tag = "character"
        self.visible = True     # Widget active and visible = True
        story.widgets.append(create_character_widget(self.name, page, self.tag))  # Add our widget to the story's widgets dict  # Add our widget to the bottom pin list
        
    # picture : ft.Image?
    age : int
    parents: list[str]
    backstory : str
    abilities : list[str]
    occupation : str
    # origin = Origin
    notes : str
    shown : bool

    # unique data types, (not str)
    color : str
    icon : str

    tags : list[str]



    '''
    # Add ons that won't show by default
    race: str
    species : str
    parents = []


class Origin:
    "Birthplace": str,
    "Birth date": str,
    "Hometown": str,
    "Education": str,


tags = {
    main_character : bool
    side_character : bool
    background_character : bool
    good : bool
    evil : bool
    neutral : bool
    man : bool
    woman : bool
    alive : bool
}
'''
# Saving characters locally
# app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
# my_file_path = os.path.join(app_data_path, "characters.json")
# with open(my_file_path, "w") as f:
    # f.write("My characters will go here")


# Creates our widget for each character object
def create_character_widget(name, page, tag):

    # Format our body as list of flet controls
    # list of flet controls, nested within a column
    body = [
        ft.Text("title 1")
    ]

    # Returns our ft container for the widget control
    control = create_widget_control(name, body, page)
    story.bottom_pin_widgets.append(control)  # Add our widget to the bottom pin list by default for characters

    # Create our widget obj --------------- widget ----- name - tag
    widget = Widget(control, name, tag)

    return widget