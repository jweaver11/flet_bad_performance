import flet as ft
from models.widget import Widget


# Parent Class that holds our mini note objects (ft.Containers), that are held within widget objects only
# These child objects appear inside of another widget, (from right or left) to show more detail and child information
# Example, clicking a plotpoint, arc, etc. on a timeline brings up a mini widget
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

        # Check if we loaded our mini widget or not
        if self.data is None:
            loaded = False
        else:
            loaded = True

        # If this is a new mini widget (Not loaded), give it default data all widgets need
        if not loaded:
            self.create_default_data()  # Create default data if none was passed in

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            self.verify_mini_widget_data()




        # Apply our visibility
        self.visible = self.data['visible']

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
            'tag': "mini_widget",   # Default mini widget tag, but should be overwritten by child classes
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            'is_selected': False, # If the mini widget is selected in the owner's list of mini widgets, to change parts in UI
        }

        # Update existing data with any new default fields we added
        self.data.update(default_data)
        self.save_dict()
        return
    
    def verify_mini_widget_data(self):

        print("Verifying mini widget data for ", self.title)
        
        # Required data for all widgets and their types
        required_data_types = {
            'title': str,
            'tag': str,
            'visible': bool,
            'is_selected': bool,
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'title': self.title,
            'tag': "mini_widget",   # Default mini widget tag, but should be overwritten by child classes
            'visible': True,
            'is_selected': False,
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]
                print(key, " missing or incorrect type, setting to default: ", self.data[key])
            else:
                print(key, " exists and is correct type")

        # Save our updated data
        self.save_dict()
        return

    
    # Called to fix any missing data fields in existing mini widgets. Only fixes our missing fields above
    def repair_data(self, tag: str):
        ''' Repairs any missing data fields in existing mini widgets '''

        # Error handling
        if self.data is None or not isinstance(self.data, dict):
            self.data = {}

        # Make sure our mini widget has its required data that it needs to function
        required_data = {
            'title': self.title,    # Fix our title if broke
            'tag': tag,         # Fix our tag so we know what to load
            'visible': self.visible,        # Keep our current visibility state
            'is_selected': False,        # Just assume we're not selected
        }

        # Update our data with any missing fields
        self.data.update(required_data)
        self.save_dict()
        return

    # Called when clicking x to hide the mini note
    def toggle_visibility(self, e):
        ''' Shows or hides our mini widget, depending on current state '''

        print(f"Toggling visibility for mini widget: {self.title}")

        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        
        self.save_dict()
        self.p.update()

        print(f"Mini widget: {self.title} visibility is now: {self.visible}")

        