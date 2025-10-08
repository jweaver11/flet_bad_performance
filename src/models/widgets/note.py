''' Notes Model for the story object only. Displays in its own widget'''

import flet as ft
from models.story import Story
from models.widget import Widget
from handlers.verify_data import verify_data
    

class Notes(Widget):
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our notes json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_note_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            verify_data(
                self,   # Pass in our own data so the function can see the actual data we loaded
                {
                    'tag': str,
                    'character_count': int,
                    'created_at': str,
                    'last_modified': str,
                    'content': str
                },
                tag="note"
            )
        
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
        self.save_dict()
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

        self.body_container.content = body
        
        
        self.render_widget()
        