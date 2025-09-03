import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget


# Class that holds our timeline
class Plotline(Widget):
    def __init__(self, title: str, page: ft.Page, file_path: str, story: Story):
        

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "notes",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            file_path = file_path,  # Path to our notes json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
        )

        # Loads our notes data from file, or sets default data if no file exists. This is called at the end of the constructor
        self.load_from_dict(file_path)

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()

    # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves our data to our notes json file. '''

        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=4)
            print(f"Notes saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving notes to {self.file_path}: {e}")

    # Called at end of constructor
    def load_from_dict(self, file_path: str):
        ''' Loads our data from our notes json file. If no file exists, we create one with default data, including the path '''

        # Sets the path to our file based on our title inside of the notes directory
        timeline_file_path = file_path

        ## IN THE FUTURE, WE WILL ITERATE THROUGH ALL THE FILES IN ALL THE SUBFOLDERS...
        ## OF THE story.data['notes_directory_path'] TO LOAD ALL OUR NOTES, AND PASS IN THE PATH FROM THERE.
        ## FOR NOW, ALL NOTES JUST STORED INSIDE THE NOTES DIRECTORY, SO IT DOESNT MATTER

        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        default_data = {
            'title': self.title,
            'file_path': timeline_file_path,
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            'branches': {
                'title': "branch_title",
                'main_story_start_date': None,
                'main_story_end_date': None,
                'timeline_begin_date': None,
                'timeline_end_date': None,
                'timeskips': {'title': "timeskip_title", 'start_date': None, 'end_date': None},
                'plot_points': {
                    'event_title': "Event Title",
                    'event_description': "Event Description",
                    'event_date': None,
                    'event_time': None,
                    'involved_characters': [],
                    'related_locations': [],
                    'related_items': [],
                },
                'arcs': {
                    'arc_title': "Arc Title",
                    'arc_description': "Arc Description",
                    'start_date': None,
                    'end_date': None,
                    'involved_characters': [],
                },
            },
        }

        try:
            # Try to load existing settings from file
            if os.path.exists(timeline_file_path):
                self.path = timeline_file_path  # Set the path to the file
                #print(f"Loading character data from {self.path}")
                with open(timeline_file_path, "r") as f:
                    loaded_data = json.load(f)
                
                # Start with default data and update with loaded data
                self.data = default_data.copy()
                self.data.update(loaded_data)

                # Set specific attributes form our data
                self.visible = self.data.get('visible', True)   # live visible bool = data visible bool, default to true if error
                
            else:
               
                self.data = default_data    # Set our live object data to our default data
                
                self.save_dict()  # Create the file (or write to it) that saves our live object data

        # Our error for our try statement. Uses our default error if there is an error loading the file/doesn't exist
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading story data: {e}")
            # Fall back to default data on error
            self.data = default_data

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Body of the tab, which is the content of flet container
        body = ft.Container(
            expand=True,
            padding=6,
            #bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.ON_SECONDARY),
            content=ft.Column([
                ft.Text("hi from " + self.title),
            ])
        )

        # our tab.content is the body of our widget that we build above.
        self.tab.content=body   # We add this in combo with our 'tabs' later

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