""" WIP """

import flet as ft
from models.story import Story


def create_plot_and_timeline_rail(page: ft.Page, story: Story) -> ft.Control:
    from models.app import app  # Needs to import here for updated reference each time
 
    return ft.Column(
        spacing=0,
        expand=True,
        controls=[
            ft.Text("Plot and Timeline Rail"),
            ft.Text("From the story: "),
            ft.Text(story.title),
            ft.TextButton(
                "create character",
                on_click=story.create_character("John Doe")
            )
            # Add more controls here as needed
        ]
    )

def reload_plot_and_timeline_rail(page: ft.Page):
    ''' Reloads the plot and timeline rail, useful when switching stories '''
    pass


# Add multiple timelines