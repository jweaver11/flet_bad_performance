'''
Parent rail class used by our six workspaces. Gives uniformity to our rails
'''

import flet as ft
from models.story import Story


class Rail(ft.Container):

    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__(
            padding=None,
        )
            
        # Page and story reference
        self.p = page
        self.story = story

        # Calling initial rail to reload
        self.reload_rail()

    # Called when changes occure that require rail to be reloaded. Should be overwritten by children
    def reload_rail(self) -> ft.Control:
        ''' Sets our rail (extended ft.Container) content and applies the page update '''

        # Set your content for the rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("Base Rail - No specific content"),
                # Add more controls here as needed
            ]
        )

        # Apply the update to UI
        self.p.update()

        # Return yourself as the control
        return self