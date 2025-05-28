import flet as ft
import os

# list of all characters in the project
characters = []

# Class for each character. Requires passing in a name
class Character:
    def __init__(self, name):
        self.name : str = name
        
    # picture : ft.Image?
    age : int
    parents: list[str]
    backstory : str
    abilities : list[str]
    occupation: str
    # origin = origin
    notes : str

    '''# Used for filtering 
    main_character : bool
    side_character : bool
    background_character : bool
    good : bool
    evil : bool
    neutral : bool

    # Add ons that won't show by default
    race: str
    species : str
    parents = []


origin = {
    "Birthplace": "",
    "Birth date": "",
    "Hometown": "",
    "Education": "",
}
'''

# Saving characters locally
app_data_path = os.getenv("FLET_APP_STORAGE_TEMP")  # write to non-temp storage later /storage/data/characters
my_file_path = os.path.join(app_data_path, "test_file.txt")
with open(my_file_path, "w") as f:
    f.write("My characters will go here")

def characters_view(page):
    return ft.View(
        "/",
        [ft.Text("This is Page One"), ft.ElevatedButton("Go to Page Two", on_click=lambda _: page.go("/two"))]
    )
