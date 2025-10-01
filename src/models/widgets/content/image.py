import flet as ft
from models.widget import Widget
from models.story import Story


# Our widget class that displays images
class Image(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "image",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in
            self.save_dict()

        self.visible = self.data['visible']  # If we will show this widget or not


        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


    def create_default_data(self) -> dict:
        return {}
        

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

        self.p.update()



# Display our drawings in the rail
# drawings = {}
    # - editable = bool
    # - filters (whitewash, greyscale, invert, etc.)