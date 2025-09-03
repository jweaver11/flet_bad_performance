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

    # Reload the rail whenever we need
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
                    ),
                    ft.TextButton(
                        "create plotline",
                        on_click=lambda e: self.create_plotline("plotline 1", story)
                    ),
                    ft.TextButton(
                        "show plotlines",
                        on_click=lambda e: self.show_plotline(story)
                    ),
                    # Add more controls here as needed
                ]
            )

            self.p.update()

        else:

            print("Warning: Story is None, cannot load plot and timeline rail.")
            self.content = ft.Text("Create a story to get started!")
            self.p.update()


    def show_plotline(self, story: Story):
        for title, plotline in story.plotlines.items():
            print(plotline.title)
            print(plotline)
            plotline.show_widget(story)
            # Add more functionality here as needed

        story.workspace.reload_workspace(self.p, story)
        self.p.update()

    def create_plotline(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''
        if story is not None:
            story.create_plotline(title)
            self.reload_rail(story)
        else:
            print("No story selected, how u hit dis button dumbo??")




# Add multiple timelines