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
                ft.Text("Timeline Rail"),
                ft.Text("From the story: "),
                ft.Text(story.title),
                ft.Container(height=10),

                ft.Row([
                    ft.Text("Start date: "),
                    ft.TextField(value=str(story.timeline.data['story_start_date'])),
                ]),
                ft.Container(height=10),

                ft.Row([
                    ft.Text("End date: "),
                    ft.TextField(value=str(story.timeline.data['story_end_date'])),
                ]),
                ft.Container(height=20),

                ft.Column([
                    ft.Text("Plotlines:"),
                    ft.ListView(
                        expand=True,
                        spacing=5,
                        padding=ft.padding.all(10),
                        auto_scroll=True,
                        controls=[
                            ft.Text(plotline.title) for key, plotline in story.timeline.plotlines.items()
                        ]
                    ),
                ]),
                ft.Container(height=20),

                ft.TextButton(
                    "create plotline",
                    on_click=lambda e: self.create_plotline("plotline 2", story)
                ),

                ft.TextField(label="Create New Plotline", on_submit=lambda e: self.create_plotline(e.control.value, story)),
                # Add more controls here as needed
            ]
        )

        self.p.update()

    # Called when user creates a new plotline
    def create_plotline(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''

        # Check if name is unique
        name_is_unique = True

        for key, plotline in story.timeline.plotlines.items():
            if plotline.title == title:
                name_is_unique = False
                print("Plotline name already exists!")
                break

        if name_is_unique:

            # Calls story function to create a new plotline
            story.timeline.create_plotline(title)
            self.reload_rail(story)
        
        print(len(story.timeline.plotlines))
