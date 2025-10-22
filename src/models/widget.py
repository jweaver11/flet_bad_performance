'''
An extended flet container that is the parent class of all our story objects.
Handles uniform UI, and has some functionality all objects need for easy data use.
Every widget has its own json file
Only Widgets create mini widgets
'''

import flet as ft
from models.story import Story
import os
import json
from handlers.verify_data import verify_data

# TODO Show widget outline when clicked on rail as a pseudo 'focus'
# TODO Have option in the mini_widget column to show on mini widgets on right vs left side of widget

class Widget(ft.Container):
    
    # Constructor. All widgets require a title,  page reference, directory path, and story reference
    def __init__(self, title: str, p: ft.Page, directory_path: str, story: Story, data: dict=None):

        # set uniformity for all widgets
        super().__init__(
            expand=True, 
            bgcolor=ft.Colors.TRANSPARENT,  # Makes it invisible
            data=data,  # Sets our data. NOTE. If data is None, you need to set to {} later
        )
    
        # Required properties of all widgets
        self.title = title  # Title of our object
        self.p = p   # Grabs a page reference for updates (page.update breaks when widget is removed then re-added to the page)
        self.directory_path = directory_path    # Path to our directory that will contain our json file
        self.story = story  # Reference to our story object that owns this widget
        self.mini_widgets = []  # List that holds our mini widgets objects

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'title': self.title,                        # Title of our widget  
                'directory_path': self.directory_path,      # Directory path to the file this widget's data is stored in
                'tag': str,                                 # Tag to identify what type of widget this is
                'pin_location': "main",                     # Pin location this widget is rendered in the workspace (main, left, right, top, or bottom)
                'visible': True,                            # Whether this widget is visible in the workspace or not
                'tab_title_color': "primary",               # Color of the title in the tab (primary, secondary, blue, red, etc.)
            },
        )


        # Apply our visibility
        self.visible = self.data['visible'] 

        # UI ELEMENTS - Tab
        self.tabs = ft.Tabs()   # Tabs control to hold our tab. We only have one tab, but this is needed for it to render. Nests in self.content
        self.tab = ft.Tab()  # Tab that holds our title and hide icon. Nests inside of a ft.Tabs control
        self.hide_tab_icon_button = ft.IconButton()    # 'X' icon button to hide widget from workspace'

        # UI ELEMENTS - Body
        self.mini_widgets_column = ft.Column(spacing=4)  # Column for our mini widgets on the side of our main content. Nests inside of self.mini_widgets_container
        self.mini_widgets_container = ft.Container(expand=1)  # Control to display our mini widgets. Nests inside of self.content_row
        self.body_container = ft.Container(expand=2)  # Control to diplay our body content. Nests inside of self.content_row
        self.content_row = ft.Row(spacing=2, expand=True)   # Row for our body and mini widgets containers. Nests inside of self.tab.content

        # Gives our objects their uniform tabs.
        self.reload_tab()  # Tabs that don't need too be reloaded for color changes are only built here

    # Called whenever there are changes in our data
    def save_dict(self):
        ''' Saves our current data to the json file '''

        try:

            # Set our file path
            file_path = os.path.join(self.directory_path, f"{self.title}.json")

            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:   
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving widget to {file_path}: {e}") 
            print("Data that failed to save: ", self.data)


    # Called when a new mini note is created inside a widget
    def create_mini_note(self, title: str):
        ''' Creates a mini note inside an image or chapter '''
        from models.mini_widgets.mini_note import MiniNote

        self.mini_widgets.append(
            MiniNote(
                title=title, 
                owner=self, 
                father=self,
                page=self.p, 
                dictionary_path="mini_notes",
                data=None
            )
        )

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
    def toggle_visibility(self):
        ''' Hides the widget from our workspace and updates the json to reflect the change '''

        # Set our container object to invisible - won't be rendered anywhere
        self.data['visible'] = not self.data['visible']
        self.visible = self.data['visible']
        self.save_dict()
        self.p.update()

        self.story.workspace.reload_workspace(self.p, self.story)

    # Called at end of constructor
    def reload_tab(self):
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
            on_click=lambda e: self.toggle_visibility(),
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
                                color=self.data['tab_title_color'],   # Set our color to the tab color
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

    # Called by child classes at the end of their constructor, or when they need UI update to reflect changes
    def reload_widget(self):
        ''' Children build their own content of the widget in their own reload_widget functions '''

        # Set the body container.content to whatever control you build in the child
        self.body_container.content = ft.Text(f"hello from: {self.title}")
            
        # Call Render widget to handle the rest of the heavy lifting
        self._render_widget()

    # Called when changes inside the widget require a reload to be reflected in the UI, like when adding mini widgets
    def _render_widget(self):
        ''' Takes the 'reload_widget' content and builds the full UI with mini widgets and tab around it '''

        # Set the mini widgets visibility to false so we can check later if we want to add it to the page
        self.mini_widgets_container.visible = False
        self.content_row.controls.clear()   # Clear our content row so we can rebuild it


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