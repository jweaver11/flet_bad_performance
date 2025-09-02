''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project (other than constants) to avoid ciruclar import
'''

import flet as ft
import os
import json
from constants import data_paths


class Story(ft.View):
    # Constructor for when new story is created
    def __init__(self, title: str, page: ft.Page):
        
        # Parent constructor
        super().__init__(
            route=f"/{title}",    # Sets our route for our new story
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),    # No padding for the page
            spacing=0,      # No spacing between menubar and rest of page
        )  
       
        self.title = title # Gives our story a title when its created
        self.p = page  # Reference to our page object for updating UI elements. Sometimes we need it, sometimes not
        
        # Declare our UI elements before we create them later. They are stored as objects so we can reload them when needed
        self.all_workspaces_rail = None  # Is a extended ft.Container
        self.active_rail = None     # Is a extended ft.Container
        self.workspace = None   # Is a extended ft.Container

        # Objects for our active rail content
        self.content_rail = None  # Is an extended ft.Container
        self.characters_rail = None  # Is an extended ft.Container
        self.plot_and_timeline_rail = None  # Is an extended ft.Container
        self.world_building_rail = None  # Is an extended ft.Container
        self.drawing_board_rail = None  # Is an extended ft.Container
        self.notes_rail = None  # Is an extended ft.Container

        #data_paths.set_active_story_path(title)  # Set our active story path to the newly created story

        # Our folder structure for the story
        story_structure_folders = [
            "content",
            "characters",
            "plot_and_timeline",
            "worldbuilding",
            "drawing_board",
            "notes",
        ]
        
        # Actually creates the folders in our story path
        for folder in story_structure_folders:
            folder_path = os.path.join(data_paths.active_story_path, folder)
            os.makedirs(folder_path, exist_ok=True) # exist_ok=True avoids errors if folder already exists, and won't re-create it

        notes_folders = [
            "themes",
            "quotes",
            "research",
        ]
        for folder in notes_folders:
            folder_path = os.path.join(data_paths.notes_path,  folder)
            os.makedirs(folder_path, exist_ok=True)

        # Create story metadata file
        self.data_file_path = os.path.join(data_paths.active_story_path, f"{self.title}.json")

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters

        #self.startup()
        
        
    # Called from main when our program starts up. Needs a page reference, thats why not called here
    def startup(self):
        ''' Loads all our objects from storage (characters, chapters, etc.) and saves them to the story object'''

        # Loads our info about our story from its JSON file
        self.load_dict()    # This function creates one if story object was created not loaded

        # Loads our characters from file storage into our characters list
        self.load_characters(self.p)

        self.build_view(self.p)

        from handlers.reload_workspace import reload_workspace

        # Loads our widgets for the program whenever it starts. Make sure its called after page is built
        reload_workspace(self.p, self) 
    

    def save_dict(self):
        #print("save story dict called")
        
        # Create the path to the story's JSON file
        directory_path = os.path.join(data_paths.stories_directory_path, self.title)
        story_data_file_path = os.path.join(directory_path, f"{self.title}.json")
        
        try:
            # Save our data to file
            with open(story_data_file_path, "w") as f:
                json.dump(self.data, f, indent=4)
            #print(f"Story data saved to {story_file_path}")
            
        except (PermissionError, OSError) as e:
            print(f"Error saving story data: {e}")

    def load_dict(self):
        #print("load story dict called")

        # Create the path to the story's directory and data JSON file
        directory_path = os.path.join(data_paths.stories_directory_path, self.title)
        story_data_file_path = os.path.join(directory_path, f"{self.title}.json")

        
        # Default data structure
        default_data = {
            'title': self.title,
            'directory_path': directory_path,  # Path to our parent folder that will hold our story json objects
            'story_data_file_path' : story_data_file_path,  # Path to our main story json file

            'selected_rail': 'characters',

            # Paths to our workspaces for easier reference later
            'content_directory_path': os.path.join(directory_path, "content"),
            'characters_directory_path': os.path.join(directory_path, "characters"),
            'plot_and_timeline_directory_path': os.path.join(directory_path, "plot_and_timeline"),
            'worldbuilding_directory_path': os.path.join(directory_path, "worldbuilding"),
            'drawing_board_directory_path': os.path.join(directory_path, "drawing_board"),
            'notes_directory_path': os.path.join(directory_path, "notes"),

            'top_pin_height': 0,
            'left_pin_width': 0,
            'main_pin_height': 0,
            'right_pin_width': 0,
            'bottom_pin_height': 0,

            'created_at': None,
            'last_modified': None
        }

        # OUr paths inside the story object
        #content_path = os.path.join(active_story_path, "content")
        #characters_path = os.path.join(active_story_path, "characters")
        #plot_and_timeline_path = os.path.join(active_story_path, "plot_and_timeline")
        #worldbuilding_path = os.path.join(active_story_path, "worldbuilding")
        #drawing_board_path = os.path.join(active_story_path, "drawing_board")
        #notes_path = os.path.join(active_story_path, "notes")

        try:
            # Check if the story file exists
            if os.path.exists(story_data_file_path):
                # Load existing data from file
                with open(story_data_file_path, 'r') as f:
                    loaded_data = json.load(f)
                
                # Merge loaded data with default data (in case new fields were added)
                self.data = {**default_data, **loaded_data}
                #print(f"Loaded story data from {story_data_file_path}")

                self.title = self.data.get('title', self.title)  # Update title in case it was changed

                # Set our saved pin sizes
                #self.top_pin.height = self.data.get('top_pin_height', 0)
                #self.left_pin.width = self.data.get('left_pin_width', 0)
                #self.right_pin.width = self.data.get('right_pin_width', 0)
                #self.bottom_pin.height = self.data.get('bottom_pin_height', 0)
            else:
                # File doesn't exist, use default data
                self.data = default_data
                #print(f"Story file {story_data_file_path} not found, using default data")
                
                # Create the file with default data
                self.save_dict()
                
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading story data: {e}")
            # Fall back to default data on error
            self.data = default_data

    # Called when new story object is created, either by program or by being loaded from storage
    def build_view(self, page: ft.Page) -> list[ft.Control]:
        ''' Builds our 'view' (page) that consists of our menubar, rails, and workspace '''
        from ui.menu_bar import create_menu_bar
        from ui.all_workspaces_rails import All_Workspaces_Rail
        from ui.active_rail import Active_Rail
        from ui.workspace import Workspace
        from models.app import app

        # Clear our controls in our view before building it
        self.controls.clear()

        # Create our page elements as their own pages so they can update
        menubar = create_menu_bar(page, self)

        # Create our rails and workspace objects
        self.all_workspaces_rail = All_Workspaces_Rail(page, self)  # Create our all workspaces rail
        self.active_rail = Active_Rail(page, self)  # Container stored in story for the active rails
        self.workspace = Workspace(page, self)  # Reference to our workspace object for pin locations

        # Called when hovering over resizer to right of the active rail
        def show_horizontal_cursor(e: ft.HoverEvent):
            ''' Changes the cursor to horizontal when hovering over the resizer '''

            e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
            e.control.update()

        # Called when resizing the active rail by dragging the resizer
        def move_active_rail_divider(e: ft.DragUpdateEvent):
            ''' Responsible for altering the width of the active rail '''

            if (e.delta_x > 0 and self.active_rail.width < page.width/2) or (e.delta_x < 0 and self.active_rail.width > 100):
                self.active_rail.width += e.delta_x    # Apply the change to our rail
                
            page.update()   # Apply our changes to the rest of the page

        # Called when app stops dragging the resizer to resize the active rail
        def save_active_rail_width(e: ft.DragEndEvent):
            ''' Saves our new width that will be loaded next time app opens the app '''

            app.settings.data['active_rail_width'] = self.active_rail.width
            app.settings.save_dict()
            print("Active rail width: " + str(self.active_rail.width))

        # The actual resizer for the active rail (gesture detector)
        active_rail_resizer = ft.GestureDetector(
            content=ft.Container(
                width=10,   # Total width of the GD, so its easier to find with mouse
                bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),  # Matches our bg color to the active_rail
                # Thin vertical divider, which is what the app will actually drag
                content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.OUTLINE_VARIANT),
                padding=ft.padding.only(left=8),  # Push the 2px divider ^ to the right side
            ),
            on_hover=show_horizontal_cursor,    # Change our cursor to horizontal when hovering over the resizer
            on_pan_update=move_active_rail_divider, # Resize the active rail as app is dragging
            on_pan_end=save_active_rail_width,  # Save the resize when app is done dragging
        )

        # Save our 2 rails, divers, and our workspace container in a row
        row = ft.Row(
            spacing=0,  # No space between elements
            expand=True,  # Makes sure it takes up the entire window/screen

            controls=[
                self.all_workspaces_rail,  # Main rail of all available workspaces
                ft.VerticalDivider(width=2, thickness=2, color=ft.Colors.OUTLINE_VARIANT),   # Divider between workspaces rail and active_rail

                self.active_rail,    # Rail for the selected workspace
                active_rail_resizer,   # Divider between rail and work area
                
                self.workspace,    # Work area for pagelets
            ],
        )

        # Views render like columns, so we add elements top-down
        self.controls = [menubar, row]

        
    # Called when saving new objects to the story (characters, chapters, etc.)
    def save_object(self, obj):
        ''' Handles logic on where to save the new object in our live story object.
        Whenever a new object is created, it loads its data using its given path.
        If it has no data, it creates a new file to store data, so we don't need to save the data here.'''

        print("Save object called")

        # Called if we're saving a character object
        def save_character(obj):
            self.characters.append(obj) # Save to our characters list

        # Called if saving a chapter object
        def save_chapter(obj):
            print(obj)  # WIP

        # Handles our logic for saving objects. Checks the tag of the object to route it to correct save function
        if hasattr(obj, 'tag'):

            # Characters
            if obj.tag == "character":
                save_character(obj)

            # Chapters
            elif obj.tag == "chapter":
                save_chapter(obj)
            
            else:
                print("object does not have a valid tag dummy")

        # If no tag exists, we do nothing
        else:
            print("object has no tag at all you even bigger dummy")


    # Called when deleting an object from the story (character, chapter, etc.)
    def delete_object(self, obj):
        ''' Deletes the object from our live story object and its reference in the pins.
        We then remove its storage file from our file storage as well. '''

        print("Delete object called")

        # Called inside the delete_object method to remove the file from storage
        def delete_object_file(obj):
            ''' Grabs our objects path, and removes the associated file from storage '''

            print("delete object from file called")
            
            try:
                
                # Check if the file exists before attempting to delete
                if os.path.exists(obj.path):
                    os.remove(obj.path)
                    print(f"Successfully deleted file: {obj.path}")
                else:
                    print(f"File not found: {obj.path}")
                    
            except (OSError, IOError) as e:
                print(f"Error deleting file {obj.title}.json: {e}")
            except AttributeError as e:
                print(f"Object missing required attributes (title or path): {e}")

        # Remove from characters list if it is a character
        if hasattr(obj, 'tag') and obj.tag == "character":
            # Remove object from the characters list
            if obj in self.characters:
                self.characters.remove(obj)
    
        # Find our objects reference in the pins and remove it
        if hasattr(obj, 'pin_location'):
            if obj.pin_location == "top" and obj in self.top_pin.controls:
                self.top_pin.controls.remove(obj)
            elif obj.pin_location == "left" and obj in self.left_pin.controls:
                self.left_pin.controls.remove(obj)
            elif obj.pin_location == "main" and obj in self.main_pin.controls:
                self.main_pin.controls.remove(obj)
            elif obj.pin_location == "right" and obj in self.right_pin.controls:
                self.right_pin.controls.remove(obj)
            elif obj.pin_location == "bottom" and obj in self.bottom_pin.controls:
                self.bottom_pin.controls.remove(obj)
            else:
                print("Object not found in any pin location, cannot delete")

        # Remove the objects storage file as well
        if hasattr(obj, 'path'):
            delete_object_file(obj)

    # Called as part of the startup method during program launch
    def load_characters(self, page: ft.Page):
        ''' Loads all our characters from our characters folder and adds them to the live story object'''

        #print("load characters called")
        
        # Check if the characters folder exists. Creates it if it doesn't. Handles errors on startup
        if not os.path.exists(self.data['characters_directory_path']):
            #print("Characters folder does not exist, creating it.")
            os.makedirs(data_paths.characters_path)
            return
        
        # Iterate through all files in the characters folder
        #for filename in os.listdir(data_paths.characters_path):
        for dirpath, dirnames, filenames in os.walk(self.data['characters_directory_path']):
            for filename in filenames:

                # All our objects are stored as JSON
                if filename.endswith(".json"):
                    file_path = os.path.join(self.data['characters_directory_path'], filename)
                    
                    try:
                        # Read the JSON file
                        with open(file_path, "r") as f:
                            character_data = json.load(f)
                        
                        # Extract the title from the data
                        character_title = character_data.get("title", filename.replace(".json", ""))
                        
                        # Create Character object with the title
                        from models.character import Character
                        character = Character(character_title, page, self)
                        #character.path = file_path  # Set the path to the loaded file
                        self.characters.append(character)
                        
                        #print(f"Loaded character: {character_title}")
                        #print(f"Number of characters loaded: {len(self.characters)}")
                    
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading character from {filename}: {e}")


    # Called to create a character object
    def create_character(self, title: str):
        ''' Creates a new character object, saves it to our live story object, and saves it to storage'''

        from models.character import Character

        print("Create character called")

        # Create the character object
        character = Character(title, self.p, self)

        print("Character created: " + character.title)

        # Save it to our live story object
        #self.save_object(character)

        self.characters.append(character)

        # Update the page to show the new character in the characters rail if its active
        #self.p.update()

        self.workspace.reload_workspace(self.p, self)

        return character

