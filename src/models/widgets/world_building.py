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
from models.mini_widgets.world_building.map import Map
from models.story import Story
from handlers.verify_data import verify_data


class World_Building(Widget):

    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  
            p = page,   
            directory_path = directory_path,  
            story = story,       
            data = data,    
        )
        
        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "world_building",            
                'displayed_maps': list,                  # List of the maps displayed in the widget

                # List of different categories for organizing our world maps on the rail. (Psuedo folders)
                'categories': [
                    'continents',
                    'oceans',
                    'regions',
                    'countries',
                    'cities',
                ],           
                 
                # TODO: Have the story type add categories here

                'lores': dict,                      # Dict of any world lore, myths, legends, etc
                'history': dict,                    # History of the world
                'power_systems': dict,              # Power systems of the world
                'social_systems': dict,             # Social systems of the world
                'geography': dict,                  # Geography of the world
                'technology': dict,                 # Technology of the world
                'governments': dict,                # Governments of the world
                'content': str,
                'maps': dict,                       # All maps contained within this world building widget
            }
        )

        # List of our maps (map.map) visuals displayed in the widget
        self.displayed_maps: list = []

        # Dict of different worlds and their maps stored
        self.maps = {}
        self.locations = {}
        self.lore = {}
        self.power_systems = {}     # Tie to any
        self.social_systems = {}    # Tie to countries, tribes, continents, etc
        self.geography = {} # Tie to any
        self.technology = {}    # Tie to any
        self.history = {}   # Tie to any
        self.governments = {}   # Tie to countries, tribes, etc

        # Load our live objects from our data
        self.load_maps()
        self.load_lore()
        self.load_power_systems()
        self.load_social_systems()
        self.load_geography()
        self.load_technology()
        self.load_history()

        # Drawing controls here. Not sure if need to be stored or how do that yet

        self.reload_widget()
    

    # Called in constructor
    def load_maps(self):
        ''' Loads our world maps from our dict into our live object '''
        
        try: 
            # Run through our maps saved in the maps dict
            for map_title, map_data in self.data['maps'].items():

                # Create a new map object
                self.maps[map_title] = Map(
                    title=map_title,
                    owner=self,
                    father=self,
                    page=self.p,
                    dictionary_path="maps",
                    data=map_data,
                )

                # Add the map to our displayed maps list if it visible there
                if self.maps[map_title].data.get('map_is_visible', True):
                    self.displayed_maps.append(self.maps[map_title].display)

                # Add it to our mini widgets list
                self.mini_widgets.append(self.maps[map_title])

            # If we have no maps, create a default one to get started
            if len(self.maps) == 0:
                #print("No world maps found, creating default world map")
                self.create_map(title="World Map")

        # Catch errors
        except Exception as e:
            print(f"Error loading maps for the world building widget: {e}")

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


    # Called when creating a new map
    def create_map(self, title: str, category: str=None):
        ''' Requires a title. Creates a new world map in our live object and data'''

        # Creates our new map object
        new_map = Map(
            title=title,
            owner=self,
            father=self,
            page=self.p,
            dictionary_path="maps",
            data=None,
        )

        # Creates the new map object and saves its data
        self.maps[title] = new_map
        self.displayed_maps.append(self.maps[title].display)
        self.mini_widgets.append(self.maps[title])

        # Save our new maps data
        self.data['maps'][title] = self.maps[title].data
        self.save_dict()

        # Reload our widget and rail to show the new map
        self.reload_widget()

        # Catches error if creating default world map on program startup, where UI is not created yet
        if self.story.active_rail is not None:
            self.story.active_rail.content.reload_rail()


    def on_hover(self, e: ft.HoverEvent):
        pass

    def reload_widget(self):
        ''' Reloads our world building widget '''

        row = ft.Row()
        row.controls.extend(self.displayed_maps)
        self.body_container.content = row

        self._render_widget()




        # Users can choose to create their image or use some default ones
        # Have edit mode where all locations, places, etc. disappear and user can draw and edit underlying map

        # TODO: Make it so the maps are rendered in the body of the widget
        # Should be able to see multiple maps at once, and their mini widget info displays as 
        # MAPS ARE WIDGETS, THAT STORE THEIR OTHER MAPS HOWEVER I SEE FIT (CONTINENTS, COUNTRIES, CITIES, DUNGEONS, ROOMS, ETC, OR JUST MAPS {})
        # THEY HAVE A SAVE DICT METHOD AND UPDATE DICT METHOD THAT WOULD WORK LIKE THE MW SAVE DICT TO UPDATE PARENT MAPS
        # THEY ALSO HAVE THEIR OWN FILES TO STORE THEIR IMAGES


        # TODO: Show timeline that can drag and alter the map landscape based on changes
            # EXP. City gets destroyed at year 50, that plotpoint would disappear
        # Option to expand map to add more continents, regions, etc
        # Option for mini widget/widgets to display even when no map is shown


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