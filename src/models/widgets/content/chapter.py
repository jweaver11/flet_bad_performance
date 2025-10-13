import flet as ft
from models.story import Story
from models.widget import Widget
from handlers.verify_data import verify_data


# Class that holds our text chapter objects
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):

        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our chapters json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # This gets initialized at the end of our constructor
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            object=self,   # Pass in our own data so the function can see the actual data we loaded
            required_data={
                'tag': "chapter",
                'content': str,
                
                'temp': str,
                'test': str,
            }
        )

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()

    
    def submit_mini_note(self, e):
        title = e.control.value
        self.create_mini_note(title)
        e.control.value = ""
        self.reload_widget()


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''


        # BUILDING BODY - the inside the body container of our widget
        self.body_container.content = ft.Column(
            expand=True,
            controls=[
                ft.Text(f"hello from: {self.title}"),
                ft.TextField(
                    label="Create Mini Note",
                    hint_text="Mini Note Title",
                    expand=True,
                    on_submit=self.submit_mini_note,
                )
            ]
        )

        self.render_widget()

        