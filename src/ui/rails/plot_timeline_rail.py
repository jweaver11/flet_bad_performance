""" WIP """

import flet as ft


def create_plot_and_timeline_rail(page: ft.Page) -> ft.Control:
    from models.app import app  # Needs to import here for updated reference each time
 
    return ft.Column(
        spacing=0,
        expand=True,
        controls=[
            ft.Text("Plot and Timeline Rail"),
            ft.Text("From the story: "),
            ft.Text(app.active_story.title)
            # Add more controls here as needed
        ]
    )

def reload_plot_and_timeline_rail(page: ft.Page):
    ''' Reloads the plot and timeline rail, useful when switching stories '''
    pass


# Add multiple timelines