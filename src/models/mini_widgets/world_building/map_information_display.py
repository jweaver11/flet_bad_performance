'''
The map class for all maps inside of the world_building widget
Maps are extended mini widgets, with their 'display' being the view of the map, and their mini widget being the maps info display
Maps don't save like mini widgets. They save their data inside one file, and their drawing data in another file.
Since maps could have hundreds of sub-maps, we give them each their own file to avoid corruption
'''

# BLANK NO TEMPLATE MAPS EXIST AS WELL
# ADD DUPLICATE OPTION AS WELL
# Users can choose to create their image or use some default ones, or upload their own
# When hovering over a map, display it on the rail as well so we can see where new sub maps would


import os
import json
import flet as ft
from models.widget import Widget
from models.mini_widget import MiniWidget
from handlers.verify_data import verify_data
from models.state import State
import flet.canvas as cv
from threading import Thread



class Map_Information_Display(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, world map owner, and optional data dictionary
    def __init__(
        self, 
        title: str, 
        owner: Widget, 
        father, 
        page: ft.Page, 
        dictionary_path: str, 
        category: str = None, 
        data: dict = None
    ):
        
        # Supported categories: World map, continent, region, ocean, country, city, dungeon, room, none.
        
        
        # Parent constructor
        super().__init__(
            title=title,           
            owner=owner, 
            father=father,       # In this case, father is either a parent map or the world building widget
            page=page,              
            data=data,              
            dictionary_path=dictionary_path     
        ) 

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   
            {
                'tag': "map_information_display", 
                'is_displayed': True,           # Whether the map is visible in the world building widget or not
                'maps': dict,                   # Sub maps contained within this map
                'category': category,           # Category/psuedo folder this map belongs to
                'markers': dict,                # Markers placed on the map
                'locations': dict,
                'geography': dict,              # Geography of the world
                'rooms': dict,                  
                'notes': str,

                'position': {               # Our position on our parent map
                    'x': 0,                    
                    'y': 0,                     
                },

                'sub_categories': {                     # Categories for organizing our maps on the rail
                    'category_name': {
                        'title': str,               # Title of the category
                        'is_expanded': bool,        # Whether the category is expanded or collapsed
                    },
                },
            },
        )


        # Reloads the information display of the map
        self.reload_mini_widget()


    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
    



        