# Notes that are displayed inside of other widgets
import flet as ft
from models.story import Story
from models.mini_widget import MiniWidget
from models.widget import Widget


# Class that holds our mini note objects inside images or chapters
class MiniNote(MiniWidget):
    # Constructor
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        # Check if we're loading a mini note or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # Initialize our mini widget owner class
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        )

        # If our character is new and not loaded, give it default data
        if not loaded:
            self.create_default_mini_note_data()  # Create data defaults for each chapter widget
            self.save_dict()    # Save our data to the file
            

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




        