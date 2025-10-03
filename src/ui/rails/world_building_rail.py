""" WIP """

import flet as ft
from models.story import Story


class World_Building_Rail(ft.Container):
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
        ''' Reloads the world building rail '''

        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("World buidling Rail"),
                ft.Text("From the story: "),
                ft.Text(story.title),
                ft.TextButton(
                    "Show world",
                    on_click=lambda e: self.show_world(story)
                    
                ),
                # Add more controls here as needed
            ]
        )

        # Apply the update
        self.p.update()

    def show_world(self, story: Story):
        ''' Shows the world building widget '''

        if story.world_building is not None:
            story.world_building.toggle_visibility(story)
    
        
