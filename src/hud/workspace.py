'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.layout_widgets import widget_row



stack = ft.Stack(
    expand=True, 
    controls=[widget_row]
)




# Function to return our container for our widgets
def create_workspace(page: ft.Page, story):     

    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        #margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        #bgcolor=ft.Colors.GREY_800,
        content=stack
    )
    
    page.update()
    

    return workspace_container