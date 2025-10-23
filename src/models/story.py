''' 
Master Story class that contains data and methods for the entire story 
Our story is an extended ft.View, meaning new routes can display the story object directly
The Story object creates widgets (characters, chapters, notes, etc.) objects that are stored inside of itself.
Stories contain metadata, ui elements, and all the widgets, as well as methods to create new widgets only
'''

import flet as ft
import os
import json
from constants import data_paths
from handlers.verify_data import verify_data


class Story(ft.View):
    # Constructor.
    def __init__(self, title: str, page: ft.Page, data: dict=None, template: str=None, type: str=None):
        # Required: title, page reference
        # Optional: data (if loading), template (sci-fi, fantasy, etc.),
        
        # Parent constructor
        super().__init__(
            route=f"/{title}",    # Sets our route for our new story
            padding=ft.padding.only(top=0, left=0, right=0, bottom=0),    # No padding for the page
            spacing=0,      # No spacing between menubar and rest of page
        )  

        self.title = title  # Gives our story a title when its created
        self.p = page   # Reference to our page object for updating UI elements
        self.data = data    # Sets our data (if any) passed in. New stories just have none
        self.type = type    # Type of story, novel or comic. Affects how templates for creating new content will work

        # Sets our data empty if its none
        if self.data is None or not isinstance(self.data, dict):
            self.data = {}

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'title': self.title,
                'directory_path': os.path.join(data_paths.stories_directory_path, self.title),
                'tag': "story",
                'selected_rail': "characters",
                'content_directory_path': os.path.join(data_paths.stories_directory_path, self.title, "content"),
                'characters_directory_path': os.path.join(data_paths.stories_directory_path, self.title, "characters"),
                'timelines_directory_path': os.path.join(data_paths.stories_directory_path, self.title, "timelines"),
                'world_building_directory_path': os.path.join(data_paths.stories_directory_path, self.title, "world_building"),
                'notes_directory_path': os.path.join(data_paths.stories_directory_path, self.title, "notes"),
                'top_pin_height': 0,
                'left_pin_width': 0,
                'main_pin_height': 0,
                'right_pin_width': 0,
                'bottom_pin_height': 0,
                'created_at': str,
                'last_modified': str,
                'settings': {
                    'type': self.type,  # Novel or comic. Affects templates and default data for new content
                    'multi_planitary': False,   # Whether the story will take place on multiple planets
                },
            },
        )

        # Stories have required structures as well, so we verify they exist or we will error out
        # We also use this function to create most detailed structures from templates if newly created story
        self.verify_story_structure(template)  


            
        # Declare our UI elements before we create them later. They are stored as objects so we can reload them when needed
        self.menubar: ft.Container = None     # Menu bar at top of page
        self.workspaces_rail: ft.Container = None      # Rail on left side showing our 6 workspaces
        self.active_rail: ft.Container = None    # Rail showing whichever workspace is selected
        self.workspace: ft.Container = None        # Main workspace area where our pins display our widgets

        # Our widgets objects
        self.widgets: list = []   # All widgets stored in our story. Easier access to rendering pins this way
        self.chapters: dict = {}   # Chapters stored in our story
        self.images: dict = {}  # Images stored in our story
        self.characters: dict = {}      # Characters stored in our story
        self.timelines: dict = {}   # Only one plotline obj that displays our timlines
        self.world_building: None = ft.Container()  # Only one world building obj that displays our maps
        self.notes: dict = {}   # Notes stored in our story

        # Variables to store our mouse position for opening menus
        self.mouse_x: int = 0
        self.mouse_y: int = 0

        # Called outside of constructor to avoid circular import issues, or it would be called here
        #self.startup() # Called when opening our active story to load all its data and build its view
        
        
    # Called from main when our program starts up. Needs a page reference, thats why not called here
    def startup(self):

        # Loads our content objects from storage into our story object. Includes chapters and images
        # This also loads our drawing board images here, since they can be opened in either workspace
        self.load_content()

        # Loads our characters from file storage into our characters list
        self.load_characters()

        # Loads our timeline from file storage, which holds our timelines
        self.load_timelines()

        # Load our world building objects from file storage
        self.load_world_building()

        # Loads our notes from file storage
        self.load_notes()

        # Everything we loaded above is a widget, but this just adds them all to self.widgets
        self.load_widgets()

        # Builds our view (menubar, rails, workspace) and adds it to the page
        self.build_view()


    # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves the data of our story to its JSON File, and all its folders as well '''

        try:
            # Makes sure our directory path is always right. 
            self.data['directory_path'] = os.path.join(data_paths.stories_directory_path, self.title)
                
            # Our file path we store our data in
            file_path = os.path.join(self.data['directory_path'], f"{self.title}.json")

            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.data['directory_path'], exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:   
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving story to {file_path}: {e}")
            

    # Called when a new story is created and not loaded with any data
    def verify_story_structure(self, template: str=None):
        ''' Creates our story folder structure inside of our stories directory '''

        # Sets our path to our story folder
        directory_path = os.path.join(data_paths.stories_directory_path, self.title)

        # Set our workspace folder structure inside our story folder
        required_story_folders = [
            "content",
            "characters",
            "timelines",
            "world_building",
            "drawing_board",
            "planning",
            "notes",
        ]

        # Create the workspace folder strucutre above
        for folder in required_story_folders:
            folder_path = os.path.join(directory_path, folder)
            os.makedirs(folder_path, exist_ok=True)     # Checks if they exist or not, so they won't be overwritten
            
        # Using templates
        if template is not None:
            pass

        # Create sub folders inside of world building
        maps_folder = os.path.join(directory_path, "world_building", "maps")
        os.makedirs(maps_folder, exist_ok=True)

        # Set our sub folders inside of notes
        notes_folders = [
            "themes",
            "quotes",
            "research",
        ]

        # Create the sub folders inside of notes
        for folder in notes_folders:
            folder_path = os.path.join(directory_path,  "notes", folder)
            os.makedirs(folder_path, exist_ok=True)
        

        # Create the path to the story's JSON file
        directory_path = os.path.join(data_paths.stories_directory_path, self.title)
        
        self.save_dict()
            


    # Called when deleting a widget from our story
    def delete_widget(self, widget) -> bool:
        ''' Deletes the object from our live story object and its reference in the pins.
        We then remove its storage file from our file storage as well. '''
        from models.widget import Widget

        print("Delete widget called")


        # Called inside the delete_object method to remove the file from storage
        def _delete_widget_file(widget: Widget) -> bool:
            ''' Deletes our widgets json file from storage. Returns true if successful, false if not '''

            print("delete widget file called")
            
            try:
                # Grab our widgets tag to see what type of object it is
                tag = widget.data.get('tag', None)

                # Check that somehow our plotline and world building didn't get accidently passed in here
                if tag != "plotline" and tag != "world_building":
                
                    # Check if the file exists before attempting to delete
                    if os.path.exists(widget.directory_path):
                        file_path = os.path.join(widget.directory_path, f"{widget.title}.json")
                        os.remove(file_path)

                        print(f"Successfully deleted file: {widget.directory_path}")
                        return True
                    
                    else:
                        print(f"File not found: {widget.directory_path}")
                        return False
                    
            # Errors
            except (OSError, IOError) as e:
                print(f"Error deleting file {widget.title}.json: {e}")
                return False
            except AttributeError as e:
                print(f"Object missing required attributes (title or path): {e}")
                return False

        # Called if file is successfully deleted. Then we remove the widget from its live storage
        def _delete_live_widget(widget: Widget):
            # Grab our widgets tag to see what type of object it is
            tag = widget.data.get('tag', None)
            
            # Based on its tag, it deletes it from our appropriate dict
            if tag == "chapter":
                if widget.title in self.chapters:
                    del self.chapters[widget.title]
            elif tag == "image":
                if widget.title in self.images:
                    del self.images[widget.title]
            elif tag == "character":
                if widget.title in self.characters:
                    del self.characters[widget.title]
            elif tag == "note":
                if widget.title in self.notes:
                    del self.notes[widget.title]

            
            # Remove from our master widgets list so it won't be rendered anymore
            if widget in self.widgets:
                self.widgets.remove(widget)
        
        # Call our internal functions above
        try:
            # If we can delete the file, we remove the live object
            if _delete_widget_file(widget):

                _delete_live_widget(widget)

                # Reload our workspace to apply the UI Change if was needed
                if widget.visible:
                    self.workspace.reload_workspace(self.p, self)

                print(f"Successfully deleted widget: {widget.title}")

        # Errors
        except Exception as e:
            print(f"Error deleting widget : {e}")
            return


    # Called on story startup to load all our content objects
    def load_content(self):
        ''' Loads our content from our content folder inside of our story folder '''

        #print("Loading content")

        from models.widgets.content.chapter import Chapter

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

        from models.widgets.character import Character
        
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
                        character_title = character_data.get("title", filename.replace(".json", ""))    # TODO Add error handling
                            
                        # Create our character object using our loaded data
                        self.characters[character_title] = Character(character_title, self.p, dirpath, self, character_data)
                        #self.widgets.append(self.characters[character_title])  # Add to our master list of widgets in our story
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading character from {filename}: {e}")

        

    # Called on story startup to create our plotline object.
    def load_timelines(self):
        ''' Creates our timeline object, which in turn loads all our plotlines from storage '''
        from models.widgets.timeline import Timeline
 
        # Check if the plotline folder directory exists. Creates it if it doesn't. 
        # Handles errors on startup if people delete this folder, otherwise uneccessary
        if not os.path.exists(self.data['timelines_directory_path']):
            #print("Plotline folder does not exist, creating it.")
            os.makedirs(self.data['timelines_directory_path'])    
            return
        
        # Iterate through all files in the timelines folder
        for dirpath, dirnames, filenames in os.walk(self.data['timelines_directory_path']):
            for filename in filenames:

                # All our objects are stored as JSON
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)   
                    #print("dirpath = ", dirpath)
                    
                    try:
                        # Read the JSON file
                        with open(file_path, "r", encoding='utf-8') as f:
                            timeline_data = json.load(f)
                        
                        # Extract the title from the data
                        timeline_title = timeline_data.get("title", filename.replace(".json", ""))    
                            
                        # Create our timeline object using our loaded data
                        self.timelines[timeline_title] = Timeline(timeline_title, self.p, dirpath, self, timeline_data)
                        #self.widgets.append(self.characters[character_title])  # Add to our master list of widgets in our story
                    # Handle errors if the path is wrong
                    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                        print(f"Error loading character from {filename}: {e}")
            
        
        # Create our plotline object with no data if story is new, or loaded data if it exists already
        if len(self.timelines) == 0:
            self.timelines["Main_Timeline"] = Timeline(
                title="Main_Timeline", 
                page=self.p, 
                directory_path=dirpath, 
                story=self, 
                data=None
            )

       
    # Called on story startup to load all our world building widget
    def load_world_building(self):
        ''' Loads our world object from storage, or creates a new one if it doesn't exist '''

        from models.widgets.world_building import World_Building
 
        # Check if the plotline folder exists. Creates it if it doesn't. 
        # Handles errors on startup if people delete this folder, otherwise uneccessary
        if not os.path.exists(self.data['world_building_directory_path']):
            #print("Plotline folder does not exist, creating it.")
            os.makedirs(self.data['world_building_directory_path'])    
            return
        
        # Construct the path to plotline.json
        world_building_json_path = os.path.join(self.data['world_building_directory_path'], 'world_building.json')

        # Set data blank initially
        world_building_data = None
        
        # Attempt to open and read the plotline.json file. Sets our stored data if successful
        try:
            with open(world_building_json_path, 'r', encoding='utf-8') as file:
                world_building_data = json.load(file)
                #print("World buliding data: \n", world_building_data)
                
                #print(f"Successfully loaded world data")
        except FileNotFoundError:
            print(f"world.json not found at {world_building_json_path}")
        
        except json.JSONDecodeError as e:
            print(f"Error parsing world_building.json: {e}")
            
        except Exception as e:
            print(f"Unexpected error reading world.json: {e}")
          
        
        # Create our world object with no data if story is new, or loaded data if it exists already
        self.world_building = World_Building("World_Building", self.p, self.data['world_building_directory_path'], self, world_building_data)


    # Called on story startup to load all our notes objects
    def load_notes(self):
        ''' Loads all our note objects stored in the notes directory path'''

        from models.widgets.note import Notes

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

    def load_widgets(self):
        ''' Loads all our widgets (characters, chapters, notes, etc.) into our master list of widgets '''

        from models.app import app

        # Add all our characters to the widgets list
        for character in self.characters.values():
            if character not in self.widgets:
                self.widgets.append(character)

        # Add all our chapters to the widgets list
        for chapter in self.chapters.values():
            if chapter not in self.widgets:
                self.widgets.append(chapter)

        # Add all our images to the widgets list
        for image in self.images.values():
            if image not in self.widgets:
                self.widgets.append(image)

        # Add our plotline to the widgets list
        for timeline in self.timelines.values():
            if timeline not in self.widgets:
                self.widgets.append(timeline)

        # Add our world building to the widgets list
        if self.world_building is not None:
            if self.world_building not in self.widgets:
                self.widgets.append(self.world_building)

        # Add all our notes to the widgets list
        for note in self.notes.values():
            if note not in self.widgets:
                self.widgets.append(note)

        if app.settings not in self.widgets:
            self.widgets.append(app.settings)   # Add our app settings to the widgets list so its accessible everywhere
        
        #print(f"Total widgets loaded for {self.title}: {len(self.widgets)}")


    # Called to create a new chapter
    def create_chapter(self, title: str, directory_path: str=None):
        ''' Creates a new chapter object, saves it to our live story object, and saves it to storage'''
        print("Create chapter called")

        from models.widgets.content.chapter import Chapter

        # If no path is passed in, construct the full file path for the chapter JSON file
        if directory_path is None:   # There SHOULD always be a path passed in, but this will catch errors
            directory_path = self.data['content_directory_path']

        # Save the new chapter
        self.chapters[title] = Chapter(title, self.p, directory_path, self)
        self.widgets.append(self.chapters[title])  # Add to our master list of widgets in our story

        self.active_rail.content.reload_rail()
        self.workspace.reload_workspace(self.p, self)


    # Called to create a new character
    def create_character(self, title: str, directory_path: str=None):
        ''' Creates a new character object, saves it to our live story object, and saves it to storage'''
        #print("Create character called")

        from models.widgets.character import Character

        # If no path is passed in, construct the full file path for the character JSON file
        if directory_path is None:
            directory_path = self.data['characters_directory_path'] # There SHOULD always be a path passed in, but this will catch errors
        
        # Save our new character
        self.characters[title] = Character(title, self.p, directory_path, self)
        self.widgets.append(self.characters[title])  # Add to our master list of widgets in our story

        self.active_rail.content.reload_rail()
        self.workspace.reload_workspace(self.p, self)

    # Called to create a timeline object
    def create_timeline(self, title: str):
        ''' Creates a new timeline and updates the UI. Doesn't need a directory path since its always the same '''
        from models.widgets.timeline import Timeline

        dirpath = self.data['timelines_directory_path']
        self.timelines[title] = Timeline(
            title=title, 
            page=self.p, 
            directory_path=dirpath, 
            story=self, 
            data=None
        )

        self.active_rail.content.reload_rail()
        self.workspace.reload_workspace(self.p, self)


    # Called to create a note object
    def create_note(self, title: str, directory_path: str=None):
        ''' Creates a new note object, saves it to our live story object, and saves it to storage'''
        from models.widgets.note import Notes 

        # If no path is passed in, construct the full file path for the note JSON file
        if directory_path is None:   # There SHOULD always be a path passed in, but this will catch errors
            directory_path = self.data['notes_directory_path']
            #file_path = os.path.join(self.data['notes_directory_path'], note_filename)

        self.notes[title] = Notes(title, self.p, directory_path, self)
        self.widgets.append(self.notes[title])  # Add to our master list of widgets in our story

        self.workspace.reload_workspace(self.p, self)


    # Called when new story object is created, either by program or by being loaded from storage
    def build_view(self) -> list[ft.Control]:
        ''' Builds our 'view' (page) that consists of our menubar, rails, and workspace '''
        from ui.menu_bar import create_menu_bar
        from ui.workspaces_rail import Workspaces_Rail
        from ui.active_rail import Active_Rail
        from ui.workspace import Workspace
        from models.app import app

        page = self.p

        # Clear our controls in our view before building it
        self.controls.clear()

        # Create our page elements as their own pages so they can update
        self.menubar = create_menu_bar(page, self)

        # Create our rails and workspace objects
        self.workspaces_rail = Workspaces_Rail(page, self)  # Create our all workspaces rail
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
                self.workspaces_rail,  # Main rail of all available workspaces
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
