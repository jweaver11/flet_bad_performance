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
from models.story import Story
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Map(ft.GestureDetector):

    # Contsturctor. Accepts tile, file path, and optional data if plotline is beaing created from existing json file
    def __init__(self, title: str, directory_path: str, page: ft.Page, story: Story, data: dict=None):

        # Initialize our flet control. Theres problems with the data if this is not done first
        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title  # Set our title
        self.directory_path = directory_path  # Path to our plotline json file
        self.p = page  # Page reference for convenience
        self.story = story  # Story object that contains this timeline
        self.data = data    # Set our data. If new object, this will be None, otherwise its loaded data


        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_map_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            verify_data(
                self,   # Pass in our own data so the function can see the actual data we loaded
                {},
                #tag="map"
            )


        # Apply our visibility
        self.visible = self.data['visible']

        # Need to be able to draw maps for continents, countries, regions, dungeons, cities, etc.
        # Needs drawing functionality, as well as ability to just add locations, markers, notes
        
        self.maps = {}

        # Load the rest of our data from the file
        

        # Builds/reloads our timeline UI
        self.reload_map()

    # Called when saving changes in our timeline object to file
    def save_dict(self):
        ''' Saves our data dict to our json file '''

        # Make the correct file path
        file_path = os.path.join(self.directory_path, f"{self.title}.json")

        # Takes our 

        try:
            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:   
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving object to {file_path}: {e}")
        
    

    # Called at the constructor if this is a new timeline that was not loaded
    def create_default_map_data(self) -> dict:
        ''' Returns a default dict data sctructure for a new timeline '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        default_map_data = {
            
            'tag': "map",

            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
             
        }

        # Update existing data with any new default fields we added
        self.data.update(default_map_data)
        self.save_dict()
        return self.data

    
    
    
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
    



        