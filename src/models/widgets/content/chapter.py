import flet as ft
from models.story import Story
from models.widget import Widget


# Class that holds our text chapter objects
class Chapter(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):

        # Check if we're loading a chapter or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # This gets initialized at the end of our constructor
        )

        # If our character is new and not loaded, give it default data
        if not loaded:
            self.create_default_chapter_data()  # Create data defaults for each chapter widget
            self.save_dict()    # Save our data to the file

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()


    # Called when creating new chapter widget, not when loading one
    def create_default_chapter_data(self) -> dict:
        ''' Returns default data all chapter widgets will have '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}
        
        # Default data for new chapters
        default_chapter_data = {
            'tag': "chapter",
            'visible': True,    # If this chapter is visible in the UI or not

            'content': "",    # Content of our chapter
        }

        # Update existing data with any new default fields we added
        self.data.update(default_chapter_data)  
        return
        
    
    def submit_mini_note(self, e):
        title = e.control.value
        self.create_mini_note(title)
        e.control.value = ""
        self.reload_widget()


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # Set the mini widgets visibility to false so we can check later if we want to add it to the page
        self.mini_widgets_container.visible = False
        self.content_row.controls.clear()   # Clear our content row so we can rebuild it

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

        # Add the body container to our content row
        self.content_row.controls.append(self.body_container)


        # BUILDING MINI WIDGETS - Column that holds our mini note controls on the side 1/3 of the widget
        self.mini_widgets_column.controls = self.mini_widgets   
        
        # Add our column that we build to our mini widgets container
        self.mini_widgets_container.content = self.mini_widgets_column

        # Check if we are showing any mini widgets. If we are, add the container to our content row
        for mini_widget in self.mini_widgets_column.controls:
            # TODO: Add check for right or left side mini widgets. Either insert at controls[0] or append
            if mini_widget.visible:
                self.mini_widgets_container.visible = True
                self.content_row.controls.append(self.mini_widgets_container)
                break
            
        
        # BUILD OUR TAB CONTENT - Our tab content holds the row of our body and mini widgets containers
        self.tab.content = self.content_row  # We add this in combo with our 'tabs' later
        
        # Add our tab to our tabs control so it will render. Set our widgets content to our tabs control and update the page
        self.tabs.tabs = [self.tab]
        self.content = self.tabs
        self.p.update()

        