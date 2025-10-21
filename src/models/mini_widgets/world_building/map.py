'''
Parent map class that contains all other sub-maps, such as locations, world maps, continents, countries, regions, cities, dungeons, etc.
Basically, anything that COULD be fleshed out visually.
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

    # Constructor. Requires title, owner widget, page reference, world map owner, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, dictionary_path: str, type: str=None, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,           
            owner=owner, 
            father=father,       
            page=page,              
            data=data,              
            dictionary_path=dictionary_path     
        ) 

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   
            {
                'tag': "map", 
                'type': type,                  # Type of map - continent, country, region, city, dungeon, etc
                'maps': dict,   # Needed????
                'category': str,                 # Category/psuedo folder this map belongs to
                'markers': dict,
                'locations': dict,
                'geography': dict,                  # Geography of the world
                'rooms': dict,
                'notes': str,
            },
        )

        
        self.sub_maps = {}
        self.details = {}

        # Load our sub maps
        self.load_sub_maps()
        
        # Load the rest of our map details and data thats not sub maps
        self.load_details()

        # The control thats displayed on the UI
        self.ui_map: ft.Control = None
        

        # Builds/reloads our timeline UI
        self.reload_map()

    # Called in constructor
    def load_sub_maps(self):
        ''' Loads all sub maps stored in our data into our sub_maps dict'''
        # Change cursor to click one, highlight map in widdget
        pass

    def load_details(self):
        ''' Loads the rest of our map details that are not sub maps into our details dict '''
        #self.load_locations()
        #self.load_lores()
        #self.load_history()
        #self.load_power_systems()
        #self.load_technology()
        #self.load_social_systems()
        #self.load_governments()
        pass
 
    

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_map(self):


        # Depending on the type of map, we render the Map differently
        # Different right click hover options to add sub maps.
        # I.E. Continents can add countries, regions, oceans, etc.. But countries cant add continents, etc.
        # Add option to have the mini widget show on larger portion of screen, like an expand button at bottom left or right

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
    



        