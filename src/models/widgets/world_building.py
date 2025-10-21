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
            p = page,   
            directory_path = directory_path,  
            story = story,       
            data = data,    
        )
        
        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "world_building",            # Tag to identify what type of object this is

                # List of different categories for organizing our world maps on the rail. (Psuedo folders)
                'categories': [
                    'continents',
                    'oceans',
                    'regions',
                    'countries',
                    'cities',
                ],            # Only check world maps for categories
                # TODO: Have the story type add categories here

                'world_maps': dict,                 # Dict of different worlds and their maps stored
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
        self.world_maps = {}
        self.locations = {}
        self.lore = {}
        self.power_systems = {}     # Tie to any
        self.social_systems = {}    # Tie to countries, tribes, continents, etc
        self.geography = {} # Tie to any
        self.technology = {}    # Tie to any
        self.history = {}   # Tie to any
        self.governments = {}   # Tie to countries, tribes, etc

        # Load our live objects from our data
        self.load_world_maps()
        self.load_lore()
        self.load_power_systems()
        self.load_social_systems()
        self.load_geography()
        self.load_technology()
        self.load_history()

        # TODO: Show timeline that can drag and alter the map landscape based on changes
            # EXP. City gets destroyed at year 50, that plotpoint would disappear
        # Option to expand map to add more continents, regions, etc
        # Option for mini widget/widgets to display even when no map is shown

        self.reload_widget()
    

    # Called in constructor
    def load_world_maps(self):
        ''' Loads our world maps from our dict into our live object '''
        

        for map_title, map_data in self.data['world_maps'].items():

            # Create a new Map object for each map in our data
            from models.mini_widgets.world_building.map import Map

            self.world_maps[map_title] = Map(
                title = map_title,
                owner = self,
                father=self,
                page = self.p,
                dictionary_path="world_maps",
                data = map_data,
            )


        # If we have no world maps, create a default one to get started
        if len(self.world_maps) == 0:
            #print("No world maps found, creating default world map")
            self.create_world_map(title="World Map")

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


    # Called when creating a new world map
    def create_world_map(self, title: str):
        ''' Requires a title. Creates a new world map in our live object and data'''
        from models.mini_widgets.world_building.maps.world_map import WorldMap

        # Filters to hide different kinds of maps like countries, continents, oceans, cities, locations, etc

        # Creates our new map object
        new_map = WorldMap(
            title=title,
            owner=self,
            father=self,
            page=self.p,
            dictionary_path=os.path.join(self.directory_path, 'world_maps'),
            data=None,
        )


        # Creates the new map object and saves its data
        self.world_maps[title] = new_map
        self.data['world_maps'][title] = self.world_maps[title].data
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

        # Worlds are maps in this case

        # World building widget will use an image as a base, and overlay its content on top of that.
        # Users can choose to create their image or use some default ones
        # If no image is provided, start with a default circle 
        # Have edit mode where all locations, places, etc. disappear and user can draw and edit underlying map

        # Our column that will display our header filters and body of our widget
        self.body_container.content = ft.Text(f"hello from: {self.title}")

        self._render_widget()