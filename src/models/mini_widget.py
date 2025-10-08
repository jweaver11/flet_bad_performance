'''
Parent class for mini widgets, which are extended flet containers used as information displays on the side of the parent widget
Makes showing detailed information easier without rending and entire widget where it doesn't make sense
'''


import flet as ft
from models.widget import Widget
from handlers.verify_data import verify_data



class MiniWidget(ft.Container):
    # Constructor. All mini widgets require a title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):

        # Parent constructor
        super().__init__(
            expand=True,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.GREEN),
        )
           
        self.title = title  # Title of the widget that will show up on its tab
        self.owner = owner  # The widget that contains this mini widget. (Can't use parent because ft.Containers have hidden parent attribute)
        self.p = page   # Grabs our original page for convenience and consistency
        self.data = data    # Pass in our data when loading existing mini widgets

        # Check if we loaded our mini widget or created a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # If this is a new mini widget (Not loaded), give it default data all widgets need
        if not loaded:
            self.create_default_data()  # Create default data if none was passed in

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            verify_data(
                self,   # Pass in our object so we can access its data and change it
                {   # Pass in the required fields and their types
                    'title': str,       # Title of the mini widget, should match the object title
                    'tag': str,     # Default mini widget tag, but should be overwritten by child classes
                    'visible': bool,        # If the widget is visible. Flet has this parameter build in, so our objects all use it
                    'is_selected': bool,    # If the mini widget is selected in the owner's list of mini widgets, to change parts in UI
                },
            )


        # Apply our visibility
        self.visible = self.data['visible']
        self.is_selected = False    # Check if we are selected for ui purposes

        # UI Elements
        self.title_control = ft.TextField(
            value=self.title,
            label=None,
        )

        self.content_control = ft.TextField(
            #value=self.data['content'],
            label="Body",
            expand=True,
            multiline=True,
        )

    # Called when saving changes in our mini widgets data to the OWNERS json file
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        if self.owner.data is None or not isinstance(self.data, dict):
            print("Error: owner data is None, cannot save mini widget data")
            return

        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['mini_widgets'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Creates default data for the mini widget when no data is passed in '''

        # Catch errors where data is corrupted or not initialized properly/deleted from the file
        if self.data is None or not isinstance(self.data, dict):
            self.data = {}

        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        default_data = {
            'title': self.title,        
            'tag': "",   
            'visible': True,    
            'is_selected': False, 
        }

        # Update existing data with any new default fields we added
        self.data.update(default_data)
        self.save_dict()
        return self.data


    # Called when clicking x to hide the mini note
    def toggle_visibility(self, e):
        ''' Shows or hides our mini widget, depending on current state '''

        print(f"Toggling visibility for mini widget: {self.title}")

        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        
        self.save_dict()
        self.p.update()

        print(f"Mini widget: {self.title} visibility is now: {self.visible}")

        