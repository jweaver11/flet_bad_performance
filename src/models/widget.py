'''
An extended flet container that is the parent class of all our story objects.
Handles uniform UI, and has some functionality all objects need for easy data use.
'''

import flet as ft
from models.story import Story
import os
import json

# TODO Show widget outline when clicked on rail as a pseudo 'focus'
# TODO Have option in the mini_widget column to show on mini widgets on right vs left side of widget

class Widget(ft.Container):
    # Constructor. All widgets require a title,  page reference, directory path, and story reference
    def __init__(self, title: str, p: ft.Page, directory_path: str, story: Story, data: dict=None):

        # set uniformity for all widgets
        super().__init__(
            expand=True, 
            bgcolor=ft.Colors.TRANSPARENT,  # Makes it invisible
        )
    
        # Required properties of all widgets
        self.title = title  # Title of our object
        self.p = p   # Grabs a page reference for updates (page.update breaks when widget is removed then re-added to the page)
        self.directory_path = directory_path    # Path to our directory that will contain our json file
        self.story = story  # Reference to our story object that owns this widget
        self.data = data    # Pass in data if loading an object, otherwise can be left blank for new objects
        self.mini_widgets = []  # List that holds our mini widgets objects

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
            self.verify_widget_data()

        # Apply our visibility
        self.visible = self.data['visible'] 

        # UI ELEMENTS - Tab
        self.tabs = ft.Tabs()   # Tabs control to hold our tab. We only have one tab, but this is needed for it to render. Nests in self.content
        self.tab = ft.Tab()  # Tab that holds our title and hide icon. Nests inside of a ft.Tabs control
        self.tab_title_color: ft.Colors.PRIMARY = "primary"     # The color of the title in our tab and the divider under it
        self.hide_tab_icon_button = ft.IconButton()    # 'X' icon button to hide widget from workspace'

        # UI ELEMENTS - Body
        self.content_row = ft.Row(spacing=2, expand=True)   # Row for our body and mini widgets containers. Nests inside of self.tab.content
        self.body_container = ft.Container(expand=2)  # Control to diplay our body content. Nests inside of self.content_row
        self.mini_widgets_container = ft.Container(expand=1)  # Control to display our mini widgets. Nests inside of self.content_row
        self.mini_widgets_column = ft.Column(spacing=4)  # Column for our mini widgets on the side of our main content. Nests inside of self.mini_widgets_container

        # Load any mini widgets this object may have
        self.load_mini_widgets()

        # Gives our objects their uniform tabs.
        self.reload_tab(story)  # Tabs that don't need too be reloaded for color changes are only built here

    # Called whenever there are changes in our data
    def save_dict(self):
        ''' Saves our current data to the json file '''

        # Print(f"Saving object data to {self.data['file_path']}")
        file_path = os.path.join(self.directory_path, f"{self.title}.json")

        try:
            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:   
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving object to {file_path}: {e}")

    # Called when creating a new widget, not when loading one
    def create_default_data(self) -> dict:
        ''' Returns required data all widgets must have '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # Give all widgets their default data
        default_data = {
            'title': self.title,
            'directory_path': self.directory_path,
            'tag': "widget",    # Default tag, should be overwritten by child classes
            'pin_location': "main",     # Stick us in the main pin area by default
            'visible': True,    
            'tab_title_color': "primary",
            'mini_widgets': {},
        }

        # Update our data dict with any missing fields from the defaults
        self.data.update(default_data)  # Overwrite any missing or duplicate fields (should be no duplicates anyway)
        self.save_dict()
        return
    
    # Called to fix any missing data fields in loaded widgets. Only fixes our missing fields above
    def verify_widget_data(self):
        ''' Verify loaded any missing data fields in existing widgets '''

        # Required data for all widgets and their types
        required_data_types = {
            'title': str,
            'directory_path': str,
            'tag': str,
            'pin_location': str,
            'visible': bool,
            'tab_title_color': str,
            'mini_widgets': dict,
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'title': self.title,
            'directory_path': self.directory_path,
            'tag': "widget",    # Default tag, should be overwritten by child classes
            'pin_location': "main",     # Stick us in the main pin area by default
            'visible': True,    
            'tab_title_color': "primary",
            'mini_widgets': {},
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        # Save our updated data
        self.save_dict()
        return
    
    # Called in a childs constructor to load any mini widgets that it may have
    def load_mini_widgets(self):
        ''' Checks all the items under the data['mini_widgets'] dictionary and creates the appropriate mini widget objects '''

        from models.mini_widgets.mini_note import MiniNote

        # Error handling
        if 'mini_widgets' not in self.data:
            self.create_default_data()

        # Loop through our mini widgets items in the dict and load them based on their tag into our mini widgets list
        # NOTE: Plotlines store data in their timelines files, so they load mini widgets in their own model file.
        for key, mini_widget in self.data['mini_widgets'].items():

            # Check the tag to see what type of mini widget it is, and create the appropriate object
            if mini_widget['tag'] == "mini_note":
                #self.mini_widgets[key] = MiniNote(title=key, owner=self, page=self.p, data=mini_widget)
                self.mini_widgets.append(MiniNote(title=key, owner=self, page=self.p, data=mini_widget))

    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''

        from models.mini_widgets.mini_note import MiniNote

        #self.mini_widgets[title] = MiniNote(title=title, owner=self, page=self.p, data=None)
        self.mini_widgets.append(MiniNote(title=title, owner=self, page=self.p, data=None))

        self.reload_widget()


    # Called when a draggable starts dragging.
    def start_drag(self, e: ft.DragStartEvent):
        ''' Shows our pin drag targets '''
        
        self.story.workspace.show_pin_drag_targets()
        
    # Called when mouse hovers over the tab part of the widget
    def hover_tab(self, e):
        ''' Changes the hide icon button color slightly for more interactivity '''

        self.hide_tab_icon_button.icon_color = ft.Colors.ON_PRIMARY_CONTAINER
        self.p.update()

    # Called when mouse stops hovering over the tab part of the widget
    def stop_hover_tab(self, e):
        ''' Reverts the color change of the hide icon button '''

        self.hide_tab_icon_button.icon_color = ft.Colors.OUTLINE
        self.p.update()

    # Called when app clicks the hide icon in the tab
    def toggle_visibility(self, story: Story):
        ''' Hides the widget from our workspace and updates the json to reflect the change '''

        # Set our container object to invisible - won't be rendered anywhere
        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        self.save_dict()
        self.p.update()
            
        # Settings doesn't have a story, so we reload all the stories workspaces instead of just the one for our widget
        if self.title == "Settings":
            from models.app import app
            for story in app.stories.values():
                story.workspace.reload_workspace(self.p, story)

        # Otherwise, our widget will have a story, so we just reload that one
        else:
            story.workspace.reload_workspace(self.p, story)

    # Called when creating a new mini note inside a widget
    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''

        from models.mini_widgets.mini_note import MiniNote

        self.mini_widgets.append(MiniNote(title=title, owner=self, page=self.p, data=None))

        return

    # Called at end of constructor
    def reload_tab(self, story: Story):
        ''' Creates our tab for our widget that has the title and hide icon '''

        # Initialize our tabs control that will hold our tab. We only have one tab, but this is needed for it to render
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
        )

        # Our icon button that will hide the widget when clicked in the workspace
        self.hide_tab_icon_button = ft.IconButton(    # Icon to hide the tab from the workspace area
            scale=0.8,
            on_click=lambda e: self.toggle_visibility(story),
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=ft.Colors.OUTLINE,
        )

        self.tab_title_color = ft.Colors.PRIMARY  # The color of the title in our tab and the divider under it

        # Tab that holds our widget title and 'body'.
        # Since this is a ft.Tab, it needs to be nested in a ft.Tabs control or it wont render.
        # We do this so we can use tabs in the main pin area, but still show as a container in other pin areas
        self.tab = ft.Tab(

            # Initialize the content. This will be our content of the body of the widget
            #content=ft.Stack(), 

            # Content of the tab itself. Has widgets name and hide widget icon, and functionality for dragging
            tab_content=ft.Draggable(   # Draggable is the control so we can drag and drop to different pin locations
                group="widgets",    # Group for draggables (and receiving drag targets) to accept each other
                data=self,  # Pass ourself through the data (of our tab, NOT our object) so we can move ourself around

                # Drag event handlers
                on_drag_start=self.start_drag,    # Shows our pin targets when we start dragging
                #on_drag_complete = Do nothing. The accepted drag targets handle logic and removing pin drag targets
                #on_drag_cancel=lambda e: story.workspace.remove_drag_targets,

                # Content when we are dragging the follows the mouse
                content_feedback=ft.TextButton(self.title), # Normal text won't restrict its own size, so we use a button

                # The content of our draggable. We use a gesture detector so we have more events
                content=ft.GestureDetector(

                    # Change mouse cursor to the selector cursor when hovering over the tab
                    mouse_cursor=ft.MouseCursor.CLICK,

                    # Event handlers for hovering and stop hovering over tab
                    on_hover=self.hover_tab,
                    on_exit=self.stop_hover_tab,

                    # Content of the gesture detector. This has our actual title and hide icon
                    content=ft.Row(

                        # The controls of the row that are now left to right
                        controls=[
                            # A container for padding. We do this because we can still drag this type of padding
                            ft.Container(width=6),

                            # The text control that holds our title of the object
                            ft.Text(
                                weight=ft.FontWeight.BOLD, # Make the text bold
                                color=self.tab_title_color,   # Set our color to the tab color
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,     # Set to a built in theme (mostly for font size)
                                value=self.title,   # Set the text to our title
                                
                            ),

                            # Our icon button that hides the widget when clicked
                            self.hide_tab_icon_button, 
                        ]
                    )
                ),
            ),                       
        )