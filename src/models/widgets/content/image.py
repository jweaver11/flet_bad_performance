import flet as ft
from models.widget import Widget
from models.story import Story
from handlers.verify_data import verify_data


# Our widget class that displays images
class Image(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            page = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "image",
                'summary': str,     # Summary of what will happen in the chapter
            }
        )
            

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()
        

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

        self._render_widget()



# Display our drawings in the rail
# drawings = {}
    # - editable = bool
    # - filters (whitewash, greyscale, invert, etc.)