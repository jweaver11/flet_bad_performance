'''
A 'Map' object that is displayed in the world building widget.
These objects are stored in 'WorldMap' objects and files, or inside of other maps
They can represent any scale of map smaller than a world, from continents, to regions, countries, cities, dungeons, buildings, etc.
Their data is stored in the parent most 'WorldMap' object file that contains them
'''

# TYPES OF MAPS, COUNTRIES CONTINENTS ETC. THAT CAN ADD THEIR OWN (SUB) MAPS. EXP. CONTINENT CAN ADD COUNTRIES, REGIONS, ETC
# BLANK NO TEMPLATE MAPS EXIST AS WELL

import os
import json
import flet as ft
from models.widget import Widget
from models.mini_widget import MiniWidget
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Map(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
            dictionary_path=""  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
        ) 

        
        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "map", 
            },
        )

        
        self.maps = {}

        # Load the rest of our data from the file
        

        # Builds/reloads our timeline UI
        self.reload_map()
 
    
    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_map(self):

        # We only show branches, arcc, plotpoints, and timeskips using their UI elements, not their mini widget

        # Content of our Timeline (Gesture detector)
        self.content = ft.Container(
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
    



        