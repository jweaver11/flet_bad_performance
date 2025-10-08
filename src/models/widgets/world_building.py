''' 
Our widget class that displays our world building and lore information.
Our stories have one world building widget, that displays whichever map is selected
This widget stores 'WorldMaps', which stores sub 'Maps' for its continents, oceans, countries, dungeons etc.
Maps (sub maps) can store other sub maps infinitely, so a continent can store countries, which can store cities, etc, but don't need to be
Nested in any particular way. WorldMaps CANNOT store each other or be nested.
'''

import flet as ft
from models.widget import Widget
from models.story import Story
from handlers.verify_data import verify_data


class World_Building(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # Set our passed in data to our objects data
        )
        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_world_building_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            verify_data(
                self,   # Pass in our own data so the function can see the actual data we loaded
                {
                    'tag': str,
                    'world_maps': dict,
                    'content': str,
                    'locations': dict,
                    'lore': dict,
                    'power_systems': dict,
                    'social_systems': dict,
                    'geography': dict,
                    'history': dict,
                    'content': str,
                },
                tag="world_building"
            )

        # Dict of different worlds and their maps stored
        self.world_maps = {}
        self.lore = {}
        self.power_systems = {}
        self.social_systems = {}
        self.geography = {}


        # TODO: Show timeline that can drag and alter the map landscape based on changes
            # EXP. City gets destroyed at year 50, that plotpoint would disappear
        # Option to expand map to add more continents, regions, etc
        # Option for mini widget/widgets to display even when no map is shown

        self.load_maps()

        self.reload_widget()
        
    # Called when new story is created, and no data for our world exists
    def create_default_world_building_data(self) -> dict:
        ''' Gives our world building widget default data it will need if none exists '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # Default data for our world building widget
        default_world_building_data = {
            'tag': "world_building",  
            'world_maps': {},  # Dict of different worlds and their maps stored
            'locations': {},    # Dict of any locations stored in the world but not in a sub map
            'lore': {},     # Dict of any world lore, myths, legends, etc
            'power_systems': {},    # Power systems of the world
            'social_systems': {},   # Social systems of the world
            'geography': {},
            'technology': {},
            'history': {},
            'content': "",
        }

        # Update existing data with any new default fields we added
        self.data.update(default_world_building_data)
        self.save_dict()
        return self.data

    
    def load_maps(self):
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

        self.render_widget()