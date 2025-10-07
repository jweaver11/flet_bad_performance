import flet as ft
from models.widget import Widget
from models.story import Story


# Our widget class that displays our world building and lore information
class World_Building(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # Set our passed in data to our objects data
        )
        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_world_building_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            self.verify_world_building_data()

        self.reload_widget()
        
    # Called when new story is created, and no data for our world exists
    def create_default_world_building_data(self):
        ''' Gives our world building widget default data it will need if none exists '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # Default data for our world building widget
        default_world_building_data = {
            'tag': "world_building",  
            'content': "",
        }

        # Update existing data with any new default fields we added
        self.data.update(default_world_building_data)
        self.save_dict()
        return
    
    # Called to verify loaded data
    def verify_world_building_data(self):
        ''' Verify loaded any missing data fields in existing chapters '''

        # Required data for all widgets and their types
        required_data_types = {
            'tag': str,
            'content': str
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'tag': "chapter",
            'content': "",
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        self.data['tag'] = "world_building"   # Make sure our tag is always correct

        # Save our updated data
        self.save_dict()
        return

    def reload_widget(self):
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


#locations = {}
#self.lore = {}
#self.power_systems = {}
##social_systems = {}
#self.geography = {}

# Description of world
# Power systems (if any)
# Social systems
# Geography
# History
# ...