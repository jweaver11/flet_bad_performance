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
            self.verify_world_building_data()

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
    
    # Called to verify loaded data
    def verify_world_building_data(self):
        ''' Verify loaded any missing data fields in existing chapters '''

        # Required data for all widgets and their types
        required_data_types = {
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
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'tag': "chapter",
            'world_maps': {},
            'content': "",
            'locations': {},
            'lore': {},
            'power_systems': {},
            'social_systems': {},
            'geography': {},
            'history': {},
            'content': "",
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        self.data['tag'] = "world_building"   # Make sure our tag is always correct

        # Save our updated data
        self.save_dict()
        return
    
    def load_maps(self):
        pass

    def reload_widget(self):
        ''' Reloads our world building widget '''

        # Worlds are maps in this case

        # World building widget will use an image as a base, and overlay its content on top of that.
        # Users can choose to create their image or use some default ones
        # If no image is provided, start with a default circle 
        # Have edit mode where all locations, places, etc. disappear and user can draw and edit underlying map

        self.mini_widgets_container.visible = False

        # Our column that will display our header filters and body of our widget
        self.body_container.content = ft.Text(f"hello from: {self.title}")

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