'''
An extended flet container that is the parent class of all our story objects.
Handles uniform UI, and has some functionality all objects need for easy data use.
All objects contain a title, tag, page reference, pin location, tab color, and a file path
'''

import flet as ft
from models.story import Story
import os
import json


class Widget(ft.Container):
    # Constructor
    def __init__(self, title: str, tag: str, p: ft.Page, directory_path: str, story: Story, data: dict = None):

        # set uniformity for all widgets
        super().__init__(
            expand=True, 
            bgcolor=ft.Colors.TRANSPARENT,  # Makes it invisible
        )
    
        # Required parameters: title, tag, page reference, pin location, story
        self.title = title  # Title of our object
        self.tag = tag  # Tag for logic routing and identification
        self.p = p   # Grabs a page reference for updates (page.update breaks when widget is removed then re-added to the page)
        self.directory_path = directory_path    # Path to our directory that will contain our json file
        self.story = story  # Reference to our story object that owns this widget
        self.data = data    # Pass in data if loading an object, otherwise can be left blank for new objects

        # If this is a new widget (Not loaded), give it default data all widgets need
        if self.data is None:
            self.create_default_data()  # Create default data if none was passed in
            self.save_dict()    # Save our data to the file if the object is new

        # Declare our mini widgets dictionary
        self.mini_widgets = {}

        # Apply our visibility
        self.visible = self.data['visible'] 

        # Load any mini widgets this object may have
        self.load_mini_widgets()

        # Declaring UI elements that widgets will have
        self.hide_tab_icon: ft.IconButton = ft.IconButton()  # Icon button that hides the widget from the workspace
        self.tab_color: ft.Colors = ft.Colors("primary")  # Color of the tab text and divider
        self.tab: ft.Tab = ft.Tab()  # Tab that holds our title and hide icon
        self.stack: ft.Stack = ft.Stack()  # Stack that holds our content for our widget, and allows us to add our mini notes overtop

        # Gives our objects their uniform tabs.
        self.create_tab(story)  # Tabs that don't need too be reloaded for color changes are only built here

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

        # If no data exists, this declares it as an empty dictionary to catch errors
        if self.data is None:
            self.data = {}

        # Give all widgets their default data
        default_data = {
            'title': self.title,
            'directory_path': self.directory_path,
            'tag': self.tag,
            'pin_location': "main",  
            'visible': True,    
            'mini_widgets': {},
        }

        # Update existing data with any new default fields we added
        self.data.update(default_data)
        return
    
    # Called in a childs constructor to load any mini widgets that it may have
    def load_mini_widgets(self):
        ''' Checks all the items under the data['mini_widgets'] dictionary and creates the appropriate mini widget objects '''

        from models.mini_widgets.mini_note import MiniNote
        #from models.mini_widgets.plotline import arcs...

        # Make sure we have the mini widgets key
        if 'mini_widgets' not in self.data:
            self.create_default_data()

        for key, mini_widget in self.data['mini_widgets'].items():
            # Check the tag to see what type of mini widget it is, and create the appropriate object
            if mini_widget['tag'] == "mini_note":
                self.mini_widgets[key] = MiniNote(title=key, parent=self, page=self.p, data=mini_widget)


    # Called when a draggable starts dragging.
    def start_drag(self, e: ft.DragStartEvent):
        ''' Shows our pin drag targets '''
        
        self.story.workspace.show_pin_drag_targets()
        
    # Called when mouse hovers over the tab part of the widget
    def hover_tab(self, e):
        ''' Changes the hide icon button color slightly for more interactivity '''

        self.hide_tab_icon.icon_color = ft.Colors.ON_PRIMARY_CONTAINER
        self.p.update()

    # Called when mouse stops hovering over the tab part of the widget
    def stop_hover_tab(self, e):
        ''' Reverts the color change of the hide icon button '''

        self.hide_tab_icon.icon_color = ft.Colors.OUTLINE
        self.p.update()

    # Called when app clicks the hide icon in the tab
    def hide_widget(self, story: Story):
        ''' Hides the widget from our workspace and updates the json to reflect the change '''

        print(f"Hiding widget {self.title}")
        # Set our container object to invisible - won't be rendered anywhere
        self.visible = False

        # Update the child object's data and save to file
        if hasattr(self, 'data'):
            self.data['visible'] = False
            self.save_dict()
            
        # Settings doesn't have a story, so we reload all the stories workspaces instead of just the one for our widget
        if self.title == "Settings":
            from models.app import app
            for story in app.stories.values():
                story.workspace.reload_workspace(self.p, story)

        # Otherwise, our widget will have a story, so we just reload that one
        else:
            story.workspace.reload_workspace(self.p, story)

    # Called when app clicks the widget in the rail
    def show_widget(self, story: Story):
        ''' Makes our widget visible for our workspace and updates the json to reflect the change '''

        #print(f"Showing widget {self.title}")
        self.visible = True
        
        if hasattr(self, 'data'):
            self.data['visible'] = True
            self.save_dict()
        
        # Catch errors when no story loaded for settings widget
        if self.title == "Settings":
            from models.app import app
            for story in app.stories.values():
                story.workspace.reload_workspace(self.p, story)
        else:
            story.workspace.reload_workspace(self.p, story)

    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''

        from models.mini_widget import MiniNote

        # Create our mini note object
        mini_note = MiniNote(
            title=title,
            page=self.p,
            story=self.story,
        )

        # Add to our notes dictionary for access later
        self.mini_notes[title] = mini_note

        # Add to our UI
        #self.content.controls.append(mini_note)
        self.p.update()

        return mini_note

    # Called at end of constructor
    def create_tab(self, story: Story):
        ''' Creates our tab for our widget that has the title and hide icon '''

        # Our icon button that will hide the widget when clicked in the workspace
        self.hide_tab_icon = ft.IconButton(    # Icon to hide the tab from the workspace area
            scale=0.8,
            on_click=lambda e: self.hide_widget(story),
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=ft.Colors.OUTLINE,
        )

        self.tab_color =  ft.Colors.PRIMARY  # The color of the title in our tab and the divider under it

        # Tab that holds our widget title and 'body'.
        # Since this is a ft.Tab, it needs to be nested in a ft.Tabs control or it wont render.
        # We do this so we can use tabs in the main pin area, but still show as a container in other pin areas
        self.tab = ft.Tab(

            # Initialize the content. This will be our content of the body of the widget
            content=ft.Stack(), 

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
                                color=self.tab_color,   # Set our color to the tab color
                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,     # Set to a built in theme (mostly for font size)
                                value=self.title,   # Set the text to our title
                                
                            ),

                            # Our icon button that hides the widget when clicked
                            self.hide_tab_icon, 
                        ]
                    )
                ),
            ),                       
        )