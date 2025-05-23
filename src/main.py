# The main 'story' page. The default page that all others work through
import flet as ft
from characters import characters_view
from characters import Character
from nav_rail import rail
from workspace import workspace
from menu_bar import menubar

# Class for each seperate story/project
class Story:
    # Page navigations
    characters = [Character]
    Notes = []

    # Constructor that sets the story name
    def __init__(self, name):
        self.name = name

    # Create our character 
    def CreateCharacter(self, character_name):
        # Create the character name
        self.name = character_name
        char3 = Character(self.name)
        self.characters[0] = char3
        return print(self.characters[0].name)
                

# Creating new character object within story object
char2 = Character("character name 2")
story = Story("story name")
story.characters[0] = char2

story.CreateCharacter("my brand new characters name")


# MAIN FUNCTION TO RENDER PAGE ---------------------------------------------------------
def main(page: ft.Page):

    # page.add(ft.Row([menubar, appbar]))
    page.add(ft.Row([menubar]))

    # Adds our navbar and the workspace for the rest of the space
    page.add(
        ft.Row
        (
            [
                rail,
                ft.VerticalDivider(width=10),
                workspace,
            ],
            expand=True
        )
    )


ft.app(main)