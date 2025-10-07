''' Notes Model for the story object only. Displays in its own widget'''

import flet as ft
from models.story import Story
from models.widget import Widget

    

class Notes(Widget):
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):

        # Check if we're loading a note or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "notes",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our notes json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        # If our note is new and not loaded, give it default data
        if not loaded:
            self.create_default_note_data()  # Create data defaults for each note widget
            self.save_dict()    # Save our data to the file
        
        # Load our widget UI on start after we have loaded our data
        self.reload_widget()

    # Called at end of constructor
    def create_default_note_data(self) -> dict:
        ''' Loads our data from our notes json file. If no file exists, we create one with default data, including the path '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        default_note_data = {
            'tag': "note",  

            "character_count": 0,
            "created_at": None,
            "last_modified": None,
            "content": "",
        }

        # Update existing data with any new default fields we added
        self.data.update(default_note_data)  
        return

    # Called after any changes happen to the data that need to be reflected in the UI, usually just ones that require a rebuild
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
            selected_index=0,       # Since we only have one tab, we make sure it is selected
            animation_duration=0,   # Gets rid of transition animation between tabs
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),  # No padding so it fills the entire container
            label_padding=ft.padding.all(0),    # No padding around the label either
            mouse_cursor=ft.MouseCursor.BASIC,  # Basic mouse cursor when hovering over tabs
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Content of our widget (ft.Container) is our created tabs content
        self.content = content
        