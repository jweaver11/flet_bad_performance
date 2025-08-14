'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from models.user import user

# Function to return our container for our widgets
def create_workspace(page: ft.Page):   

    story = user.active_story  # Get our story object from the user 
    
    page.update()

    
    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
        #bgcolor=user.settings.workspace_bgcolor,
        #padding=ft.padding.all(4),
        #border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        content=story.master_stack,
        
    )
    

    return workspace_container
