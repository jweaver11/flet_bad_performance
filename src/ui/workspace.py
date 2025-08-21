'''
UI styling for the main workspace area of appliction that holds our widgets (tabs)
Returns our container with our formatting areas inside the workspace area.
The stories 'mast_stack' holds our 'master_row', which contains our five pins: top, left, main, right, and bottom.
Overtop that, we append our drag targets when we start dragging a widget (tab). Thats why its a stack
'''

import flet as ft
from models.user import user

# Function to return our container for our widgets
def create_workspace() -> ft.Container:   

    # Container for 1 or more widgets open on the workspace area right side of screen
    return ft.Container(
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
        content=user.active_story.master_stack,   
    )
