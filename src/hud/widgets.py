'''
Our 'widgets' page that returns the container for
all the active widgets.
Our widgets are draggable, and fit pre-set sized spacers
for more customization
'''

import flet as ft
from workspaces.story import story

def update_page(page):
    print("page updated")
    page.update()




# Function to return our container for our widgets
def create_widgets(page: ft.Page):      

    # Will add our active widgets
    widgets_row = ft.Row(
        spacing=4,
        expand=True,
        controls=story.widgets    # Make the story.widgets somehow
    )

    # Container for 1 or more pagelets open on main right side of screen (work area)
    active_widgets_container = ft.Container(
        expand=True,
        margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_800,
        content=widgets_row
    )

    '''
    tr = ft.Container(
        height=100,
        expand=True, 
        bgcolor=ft.Colors.RED,
        content=ft.DragTarget(
            group="top_row",
            content=ft.Container(height=20)
        )
    )

    stack = ft.Stack(
        clip_behavior=True,
        controls=
        [
            #d1, 
            #d2,
            #tr,
        ],
    )
    '''

    return active_widgets_container