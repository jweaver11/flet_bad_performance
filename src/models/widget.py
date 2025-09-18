'''
An extended flet container that is the parent class of all our story objects.
Handles uniform UI, and has some functionality all objects need for easy data use.
All objects contain a title, tag, page reference, pin location, tab color, and a file path
'''

import flet as ft
#from handlers.reload_workspace import reload_workspace
from models.story import Story
#from handlers.reload_workspace import show_pin_drag_targets


class Widget(ft.Container):
    # Constructor
    def __init__(self, title: str, tag: str, p: ft.Page, directory_path: str, story: Story):

        # set uniformity for all widgets
        super().__init__(
            expand=True, 
            bgcolor=ft.Colors.TRANSPARENT,  # Makes it invisible
        )
    
        # Required parameters: title, tag, page reference, pin location
        self.title = title  # Title of our object
        self.tag = tag  # Tag for logic routing and identification
        self.p = p   # Grabs a page reference for updates (page.update breaks when widget is removed then re-added to the page)
        self.directory_path = directory_path
        self.story = story
        


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
            content=ft.Container(), 

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

    # Called when a draggable starts dragging.
    def start_drag(self, e: ft.DragStartEvent):
        ''' Shows our pin drag targets '''

        # For now, settings don't drag and give the exception error instead
        try:
            self.story.workspace.show_pin_drag_targets()
        except Exception as e:
            print(f"Error showing pin drag targets: {e}")


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
            for key, story in app.stories.items():
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
            for key, story in app.stories.items():
                story.workspace.reload_workspace(self.p, story)
        else:
            story.workspace.reload_workspace(self.p, story)