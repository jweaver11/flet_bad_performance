'''
Our timeline object that stores plot points, arcs, and time skips.
These objects is displayed in the plotline widget, and store our mini widgets plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from models.widget import Widget
from models.mini_widgets.plotline.arc import Arc
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the plotline widget, so need for this to be a flet control
class Timeline(Arc):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, dictionary_path: str, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,      
            father=father,
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "timeline",        
            },
        ) 
        

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
    



        