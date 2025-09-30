# Notes that are displayed inside of other widgets
import flet as ft
from models.story import Story


# Class that holds our mini note objects inside images or chapters
class MiniNote(ft.Container):
    # Constructor
    def __init__(self, title: str, page: ft.Page, story: Story, data: dict = None):

        super().__init__(
            expand=True,
            spacing=None,
            right=10,
            border_radius=ft.border_radius.all(6),
            controls=[]
        )

        self.visible = True
        
        # Initialize from our parent class 'Widget'. 
        
        self.title = title,  # Title of the widget that will show up on its tab
        self.p = page,   # Grabs our original page for convenience and consistency
        self.story = story,       # Saves our story object that this widget belongs to, so we can access it later
        self.data = data,

        # Required - title, page, story
        # Not required - body, visible

        # If no data is passed in (Newly created chapter), give it default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in

        self.visible = self.data['visible']  # If we will show this widget or not

        self.title_control = ft.TextField(
            value=self.title,
            label=None,
        )

        self.content_control = ft.TextField(
            value=self.data['content'],
            expand=True,
            multiline=True,
        )

        # Load our widget UI on start after we have loaded our data
        self.reload()


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        return {
            'title': self.title,
            'tag': "mini_note",
        
            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            
            'content': "",    # Content of our chapter
        }

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Our column that will display our header filters and body of our widget
        title = ft.TextButton(f"Hello from mini note: {self.title}")

        content = ft.TextField(
            value=self.data['content'],
            expand=True,
            multiline=True,
        )

        self.content = ft.Column(
            spacing=6,
            controls=[title, content],
        )



        