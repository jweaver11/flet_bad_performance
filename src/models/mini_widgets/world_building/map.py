'''
The map class for all maps inside of the world_building widget
Maps are extended mini widgets, with their 'display' being to view of the map, and their mini widget being the map info display
Maps save like normal mini widgets, but have their own drawing data saved in the /maps folder.
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



class Map(MiniWidget):

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
                'tag': "map", 
                'is_displayed': True,           # Whether the map is visible in the world building widget or not
                'maps': dict,                   # Sub maps contained within this map
                'category': category,           # Category/psuedo folder this map belongs to
                'markers': dict,                # Markers placed on the map
                'locations': dict,
                'geography': dict,              # Geography of the world
                'rooms': dict,                  
                'notes': str,

                'sub_categories': {                     # Categories for organizing our maps on the rail
                    'category_name': {
                        'title': str,               # Title of the category
                        'is_expanded': bool,        # Whether the category is expanded or collapsed
                    },
                },
            },
        )

        # State used for drawing
        self.state = State()

        # Have edit mode where all locations, places, etc. disappear and user can draw and edit underlying map
        self.drawing_mode = False  # Whether we are in drawing mode or not


        self.dragging_mode = False  # Whether we are in dragging mode or not. Used to drag around on top of parent map

        # Dict of our sub maps
        self.maps = {}


        self.details = {}

        # Load our maps that are held within this amp
        self.load_sub_maps()
        
        # Load the rest of our map details and data thats not sub maps
        self.load_details()

        

        # The Visual Canvas map for drawing
        self.map = cv.Canvas(
            content=ft.GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            expand=True
        )


        self.display = self.reload_map()    # Make into an interactive viewer
        

        # Builds/reloads our timeline UI
        self.reload_map()

        # Reloads the information display of the map
        self.reload_mini_widget()

    # Called in constructor
    def load_sub_maps(self):
        ''' Loads all sub maps stored in our data into our sub_maps dict'''

        try: 
            # Run through our maps saved in the maps dict
            for map_title, map_data in self.data['maps'].items():

                # Create a new map object
                self.maps[map_title] = Map(
                    title=map_title,
                    owner=self.owner,       # Our world building widget
                    father=self,
                    page=self.p,
                    dictionary_path="maps",
                    data=map_data,
                )
                # Add it to our mini widgets list
                self.owner.mini_widgets.append(self.maps[map_title])

        # Catch errors
        except Exception as e:
            print(f"Error loading maps for the world building widget: {e}")

    # Called when loading our drawing data from its file
    def load_drawing(self):
        ''' Loads our drawing from our saved map drawing file '''

        # Clear existing shapes we might have
        self.map.shapes.clear()

        try:
            # Grab our directory path from our owner widget
            directory_path = os.path.join(self.owner.directory_path, "maps")

            # Set our file path
            file_path = os.path.join(directory_path, f"{self.title}.json")

            # Load the data from the file
            with open(file_path, "r") as f:
                coords = json.load(f)
                for x1, y1, x2, y2 in coords:
                    self.map.shapes.append(cv.Line(x1, y1, x2, y2, paint=ft.Paint(stroke_width=3)))

            # Apply the loaded drawing
            #self.map.update() # OLD
            self.p.update()

        # Handle errors
        except Exception as e:
            print(f"Error loading drawing from {file_path}: {e}")

    # Called to save our drawing data to its file
    def save_drawing(self):
        ''' Saves our map drawing data to its own json file. Maps are special and get their 'drawing' saved seperately '''

        try:

            # Grab our directory path from our owner widget
            directory_path = os.path.join(self.owner.directory_path, "maps")

            # Set our file path
            file_path = os.path.join(directory_path, f"{self.title}.json")

            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w") as f:   
                json.dump(self.state.shapes, f)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving widget to {file_path}: {e}") 
            print("Data that failed to save: ", self.state.shapes)

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
 
    def create_map(self, title: str, category: str=None):

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
        self.owner.mini_widgets.append(self.maps[title])

        # Save our new maps data
        self.data['maps'][title] = self.maps[title].data
        self.save_dict()

        # Reload our widget and rail to show the new map
        self.owner.reload_widget()

        # Catches error if creating default world map on program startup, where UI is not created yet
        if self.owner.story.active_rail is not None:
            self.owner.story.active_rail.content.reload_rail()
    

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline


    async def pan_start(self, e: ft.DragStartEvent):
        self.state.x, self.state.y = e.local_x, e.local_y

    async def pan_update(self, e: ft.DragUpdateEvent):
        def draw_line():
            line = cv.Line(self.state.x, self.state.y, e.local_x, e.local_y,
                           paint=ft.Paint(stroke_width=3))
            self.map.shapes.append(line)
            self.state.shapes.append((self.state.x, self.state.y, e.local_x, e.local_y))
            #self.map.update()
            self.p.update()
            self.state.x, self.state.y = e.local_x, e.local_y
        Thread(target=draw_line, daemon=True).start()

    # Called when we need to rebuild out timeline UI
    def reload_map(self) -> ft.Control:       # Make it return an interactive viewer??
        ''' Rebuilds/reloads our map UI '''

        # Make it so that maps 'mini widget' shows inside of the map...
        # If two+ maps open at same time, both their mini widgets can be shown at same time

        # Display of our map (Gesture detector)
        display = ft.Column([
            self.map,
            ft.Row(
                expand=True,
                controls=[
                    ft.ElevatedButton("Save Drawing", on_click=lambda e: self.save_drawing()),
                    ft.ElevatedButton("Load Drawing", on_click=lambda e: self.load_drawing())
                ]
            )
        ])

        display_container = ft.Container(
            content=display,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.PURPLE),
        )
        

        return display_container
    



        