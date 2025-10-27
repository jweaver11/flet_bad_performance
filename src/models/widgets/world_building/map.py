'''
The map class for all maps inside our story
Maps are widgets that have their own drawing canvas, and info display. they can contain nested sub maps as well.
'''

# BLANK NO TEMPLATE MAPS EXIST AS WELL
# ADD DUPLICATE OPTION AS WELL
# Users can choose to create their image or use some default ones, or upload their own
# When hovering over a map, display it on the rail as well so we can see where new sub maps would


import os
import json
import flet as ft
from models.widget import Widget
from models.story import Story
from handlers.verify_data import verify_data
from models.state import State
import flet.canvas as cv
from threading import Thread



class Map(Widget):

    # Constructor. Requires title, owner widget, page reference, world map owner, and optional data dictionary
    def __init__(
        self, 
        title: str, 
        page: ft.Page, 
        directory_path: str, 
        story: Story,
        father: str = None,                     # Parent map this map belongs to. None if top level map
        category: str = None,                   # Type of map this is (world map, continent, country, city, dungeon, room, etc)
        data: dict = None
    ):
        
        # Supported categories: World map, continent, region, ocean, country, city, dungeon, room, none.
        
        
        # Parent constructor
        super().__init__(
            title=title,           
            page=page,                         
            directory_path=directory_path, 
            story=story,
            data=data,  
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   
            {
                'tag': "map", 
                'father': father,               # Parent map this map belongs to. None if top level map
                'category': category,           # Category/psuedo folder this map belongs to
                'is_displayed': True,           # Whether the map is visible in the world building widget or not
                'sub_maps': list,               # Sub maps contained within this map
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
                        'title': str,                   # Title of the category
                        'is_expanded': bool,            # Whether the category is expanded or collapsed
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
        self.maps: list = []


        self.details = {}

        # The Visual Canvas map for drawing
        self.map = cv.Canvas(
            content=ft.GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            expand=True
        )

        # The display container for our map
        self.display: ft.InteractiveViewer = None

        # Load our maps that are held within this amp
        #self.load_sub_maps()
        
        # Load the rest of our map details and data thats not sub maps
        self.load_details()

        # Load our drawing/display
        self.load_display()
        

        # Reloads the information display of the map
        self.reload_widget()


    # Store their data in their own files, so lets make them widgets
    # Their map dict is now list, and contains the title of their sub maps, not the data



    # Called in constructor
    def load_sub_maps(self):
        ''' Loads all sub maps stored in our data into our sub_maps dict'''

        try: 
            # Run through our maps saved in the maps dict
            for map_title, map_data in self.data['maps'].items():

                # Create a new map object
                self.maps[map_title] = Map(
                    title=map_title,
                    owner=self,       # Our world building widget
                    father=self,
                    page=self.p,
                    dictionary_path="maps",
                    data=map_data,
                )
                # Add it to our mini widgets list
                self.mini_widgets.append(self.maps[map_title])

        # Catch errors
        except Exception as e:
            print(f"Error loading maps for the : {e}")

    # Called when loading our drawing data from its file
    def load_display(self):
        ''' Loads our drawing from our saved map drawing file '''

        # Clear existing shapes we might have
        self.map.shapes.clear()

        try:

            # Set our file path
            filename = os.path.join(self.directory_path, f"{self.title}_display.json")

            # Check if file exists, if not create it with empty data
            if not os.path.exists(filename):
                with open(filename, "w") as f:
                    json.dump({}, f)    

            # Load the data from the file
            with open(filename, "r") as f:
                coords = json.load(f)
                for x1, y1, x2, y2 in coords:
                    self.map.shapes.append(cv.Line(x1, y1, x2, y2, paint=ft.Paint(stroke_width=3)))

            # Update the page to reflect loaded drawing
            self.p.update()

        # Handle errors
        except Exception as e:
            print(f"Error loading display from {filename}: {e}")

    # Called to save our drawing data to its file
    def save_display(self):
        ''' Saves our map drawing data to its own json file. Maps are special and get their 'drawing' saved seperately '''

        try:

            # Set our file path
            file_path = os.path.join(self.directory_path, f"{self.title}_display.json")

            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.directory_path, exist_ok=True)
            
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
    def reload_widget(self):       
        ''' Rebuilds/reloads our map UI '''

        # Make it so that maps 'mini widget' shows inside of the map...
        # If two+ maps open at same time, both their mini widgets can be shown at same time
        # We render our map and all the markers, then go through our 'sub maps', find their data, and render them on top as well
        # - Sub maps only have the title still, we don't save their data
        # -- Recursively go through rendering sub maps on top of parent map

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

        self.display = display_container

        self.body_container.content = self.display

        self._render_widget()
    



        