''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from models.character import Character
from models.story import Story

class Characters_Rail(ft.Container):
    def __init__(self, page: ft.Page, story: Story):

        super().__init__()

        self.p = page

        self.reload_rail(story)

    def submit_character(self, e):
        ''' Handles the logic for creating a new character '''

        name = e.control.value
        story = self.p.views[0]  # Our current story object
        
        story.create_character(name)

        e.control.value = None  # Clear the text field
        self.reload_rail(story)


    def rename_character(self, character: Character):
        pass

    def delete_character(self, character: Character):
        pass

    # Called when hovered over a character on the rail
    def show_character_options(e):
        ''' Shows our button that has the rename and delete options '''

        e.control.content.controls[2].opacity = 1
        e.control.content.controls[2].update()
        

    # Called when mouse leaves a character on the rail
    def hide_character_options(e):
        ''' Hides our button that shows rename and delete options '''

        e.control.content.controls[2].opacity = 0
        e.control.content.controls[2].update()


    # Called when the 'color' button next to character on the rail is clicked
    def change_character_color(self, character: Character, color, page: ft.Page):
        ''' Changes the characters tab color (not finished) '''

        self.reload_rail(page)
        character.reload_widget()
        


    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self, story: Story):

        column = ft.Column([])

        for character in story.characters.values():
            char_button = ft.TextButton(
                text=character.title,
                on_click=lambda e, char=character: char.show_widget(story), # Needs this reference, idk y
            )
            column.controls.append(char_button)

        column.controls.append(
            ft.TextField(
                label="Create Character",
                hint_text="Enter character name",
                on_submit=self.submit_character,  # When enter is pressed
            )
        )

        self.content = column

        self.p.update()



