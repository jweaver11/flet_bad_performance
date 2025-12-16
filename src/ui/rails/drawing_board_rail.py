""" WIP """

import flet as ft
from models.views.story import Story
from ui.rails.rail import Rail


# Class for our Drawing Board rail
class Drawing_Board_Rail(Rail):

    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__(
            page=page,
            story=story,
            directory_path=story.data['content_directory_path']
        )
        
        # Reload the rail on start
        self.reload_rail()


    # Called when changes occur that require rail to be reloaded, but the object does not need to be recreated. (More efficient)
    def reload_rail(self) -> ft.Control:
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
                ft.Text("Drawing Board Rail is Under Construction"),
                # Add more controls here as needed
            ]
        )

        # Apply the update
        self.p.update()