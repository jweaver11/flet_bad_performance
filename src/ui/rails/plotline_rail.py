""" WIP """

import flet as ft
from models.story import Story


# Class is created in main on program startup
class Plotline_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story=None):
        
        # Initialize the parent Container class first
        super().__init__()
            
        self.p = page

        self.reload_rail(story)


    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''

        if story is not None:

            self.content = ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    ft.Text("Plot and Timeline Rail"),
                    ft.Text("From the story: "),
                    ft.Text(story.title),
                    ft.TextButton(
                        "create character",
                        on_click=lambda e: story.create_character("John Doe")
                        #TODO create text box for user input of char name & save
                    )
                    # Add more controls here as needed
                ]
            )

            self.p.update()

        else:

            print("Warning: Story is None, cannot load plot and timeline rail.")
            self.content = ft.Text("Create a story to get started!")
            self.p.update()




# Add multiple timelines