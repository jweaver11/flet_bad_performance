import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget


# Class that holds our timeline object, that holds our plotlines
# Stories generally only have one plotline, unless we want multiple timelines, regression, multiverse, etc.
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, file_path: str, story: Story):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "chapter",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            file_path = file_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
        )

        
        # Loads our notes data from file, or sets default data if no file exists. Also loads our plotlines
        self.load_from_dict(file_path)

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


    # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves our data to our timeline json file. '''

        #print(f"Saving chapter data to {self.data['file_path']}")

        try:
            with open(self.data['file_path'], "w") as f:
                json.dump(self.data, f, indent=4)
            #print(f"Plotline saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving chapter to {self.data['file_path']}: {e}")

    # Called at end of constructor
    def load_from_dict(self, file_path: str):
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''

        # Sets the path to our file based on our title inside of the timeline directory
        chapter_file_path = file_path
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        default_data = {
            'title': self.title,
            'file_path': chapter_file_path,
            'tag': self.tag,
            'pin_location': "bottom",
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            
            'content': "",    # Content of our chapter
        }
        
        # Loads our TIMELINE object only
        try:
            # Try to load existing settings from file
            if os.path.exists(chapter_file_path):
                self.file_path = chapter_file_path  # Set the path to the file
                #print(f"Loading character data from {self.path}")
                with open(chapter_file_path, "r") as f:
                    loaded_data = json.load(f)
                
                # Start with default data and update with loaded data
                self.data = {**default_data, **loaded_data}

                # Set specific attributes form our data
                self.title = self.data.get('title', self.title)  # live title = data title, default to current title if error
                self.visible = self.data.get('visible', True)   # live visible bool = data visible bool, default to true if error
                self.file_path = self.data.get('file_path', chapter_file_path)  # live file path = data file path, default to constructed path if error
                
            else:
               
                self.data = default_data    # Set our live object data to our default data
                
                self.save_dict()  # Create the file (or write to it) that saves our live object data

        # Our error for our try statement. Uses our default error if there is an error loading the file/doesn't exist
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading timeline data: {e}")
            # Fall back to default data on error
            self.data = default_data


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''


        # Our column that will display our header filters and body of our widget
        body = ft.Text(f"hello from: {self.title}")


        # our tab.content is the column we build above.
        self.tab.content=body  # We add this in combo with our 'tabs' later

        # Sets our actual 'tabs' portion of our widget, since 'tab' needs to nest inside of 'tabs' in order to work
        content = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Content of our widget (ft.Container) is our created tabs content
        self.content = content

        