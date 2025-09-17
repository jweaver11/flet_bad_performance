""" WIP """

import flet as ft
from models.story import Story


# Class is created in main on program startup
class Timeline_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__()
            
        self.p = page

        self.reload_rail(story)

    # Reload the rail whenever we need
    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''

        # Build the content of our rail
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
                ),
                ft.TextButton(
                    "create plotline",
                    on_click=lambda e: self.create_plotline("plotline 2", story)
                ),
                # Add more controls here as needed
            ]
        )

        self.p.update()

    # Called when user creates a new plotline
    def create_plotline(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''

        # Calls story function to create a new plotline
        story.timeline.create_plotline(title)
        self.reload_rail(story)
        
        print(len(story.timeline.plotlines))
