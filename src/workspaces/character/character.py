import flet as ft

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name):
        self.name = name    
        self.widget = ft.Container
        self.widget_visible = True     # Widget active and visible = True
        
    # picture : ft.Image?
    age : int
    parents: list[str]
    backstory : str
    abilities : list[str]
    occupation: str
    # origin = Origin
    notes : str
    shown : bool

    # unique data types, (not str)
    color : str
    icon : str

    show_character : bool
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
    dead : bool
}
'''
# Saving characters locally
# app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
# my_file_path = os.path.join(app_data_path, "characters.json")
# with open(my_file_path, "w") as f:
    # f.write("My characters will go here")

# Creates our widget for each character object
def create_character_widget(name):

    # list of flet controls, nested within a column
    list = [
        ft.Text("title 1")
    ]

    # return finished widget
    #return create_new_widget(name, list)

