'''
Parent map class that contains all other sub-maps, such as locations, world maps, continents, countries, cities, dungeons, etc.
Basically, anything that COULD be fleshed out visually. Maps are special mini widgets, 
and have their 'drawing' stored in their own files, while the rest of the data is stored normally
'''

# TYPES OF MAPS, COUNTRIES CONTINENTS ETC. THAT CAN ADD THEIR OWN (SUB) MAPS. EXP. CONTINENT CAN ADD COUNTRIES, REGIONS, ETC
# BLANK NO TEMPLATE MAPS EXIST AS WELL

import os
import json
import flet as ft
from models.widget import Widget
from models.mini_widget import MiniWidget
from handlers.verify_data import verify_data
from models.state import State
import flet.canvas as cv
from threading import Thread

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

        self.state = State()

        self.drawing_data = {}  # Seperate data that holds our drawing info
        self.sub_maps = {}
        self.details = {}

        # Load our sub maps
        self.load_sub_maps()
        
        # Load the rest of our map details and data thats not sub maps
        self.load_details()

        # The control thats displayed on the UI
        self.ui_map: ft.Control = None


        self.cp = cv.Canvas(
            content=ft.GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            expand=True
    )
        

        # Builds/reloads our timeline UI
        self.reload_map()

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
            print("Data that failed to save: ", self.data)

    # Called when loading our drawing data from its file
    def load_drawing(self):
        ''' Loads our drawing from our saved map drawing file '''
        self.cp.shapes.clear()
        try:
            # Grab our directory path from our owner widget
            directory_path = os.path.join(self.owner.directory_path, "maps")

            # Set our file path
            file_path = os.path.join(directory_path, f"{self.title}.json")

            with open(file_path, "r") as f:
                coords = json.load(f)
                for x1, y1, x2, y2 in coords:
                    self.cp.shapes.append(cv.Line(x1, y1, x2, y2, paint=ft.Paint(stroke_width=3)))
            self.cp.update()

        except FileNotFoundError:
            pass
        pass

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


    async def pan_start(self, e: ft.DragStartEvent):
        self.state.x, self.state.y = e.local_x, e.local_y

    async def pan_update(self, e: ft.DragUpdateEvent):
        def draw_line():
            line = cv.Line(self.state.x, self.state.y, e.local_x, e.local_y,
                           paint=ft.Paint(stroke_width=3))
            self.cp.shapes.append(line)
            self.state.shapes.append((self.state.x, self.state.y, e.local_x, e.local_y))
            self.cp.update()
            self.state.x, self.state.y = e.local_x, e.local_y
        Thread(target=draw_line, daemon=True).start()

    # Called when we need to rebuild out timeline UI
    def reload_map(self):


        # Depending on the type of map, we render the Map differently
        # Different right click hover options to add sub maps.
        # I.E. Continents can add countries, regions, oceans, etc.. But countries cant add continents, etc.
        # Add option to have the mini widget show on larger portion of screen, like an expand button at bottom left or right

        # Content of our Timeline (Gesture detector)
        self.content = ft.Column([
            self.cp,
            ft.Row([
                ft.ElevatedButton("Save Drawing", on_click=lambda e: self.save_drawing()),
                ft.ElevatedButton("Load Drawing", on_click=lambda e: self.load_drawing())
            ])
        ])
    



        