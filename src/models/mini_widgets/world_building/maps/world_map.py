'''
A 'WorldMap' object that is displayed in the world building widget. 
These objects are stored in the world building widget, inside the diretory world_building/world_maps/wm_title.json.
These objects represent a world/planet, and can contain their own locations, geography, but also sub-maps
'''

import os
import json
import flet as ft
from models.story import Story
from models.mini_widget import MiniWidget
from models.mini_widgets.world_building.map import Map
from models.widget import Widget
from handlers.verify_data import verify_data

# Our 'world map' class that is an extended map. Acts as the parent map for all other sub maps
class WorldMap(Map):

   # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, dictionary_path: str, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,  
            father=father,    
            page=page,      
            dictionary_path=dictionary_path,     
            data=data,          
        ) 
        

        # Have the most amount of data, while maps have the least????
        
        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "world_map",             # Tag to identify what type of object this is

                # List of different categories for organizing our world maps. (Psuedo folders)
                'categories': [
                    'continents',
                    'oceans',
                    'regions',
                    'countries',
                    'cities',
                ],
                
                'content': str,                 # Content of our world map
            },
        )

        # Need to be able to draw maps for continents, countries, regions, dungeons, cities, etc.
        # Needs drawing functionality, as well as ability to just add locations, markers, notes
        # Store sub maps inside of folders - continents, oceans, etc.?
        
        self.maps = {}
        self.continents = {}
        self.oceans = {}
        self.regions = {}
        self.countries = {}
        self.cities = {}
        
        

        # Builds/reloads our timeline UI
        self.reload_world_map()


    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass

    # Called when we need to rebuild out timeline UI
    def reload_world_map(self):

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
    



        