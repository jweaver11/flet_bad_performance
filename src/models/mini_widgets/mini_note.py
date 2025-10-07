import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget


# Class that holds our mini note objects inside images or chapters
class MiniNote(MiniWidget):
    # Constructor
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):

        # Parent Constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        )

        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If this is a new widget (Not loaded), give it default data all widgets need
        if not loaded:
            self.create_default_data()  # Create default data if none was passed in

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            self.verify_mini_note_data()

            

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

        # Load our widget UI on start after we have loaded our data
        self.reload_mini_widget()

    def create_default_mini_note_data(self) -> dict:
        ''' Gives default data for all mini note objects and alters the tag '''

        default_mini_note_data = {
            'tag': "mini_note",  # Tag to identify this as a mini note
            'content': "",    # Content of our mini note
        }

        # Update existing data with any new default fields we added
        self.data.update(default_mini_note_data)
        self.save_dict()
        return self.data
    
    # Called to fix any missing data fields in loaded mini notes. Only fixes our missing fields above
    def verify_widget_data(self):
        ''' Verify loaded any missing data fields in existing mini notes '''

        # Required data for all widgets and their types
        required_data_types = {
            'tag': str,
            'content': str
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'tag': "mini_note",
            'content': "",
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        self.data['tag'] = "mini_note"   # Make sure our tag is always correct

        # Save our updated data
        self.save_dict()
        return



    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_mini_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Our column that will display our header filters and body of our widget
        self.title_control = ft.TextButton(
            f"Hello from mini note: {self.title}",
            on_click=self.toggle_visibility,
        )

        self.content_control = ft.TextField(
            #value=self.data['content'],
            label="Body",
            expand=True,
            multiline=True,
        )

        self.content = ft.Column(
            spacing=6,
            controls=[self.title_control, self.content_control],
        )

        self.p.update()




        