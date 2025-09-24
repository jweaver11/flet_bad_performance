''' 
Master Story class that contains data and methods for the entire story 
This is a dead-end model. Imports nothing else from project (other than constants) to avoid ciruclar import
'''

import flet as ft
import os
import json
from constants import data_paths

# Class for our different story objects
class Story(ft.View):
    # Constructor for when new story is created
    def __init__(self, title: str, page: ft.Page, template: str=None):      # Add is_from_template later
        
        # Parent constructor
        super().__init__(
            route=f"/{title}",    # Sets our route for our new story
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),    # No padding for the page
            spacing=0,      # No spacing between menubar and rest of page
        )  

        # Determine if story is from template and we should load template content when it is created, not loaded
        self.template = template

        self.title = title # Gives our story a title when its created
        self.p = page  # Reference to our page object for updating UI elements
        
        # Declare our UI elements before we create them later. They are stored as objects so we can reload them when needed
        self.menubar = None     # Is an extended ft.Container
        self.all_workspaces_rail = None     # Is an extended ft.Container
        self.active_rail = None     # Is an extended ft.Container
        self.workspace = None       # Is an extended ft.Container


        # Make a list for positional indexing
        self.content = {}

        self.chapters = {}
        self.drawings = {}

        self.characters = {}    
        self.plotline = None    # Singular timeline widget object, that holds our plotlines

        self.world = None
        self.notes = {}

        self.mouse_x = 0
        self.mouse_y = 0

        # Called outside of constructor to avoid circular import issues, or it would be called here
        #self.startup() # The init_saved_stories calls this, or when a new story is created
        
        
    # Called from main when our program starts up. Needs a page reference, thats why not called here
    def startup(self):

        # Loads our info about our story from its JSON file
        self.load_from_dict()    # This function creates one if story object was created not loaded

        # Loads our content objects from storage into our story object. Includes chapters and images
        # This also loads our drawing board images here, since they can be opened in either workspace
        self.load_content()

        # Loads our characters from file storage into our characters list
        self.load_characters()

        # Loads our timeline from file storage, which holds our timelines
        self.load_plotline()

        # Load our world building objects from file storage
        self.load_world()

        # Loads our notes from file storage
        self.load_notes()

        # Builds our view (menubar, rails, workspace) and adds it to the page
        self.build_view()

    
    # Called whenever there are changes in our data that need to be saved
    def save_dict(self, template: str=None):
        ''' Saves the data of our story to its JSON File '''
        #print("save story dict called")

        ''' Loads all our objects from storage (characters, chapters, etc.) and saves them to the story object'''

        # Sets our path to our story folder, and creates the folder structure if it doesn't exist
        directory_path = os.path.join(data_paths.stories_directory_path, self.title)
        story_structure_folders = [
            "content",
            "characters",
            "plotline",
            "world_building",
            "drawing_board",
            "notes",
        ]
        
        # Actually creates the folders in our story path
        for folder in story_structure_folders:
            folder_path = os.path.join(directory_path, folder)
            os.makedirs(folder_path, exist_ok=True) # exist_ok=True avoids errors if folder already exists, and won't re-create it

        # Create our sub folders inside of timeline
        plotline_folders = ["timelines"]
        for folder in plotline_folders:
            folder_path = os.path.join(directory_path, "plotline", folder)
            os.makedirs(folder_path, exist_ok=True)

        self.template = template
        self.template = "default"

        world_building_folders = [
            "locations",
            "lores",
            "power_systems",
            "social_systems",
            "history",
            "geography",
        ]
        for folder in world_building_folders:
            folder_path = os.path.join(directory_path, "world_building", folder)
            os.makedirs(folder_path, exist_ok=True)

        # Load stuff from templates we create. For now, new stories default to this so we can play with folders
        # In the future, only newly created stories get templates
        if self.template == "default":
            # sub template folders inside of notes
            notes_folders = [
                "themes",
                "quotes",
                "research",
            ]
            for folder in notes_folders:
                folder_path = os.path.join(directory_path,  "notes", folder)
                os.makedirs(folder_path, exist_ok=True)

        

        # Create story metadata file
        self.data_file_path = os.path.join(directory_path, f"{self.title}.json")

        self.template = "none"  # Reset this so we don't load template content again if story is loaded from storage
        
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

    # Called when loading a story from storage or when creating a new story
    def load_from_dict(self):
        ''' Loads our story data from its JSON file. If no file exists, we create one with default data '''
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

            'plotline_directory_path': os.path.join(directory_path, "plotline"),
            'timelines_directory_path': os.path.join(directory_path, "plotline", "timelines"),

            'world_building_directory_path': os.path.join(directory_path, "worldbuilding"),

            'notes_directory_path': os.path.join(directory_path, "notes"),

            #'drawing_board_directory_path': os.path.join(directory_path, "drawing_board"), # Not needed, TBD

            # Path to our plotlines inside of our timeline directory

            # Path to our locations inside of our notes directory

            
            'top_pin_height': 0,
            'left_pin_width': 0,
            'main_pin_height': 0,
            'right_pin_width': 0,
            'bottom_pin_height': 0,

            'created_at': None,
            'last_modified': None
        }



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
    def build_view(self) -> list[ft.Control]:
        ''' Builds our 'view' (page) that consists of our menubar, rails, and workspace '''
        from ui.menu_bar import create_menu_bar
        from ui.all_workspaces_rails import All_Workspaces_Rail
        from ui.active_rail import Active_Rail
        from ui.workspace import Workspace
        from models.app import app

        page = self.p

        # Clear our controls in our view before building it
        self.controls.clear()

        # Create our page elements as their own pages so they can update
        self.menubar = create_menu_bar(page, self)

        # Create our rails and workspace objects
        self.all_workspaces_rail = All_Workspaces_Rail(page, self)  # Create our all workspaces rail
        self.active_rail = Active_Rail(page, self)  # Container stored in story for the active rails
        self.workspace = Workspace(page, self)  # Reference to our workspace object for pin locations
        self.workspace.reload_workspace(page, self)  # Load our workspace here instead of in the workspace constructor


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

        # Our gesture detector that holds our row, and allows us to track our mouse position
        gd = ft.GestureDetector(
            content=row,
            expand=True,
            on_hover=self.on_hover,
            hover_interval=100,
        )

        # Views render like columns, so we add elements top-down
        self.controls = [self.menubar, gd]

    # Called every time the mouse moves over the workspace
    def on_hover(self, e):
        ''' Stores our mouse positioning so we know where to open menus '''

        self.mouse_x = e.local_x 
        self.mouse_y = e.local_y
        #print(f"Mouse at x={self.mouse_x}, y={self.mouse_y}")

        
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
            if obj.pin_location == "top" and obj in self.workspace.top_pin.controls:
                self.workspace.top_pin.controls.remove(obj)
            elif obj.pin_location == "left" and obj in self.workspace.left_pin.controls:
                self.workspace.left_pin.controls.remove(obj)
            elif obj.pin_location == "main" and obj in self.workspace.main_pin.controls:
                self.workspace.main_pin.controls.remove(obj)
            elif obj.pin_location == "right" and obj in self.workspace.right_pin.controls:
                self.workspace.right_pin.controls.remove(obj)
            elif obj.pin_location == "bottom" and obj in self.workspace.bottom_pin.controls:
                self.workspace.bottom_pin.controls.remove(obj) 
            else:
                print("Object not found in any pin location, cannot delete")

        # Remove the objects storage file as well
        if hasattr(obj, 'path'):
            delete_object_file(obj)

    # Called on story startup to load all our content objects
    def load_content(self):
        ''' Loads our content from our content folder inside of our story folder '''

        #print("Loading content")

        from models.content.chapter import Chapter

        # Check if the characters folder exists. Creates it if it doesn't. Exists in case people delete this folder
        if not os.path.exists(self.data['content_directory_path']):
            #print("Content folder does not exist, creating it.")
            os.makedirs(self.data['content_directory_path'])    
            return

        # Loads all files inside the content directory and its sub folders
        for dirpath, dirnames, filenames in os.walk(self.data['content_directory_path']):
            for filename in filenames:

                # All our objects are stored as JSON
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)   
                    #print("dirpath = ", dirpath)
                    try:
                        # Read the JSON file
                        with open(file_path, "r", encoding='utf-8') as f:
                            # Set our data to be passed into our objects
                            content_data = json.load(f)
                        
                        # Extract the title from the data
                        content_title = content_data.get("title", filename.replace(".json", ""))

                        # Check our tag to see what type of content it is, and load appropriately
                        if content_data.get("tag", "") == "chapter":
                            
                            self.chapters[content_title] = Chapter(content_title, self.p, dirpath, self, content_data)
                            #print("Chapter loaded")

                        elif content_data.get("tag", "") == "image":
                            print("image tag found, skipping for now")

                        elif content_data.get("tag", "") == "drawing":
                            print("drawing tag found, skipping for now")
                            
                        # Error handling for invalid tags
                        else:
                            print("content tag not valid, skipping")
                            return

                            
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading content from {filename}: {e}")

        # Load animations -- TBD in future if possible


    # Called as part of the startup method during program launch
    def load_characters(self):
        ''' Loads all our characters from our characters folder and adds them to the live story object'''

        #print("Loading characters")

        from models.character import Character
        
        # Check if the characters folder exists. Creates it if it doesn't. Handles errors on startup
        if not os.path.exists(self.data['characters_directory_path']):
            #print("Characters folder does not exist, creating it.")
            os.makedirs(self.data['characters_directory_path'])    
            return
        
        # Iterate through all files in the characters folder
        #for filename in os.listdir(data_paths.characters_path):
        for dirpath, dirnames, filenames in os.walk(self.data['characters_directory_path']):
            for filename in filenames:

                # All our objects are stored as JSON
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)   
                    #print("dirpath = ", dirpath)
                    
                    try:
                        # Read the JSON file
                        with open(file_path, "r", encoding='utf-8') as f:
                            character_data = json.load(f)
                        
                        # Extract the title from the data
                        character_title = character_data.get("title", filename.replace(".json", ""))
                            
                        # Create our character object using our loaded data
                        self.characters[character_title] = Character(character_title, self.p, dirpath, self, character_data)
                        
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading character from {filename}: {e}")

        


    # Called on story startup to create our plotline object.
    def load_plotline(self):
        ''' Creates our timeline object, which in turn loads all our plotlines from storage '''

        from models.plotline.plotline import Plotline
 
        # Check if the plotline folder directory exists. Creates it if it doesn't. 
        # Handles errors on startup if people delete this folder, otherwise uneccessary
        if not os.path.exists(self.data['plotline_directory_path']):
            #print("Plotline folder does not exist, creating it.")
            os.makedirs(self.data['plotline_directory_path'])    
            return
        
        # Construct the path to plotline.json
        plotline_json_path = os.path.join(self.data['plotline_directory_path'], 'plotline.json')

        # Set data blank initially
        plotline_data = None
        
        # Attempt to open and read the plotline.json file. Sets our stored data if successful
        try:
            with open(plotline_json_path, 'r', encoding='utf-8') as file:
                plotline_data = json.load(file)
              
                #print(f"Successfully loaded plotline data: {plotline_data}")
        except FileNotFoundError:
            print(f"plotline.json not found at {plotline_json_path}")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing plotline.json: {e}")
           
        except Exception as e:
            print(f"Unexpected error reading plotline.json: {e}")
            
        
        # Create our plotline object with no data if story is new, or loaded data if it exists already
        self.plotline = Plotline("Plotline", self.p, self.data['plotline_directory_path'], self, plotline_data)
       

    # Called on story startup to load all our world building widget
    def load_world(self):
        ''' Loads our world object from storage, or creates a new one if it doesn't exist '''

        from models.world_building.world_building import World_Building
 
        # Check if the plotline folder exists. Creates it if it doesn't. 
        # Handles errors on startup if people delete this folder, otherwise uneccessary
        if not os.path.exists(self.data['world_building_directory_path']):
            #print("Plotline folder does not exist, creating it.")
            os.makedirs(self.data['world_building_directory_path'])    
            return
        
        # Construct the path to plotline.json
        world_json_path = os.path.join(self.data['world_building_directory_path'], 'world.json')

        # Set data blank initially
        world_data = None
        
        # Attempt to open and read the plotline.json file. Sets our stored data if successful
        try:
            with open(world_json_path, 'r', encoding='utf-8') as file:
                world_data = json.load(file)
                # You can now use plotline_data as needed
                #print(f"Successfully loaded world data")
        except FileNotFoundError:
            print(f"world.json not found at {world_json_path}")
        
        except json.JSONDecodeError as e:
            print(f"Error parsing plotline.json: {e}")
            
        except Exception as e:
            print(f"Unexpected error reading world.json: {e}")
          
        
        # Create our world object with no data if story is new, or loaded data if it exists already
        self.world = World_Building("World_Building_Title", self.p, self.data['world_building_directory_path'], self, world_data)


    # Called on story startup to load all our notes objects
    def load_notes(self):
        ''' Loads all our note objects stored in the notes directory path'''

        from models.note import Notes

        # Check if the notes folder exists. Creates it if it doesn't. Handles errors on startup
        if not os.path.exists(self.data['notes_directory_path']):
            #print("Characters folder does not exist, creating it.")
            os.makedirs(self.data['notes_directory_path'])    
            return
        
        # Iterate through all files in the characters folder
        #for filename in os.listdir(data_paths.characters_path):
        for dirpath, dirnames, filenames in os.walk(self.data['notes_directory_path']):
            for filename in filenames:

                # All our objects are stored as JSON
                if filename.endswith(".json"):

                    file_path = os.path.join(dirpath, filename)     # Pass in whatever our directory is (have not tested)

                    # Set data none initially
                    note_data = None
                    
                    try:
                        # Read the JSON file
                        with open(file_path, "r", encoding='utf-8') as f:
                            note_data = json.load(f)
                        
                        # Extract the title from the data
                        note_title = note_data.get("title", filename.replace(".json", ""))

                        self.notes[note_title] = Notes(note_title, self.p, dirpath, self, note_data)
                        #print(self.notes[note_title].title)      
                    
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading notes from {filename}: {e}")

        #print(f"Total characters loaded for {self.title}: {len(self.characters)}")


    # Called when the button to create a new chapter is clicked
    def create_chapter(self, title: str, directory_path: str=None):
        ''' Creates a new chapter object, saves it to our live story object, and saves it to storage'''
        print("Create chapter called")

        from models.content.chapter import Chapter

        # If no path is passed in, construct the full file path for the chapter JSON file
        if directory_path is None:   # There SHOULD always be a path passed in, but this will catch errors
            directory_path = self.data['characters_directory_path']

        self.chapters[title] = Chapter(title, self.p, directory_path, self)

        #print("Chapter created: " + self.chapters[title].title)
        self.workspace.reload_workspace(self.p, self)

        print("num chapters: " + str(len(self.chapters)))

    # Called when the button to create a new drawing is clicked
    def create_drawing(self, title: str, directory_path: str=None):
        ''' Creates a new drawing object and saves it to our live story object and storage '''

        from models.content.drawing import Drawing
        print("Create drawing called")
        if directory_path is None:   # There SHOULD always be a path passed in, but this will catch errors
            directory_path = self.data['characters_directory_path']

        self.drawings[title] = Drawing(title, self.p, directory_path, self)
        self.workspace.reload_workspace(self.p, self)

        pass


    # Called to create a character object
    def create_character(self, title: str, directory_path: str=None):
        ''' Creates a new character object, saves it to our live story object, and saves it to storage'''
        #print("Create character called")

        from models.character import Character

        # If no path is passed in, construct the full file path for the character JSON file
        if directory_path is None:
            directory_path = self.data['characters_directory_path'] # There SHOULD always be a path passed in, but this will catch errors

        self.characters[title] = Character(title, self.p, directory_path, self)

        #print("Character created: " + character.title)

        self.workspace.reload_workspace(self.p, self)


    # Called to create a note object
    def create_note(self, title: str, directory_path: str=None):
        ''' Creates a new note object, saves it to our live story object, and saves it to storage'''
        from models.note import Notes 

        # If no path is passed in, construct the full file path for the note JSON file
        if directory_path is None:   # There SHOULD always be a path passed in, but this will catch errors
            directory_path = self.data['notes_directory_path']
            #file_path = os.path.join(self.data['notes_directory_path'], note_filename)

        self.notes[title] = Notes(title, self.p, directory_path, self)

        #print("Note created: " + notes.title)

        self.workspace.reload_workspace(self.p, self)

    # text field to name the note    
    def name_note(e):
        title = ft.Text()
        tb1 = ft.TextField(label ="With placeholder", hint_text="Note Title")