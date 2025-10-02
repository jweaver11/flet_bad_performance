# Notes that are displayed inside of other widgets
import flet as ft
from models.story import Story
from models.mini_widget import MiniWidget
from models.widget import Widget


# Class that holds our mini note objects inside images or chapters
class MiniNote(MiniWidget):
    # Constructor
    def __init__(self, title: str, parent: Widget, page: ft.Page, data: dict=None):

        # Initialize our mini widget parent class
        super().__init__(
            title=title,        # Title of our mini note
            parent=parent,      # Parent widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        )

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


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        return {
            'title': self.title,
            'tag': "mini_note",
        
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            
            'content': "",    # Content of our chapter
            'One': 1,
        }
    
    # Called when clicking x to hide the mini note
    def toggle_visible(self, e):
        self.visible = not self.visible
        self.p.update()

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_mini_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Our column that will display our header filters and body of our widget
        self.title_control = ft.TextButton(
            f"Hello from mini note: {self.title}",
            on_click=self.toggle_visible,
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



        