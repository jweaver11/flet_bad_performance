'''
Our timeline object that stores plot points, branches, arcs, and time skips.
These objects is displayed in the plotline widget, and store our mini widgets branches, plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from models.widget import Widget
from models.mini_widgets.plotline.branch import Branch
from handlers.verify_data import verify_data

# An extended Branch object that acts as the 'parent' branch for all other branches to stem from
class Timeline(Branch):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            timeline=self,   # Pass in our own timeline reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "timeline",
                'color': "primary",
            },
        ) 


        # Create our live object dictionaries
        self.connections: dict = {} # Connect points, arcs, branch, etc.???

        # The control that shows up in the plotline widget OUTSIDE our mini widget
        self.timeline_control: ft.GestureDetector = ft.GestureDetector() 

        # Builds/reloads our timeline UI
        self.reload_mini_widget()


    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_mini_widget(self):

        # We only show branches, arc, plotpoints, and timeskips using their UI elements, not their mini widget

        
        self.timeline_control = ft.Container(
            margin=ft.margin.only(left=20, right=20),
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    #ft.Text(plotline.title, color=ft.Colors.WHITE, size=16),
                    ft.Divider(color=ft.Colors.with_opacity(0.4, ft.Colors.BLUE), thickness=2),
                ],
            )
        )
    



        