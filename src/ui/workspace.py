'''
UI styling for the main workspace area of appliction that holds our widgets (tabs)
Returns our container with our formatting areas inside the workspace area.
The stories 'mast_stack' holds our 'master_row', which contains our five pins: top, left, main, right, and bottom.
Overtop that, we append our drag targets when we start dragging a widget (tab). Thats why its a stack
'''

import flet as ft
from models.app import app
from models.story import Story

# Function to return our container for our widgets
def create_workspace(story: Story=None) -> ft.Container:   

    def create_new_story_button_clicked(e):
        ''' Placeholder for new story click event '''
        print("New Story Clicked")

        def submit_new_story(title: str):
            ''' Creates a new story with the given title '''

            # Needs to check if title is unique
            app.create_new_story(title, e.page)

    if story is not None:
        # Container for 1 or more widgets open on the workspace area right side of screen
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
            content=story.master_stack,   
        )
    
    else:
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
            content=ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                text="No Active Story\nClick to Create New Story",
                on_click=create_new_story_button_clicked,
                width=200,
                height=100,
                shape=ft.RoundedRectangleBorder(radius=10),  
            ),
        )
