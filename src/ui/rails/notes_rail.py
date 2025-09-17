""" WIP """

import flet as ft
from models.story import Story


# Class for our Drawing Board rail
class Notes_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__()
            
        # Page reference
        self.p = page

        # Reload the rail on start
        self.reload_rail(story)


    # Called when changes occur that require rail to be reloaded, but the object does not need to be recreated. (More efficient)
    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the Notes rail '''

        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("Notes Rail"),
                ft.Text("From the story: "),
                ft.Text(story.title),
                ft.TextButton(
                    "Create Note",
                    on_click=lambda e: story.create_note("note_title")
                ),
                ft.TextButton(
                    "View Notes",
                    icon=ft.Icons.VIEW_LIST,
                    ),
                ft.Text("This is where you can manage your notes."),
                # Add more controls here as needed
            ]
        )

        # Apply the update
        self.p.update()
