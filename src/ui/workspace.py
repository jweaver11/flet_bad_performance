'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.render_widgets import master_stack


# Function to return our container for our widgets
def create_workspace(page: ft.Page, story):    
    
    page.update()

    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        padding=ft.padding.all(10),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        content=master_stack
    )
    

    return workspace_container
