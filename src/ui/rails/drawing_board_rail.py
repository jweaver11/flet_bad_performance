""" WIP """

import flet as ft
from models.story import Story


# Class for our Drawing Board rail
class Drawing_Board_Rail(ft.Container):
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
        ''' Reloads the drawing board rail '''

        # New
        # Open
        # Upload
        # TODO: RAIL Has brushes, tools, colors, etc.
        # Structure of content_directory, showing images in the rail
        # - click one to open it in a drawing board


        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("Drawing Board Rail"),
                ft.Text("From the story: "),
                ft.Text(story.title),
                ft.TextButton(
                    "Create Drawing",
                    on_click=lambda e: story.create_drawing("Drawing_Title")
                ),
                # Add more controls here as needed
            ]
        )

        


        # Apply the update
        self.p.update()