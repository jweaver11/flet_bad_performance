# The main 'story' page. The default page that all others work through
import flet as ft
from characters import characters_view
from characters import Character

# Class for the hud?
class Hud:
    class Top_Row:
        def __init__(self):
            self.items = []


    class Left_Column:
        def __init__(self):
            self.items = []

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
    counter = ft.Text("0", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
