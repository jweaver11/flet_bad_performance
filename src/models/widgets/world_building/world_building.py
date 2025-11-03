''' 
Our widget class that displays our world building and lore information.
Our stories have one world building widget, that displays whichever map is selected
This widget stores 'WorldMaps', which stores sub 'Maps' for its continents, oceans, countries, dungeons etc.
Maps (sub maps) can store other sub maps infinitely, so a continent can store countries, which can store cities, etc, but don't need to be
Nested in any particular way. WorldMaps CANNOT store each other or be nested.
'''

import os
import flet as ft
from models.widget import Widget
from models.story import Story
from handlers.verify_data import verify_data


class World_Building(Widget):

    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  
            page = page,   
            directory_path = directory_path,  
            story = story,       
            data = data,    
        )
        
        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "world_building",            

                'sub_categories': {                     # List of different categories for organizing our world maps on the rail. (Psuedo folders)
                    'category_name': {
                        'title': str,               # Title of the category
                        'is_expanded': bool,        # Whether the category is expanded or collapsed
                    },
                    'continents': {
                        'title': str,
                        'is_expanded': bool,
                    },
                    'oceans': {
                        'title': str,
                        'is_expanded': bool,
                    },
                    'regions': {
                        'title': str,
                        'is_expanded': bool,
                    },
                    'countries': {
                        'title': str,
                        'is_expanded': bool,
                    },
                    'cities': {
                        'title': str,
                        'is_expanded': bool,
                    },
                    # TODO: Have the story type add categories here
                },           
                 

                'lores': dict,                      # Dict of any world lore, myths, legends, etc
                'history': dict,                    # History of the world
                'power_systems': dict,              # Power systems of the world
                'social_systems': dict,             # Social systems of the world
                'geography': dict,                  # Geography of the world
                'technology': dict,                 # Technology of the world
                'governments': dict,                # Governments of the world
                'content': str,
            }
        )

        # Dict of different worlds and their maps stored
        #self.maps = {}

        self.locations = {}
        self.lore = {}
        self.power_systems = {}         # Tie to any
        self.social_systems = {}        # Tie to countries, tribes, continents, etc
        self.geography = {}             # Tie to any
        self.technology = {}            # Tie to any
        self.history = {}               # Tie to any
        self.governments = {}           # Tie to countries, tribes, etc

        # Load our live objects from our data
        #self.load_maps()
        self.load_lore()
        self.load_power_systems()
        self.load_social_systems()
        self.load_geography()
        self.load_technology()
        self.load_history()

        # Drawing controls here. Not sure if need to be stored or how do that yet

        self.reload_tab()
        self.reload_widget()
    

    def load_lore(self):
        pass

    def load_power_systems(self):
        pass

    def load_social_systems(self):
        pass

    def load_geography(self):
        pass

    def load_technology(self):
        pass

    def load_history(self): 
        pass

    def load_governments(self):
        pass



    def on_hover(self, e: ft.HoverEvent):
        pass

    # Called to reload our widget UI
    def reload_widget(self):
        ''' Reloads our world building widget '''
        

        self.body_container.content = ft.Text("Hellow from World Building Widget")

        self._render_widget()




        # Users can choose to create their image or use some default ones
        # Have edit mode where all locations, places, etc. disappear and user can draw and edit underlying map
        # Add drag target to accept maps from rail into this rail

        # TODO: Make it so the maps are rendered in the body of the widget
        # Should be able to see multiple maps at once, and their mini widget info displays as 
        # MAPS ARE WIDGETS, THAT STORE THEIR OTHER MAPS HOWEVER I SEE FIT (CONTINENTS, COUNTRIES, CITIES, DUNGEONS, ROOMS, ETC, OR JUST MAPS {})
        # THEY HAVE A SAVE DICT METHOD AND UPDATE DICT METHOD THAT WOULD WORK LIKE THE MW SAVE DICT TO UPDATE PARENT MAPS
        # THEY ALSO HAVE THEIR OWN FILES TO STORE THEIR IMAGES


        # TODO: Show timeline that can drag and alter the map landscape based on changes
            # EXP. City gets destroyed at year 50, that plotpoint would disappear
        # Option to expand map to add more continents, regions, etc


        # MAPS USE TREE VIEW FORMAT, ANY MAP CAN FIT IN ANY OTHER MAP, NO RESTRICTIONS. THEY ARE WIDGETS WITH 2 FILES,
        # ONE FOR IMAGE, ONE FOR DATA. THEY CAN STORE OTHER MAPS IN THEIR DATA
        # Change cursor to click icon, highlight map in widget




    # Called at end of reload_widget
    def _render_widget(self):
        ''' Renders our world building widget UI '''

        # Set the mini widgets visibility to false so we can check later if we want to add it to the page
        self.mini_widgets_container.visible = False
        self.content_row.controls.clear()   # Clear our content row so we can rebuild it


        # Add the body container to our content row
        self.content_row.controls.append(self.body_container)


        # BUILDING MINI WIDGETS - Column that holds our mini note controls on the side 1/3 of the widget
        self.mini_widgets_column.controls = self.mini_widgets   
        
        # Add our column that we build to our mini widgets container
        self.mini_widgets_container.content = self.mini_widgets_column

        # Check if we are showing any mini widgets. If we are, add the container to our content row
        for mini_widget in self.mini_widgets_column.controls:
            # TODO: Add check for right or left side mini widgets. Either insert at controls[0] or append
            if mini_widget.visible:
                self.mini_widgets_container.visible = True
                self.content_row.controls.append(self.mini_widgets_container)
                break
            
        
        # BUILD OUR TAB CONTENT - Our tab content holds the row of our body and mini widgets containers
        self.tab.content = self.content_row  # We add this in combo with our 'tabs' later
        
        # Add our tab to our tabs control so it will render. Set our widgets content to our tabs control and update the page
        self.tabs.tabs = [self.tab]
        self.content = self.tabs
        self.p.update()