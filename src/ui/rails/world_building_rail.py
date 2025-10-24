""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail


class World_Building_Rail(Rail):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Rail class first
        super().__init__(
            page=page,
            story=story
        )

        # Reload the rail on start
        self.reload_rail()

    def show_world(self):
        ''' Shows the world building widget '''

        if self.story.world_building is not None:
            self.story.world_building.toggle_visibility()

    # Called when changes occur that require rail to be reloaded, but the object does not need to be recreated. (More efficient)
    def reload_rail(self) -> ft.Control:
        ''' Reloads the world building rail '''

        # Button to 'Create New World'
        # TODO: Option to create new world map depending on if multiplanetory or not
        # Reads the maps categories for each level, and adds them to a list of categories. Then displays them in the rail
        # This is how we get semi tree view for maps and pass categories in.

        column = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Text("World buidling Rail"),
                ft.Text("From the story: "),
                ft.Text(self.story.title),
                ft.TextButton(
                    "Show world building widget",
                    on_click=lambda e: self.show_world() 
                ),


                # Add more controls here as needed
            ]
        )

        for map in self.story.world_building.maps.values():
            column.controls.append(
                ft.Text(map.title)
            )

        column.controls.append(
            ft.TextField(
                label="Create new map",
                on_submit=lambda e: self.story.world_building.create_map(title=e.control.value)
            )
        )

        # Build the content of our rail
        self.content = column

        # Apply the update
        self.p.update()
    
        
