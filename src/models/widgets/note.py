''' Notes Model for the story object only. Displays in its own widget'''

import flet as ft
from models.story import Story
from models.widget import Widget
from handlers.verify_data import verify_data
    

class Notes(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our notes json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        # Verifies this object has the required data fields, and creates them if not
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

        # MESSAGE TO CORY: Define all your data fields above, excluding the widget included ones
        # If you want to give default values, see below

        # Check if we loaded our note or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If not loaded, set default values. No new data here, just giving values to existing fields
        if not loaded:
            self.data.update({
                'key1': "value", 
                'key2': 5, 'key3': True
            })
            self.save_dict()

        
        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


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

        # Assign the body_container content as whatever view you have built in the widget
        self.body_container.content = body
        
        # Build it widget function that will handle loading our mini widgets and rendering the whole thing
        self.render_widget()
        