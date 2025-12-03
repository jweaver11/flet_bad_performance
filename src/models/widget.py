'''
An extended flet container that is the parent class of all our story objects. A widget is essentially a tab
Handles uniform UI, and has some functionality all objects need for easy data use.
Every widget has its own json file
Only Widgets create mini widgets
'''

import flet as ft
from models.story import Story
import os
import json
from handlers.verify_data import verify_data
from styles.snack_bar import Snack_Bar


class Widget(ft.Container):
    
    # Constructor. All widgets require a title,  page reference, directory path, and story reference
    def __init__(
        self, 
        title: str,             # Title of our object
        page: ft.Page,          # Grabs a page reference for updates
        directory_path: str,    # Path to our directory that will contain our json file
        story: Story,           # Reference to our story object that owns this widget
        data: dict = None       # Our data passed in if loaded (or none if new object)
    ):

        # Sets uniformity for all widgets
        super().__init__(
            expand=True, 
            #bgcolor=ft.Colors.TRANSPARENT, 
            data=data,                              # Sets our data. 
            border_radius=ft.border_radius.all(8),
            #border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            #bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.with_opacity(0.6, ft.Colors.ON_INVERSE_SURFACE),
                    ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
                    #ft.Colors.CYAN_400, ft.Colors.PURPLE_500
                ],
            ),
            margin=ft.margin.all(0),
            padding=ft.padding.all(8),
            #on_click=lambda e: print("Pressed widget")
            #TODO: Make bgcolor gradiant, slightly brighter at top
        )

    
        # Set our parameters
        self.title: str = title.capitalize()                          
        self.p: ft.Page = page                               
        self.directory_path: str = directory_path        
        self.story: Story = story                

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'key': f"{self.directory_path}\\{self.title}",  # Unique key for this widget based on directory path + title
                'title': self.title,                            # Title of our widget  
                'directory_path': self.directory_path,          # Directory path to the file this widget's data is stored in
                'tag': str,                                     # Tag to identify what type of widget this is
                'pin_location': "main" if data is None else data.get('pin_location', "main"),       # Pin location this widget is rendered in the workspace (main, left, right, top, or bottom)
                'index': int,                                   # Index of this widget in its pin location
                'visible': True,                                # Whether this widget is visible in the workspace or not
                'is_active_tab': True,                          # Whether this widget's tab is the active tab in the main pin
                'color': "primary",                             # Color of the icon on the rail and next to title on rail
                'mini_widgets_location': "right",               # Side of the widget the mini widgets show up on (left or right)
                'custom_fields': dict,                          # Dictionary for any custom fields the widget wants to store
            },
        )


        # Apply our visibility
        self.visible = self.data['visible'] 

        # Tracks variable to see if we should outline the widget where it is displayed
        self.focused = False

        # UI ELEMENTS - Tab
        self.tabs: ft.Tabs = ft.Tabs() # Tabs control to hold our tab. We only have one tab, but this is needed for it to render. Nests in self.content
        self.tab: ft.Tab = ft.Tab()  # Tab that holds our title and hide icon. Nests inside of a ft.Tabs control
        self.icon: ft.Icon = ft.Icon()
        self.tab_text: ft.Text = ft.Text()
        self.hide_tab_icon_button: ft.IconButton = ft.IconButton()    # 'X' icon button to hide widget from workspace'

        # UI ELEMENTS - Body

        # Declare our mini widgets list                      
        self.mini_widgets: list = []   

        # Currently active mini widget being focused on
        self.active_mini_widget: ft.Control = None

        # Column for displaying our mini widgets on the left, right, or both sides of our body
        self.mini_widgets_row: ft.Row = ft.Column(spacing=4)  
        
        self.body_container: ft.Container = ft.Container(expand=True)  # Stack to hold our body content, with mini widgets overlaid on top

        # Called at end of constructor for all child widgets to build their view (not here tho since we're not on page yet)
        #self.reload_widget()

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

    # Called for little data changes
    def change_data(self, **kwargs):
        ''' Changes a key/value pair in our data and saves the json file '''
        # Called by:
        # widget.change_data(**{'key': value, 'key2': value2})

        try:
            for key, value in kwargs.items():
                self.data.update({key: value})

            self.save_dict()

        # Handle errors
        except Exception as e:
            print(f"Error changing data {key}:{value} in widget {self.title}: {e}")

    def change_custom_field(self, **kwargs):
        ''' Changes a key/value pair in our custom fields dictionary and saves the json file '''
        # Called by:
        # widget.change_custom_field(**{'key': value, 'key2': value2})

        try:
            for key, value in kwargs.items():
                self.data['custom_fields'].update({key: value})

            self.save_dict()

        # Handle errors
        except Exception as e:
            print(f"Error changing custom field {key}:{value} in widget {self.title}: {e}")

    # Called when moving widget files
    def delete_file(self, old_file_path: str) -> bool:
        ''' Deletes our widget's json file from the directory '''

        try:
            # Delete the file if it exists
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            else:
                print(f"File {old_file_path} does not exist, cannot delete.")

            return True

        # Handle errors
        except Exception as e:
            print(f"Error deleting widget file at {old_file_path}: {e}")
            return False
        
    # Called when moving widget files
    def move_file(self, new_directory: str):
        ''' Moves our widget's json file to a new directory '''

        # Go through our new directory and check if any files there have the same title
        files = os.listdir(new_directory)
        for file in files:

            # Split the file name and extension
            file_name, file_ext = os.path.splitext(file)

            # Check the file name against our title
            if file_name == self.title: 

                # If we dropped where we started, just return out of the function
                if new_directory == self.directory_path:
                    return
                
                # Otherwise, open our app bar dialog to show the error
                self.p.open(
                    Snack_Bar(          
                        content=ft.Text(
                            f"Cannot move {self.title}. A file with that name already exists in the target directory.",
                            weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True
                        ),
                    )
                )

                # Remove our drag targets since we arent moving anything
                self.story.workspace.remove_drag_targets()
                
                # Return out of the function
                return


        # If we passed the check earlier, delete the old file
        self.delete_file(old_file_path=os.path.join(self.directory_path, f"{self.title}.json"))

        # Set our data to the new path where we need to
        self.data['directory_path'] = new_directory
        self.directory_path = self.data['directory_path']
        self.data['key'] = f"{new_directory}\\{self.title}"

        # Save our updated data
        self.save_dict()

        # Reload the rail to apply changes
        self.story.active_rail.content.reload_rail()        


    # Called when renaming a widget
    def rename(self, title: str):
        ''' Renames our widget in live title, data, and json file '''
        
        # Hides the widget while renaming to make sure pointers are updated as well
        self.toggle_visibility() 

        # Save our old file path for renaming later
        old_file_path = os.path.join(self.directory_path, f"{self.title}.json")   
        old_key = f"{self.directory_path}\\{self.title}"  
                                                 
        # Update our live title, and associated data
        self.title = title.capitalize()                              
        self.data['title'] = self.title     
        self.data['key'] = f"{self.directory_path}\\{self.title}"  


        # Rename our json file so it doesnt just create a new one
        os.rename(old_file_path, self.data['key'] + ".json")  

        # Save our data to this new file
        self.save_dict()                                

        # Remove from our live dict wherever we are stored
        tag = self.data['tag']

        # Delete our old live saved object, and add the new one
        if tag == "chapter":
            self.story.chapters.pop(old_key, None)
            self.story.chapters[self.data['key']] = self
        elif tag == "image":
            self.story.images.pop(old_key, None)
            self.story.images[self.data['key']] = self
        elif tag == "note":
            self.story.notes.pop(old_key, None)
            self.story.notes[self.data['key']] = self
        elif tag == "character":
            self.story.characters.pop(old_key, None)
            self.story.characters[self.data['key']] = self
        elif tag == "map":
            self.story.maps.pop(old_key, None)
            self.story.maps[self.data['key']] = self  
        elif tag == "timeline":
            self.story.timelines.pop(old_key, None)
            self.story.timelines[self.data['key']] = self


        # Re-applies visibility to what it was before rename
        self.toggle_visibility()                

        # Reload our widget ui and rail to reflect changes 
        self.reload_widget()           
        self.set_active_tab()              
        self.story.active_rail.content.reload_rail()   

    # Called on many actions to make this the active tab if in the main pin
    def set_active_tab(self):
        ''' Sets this widgets tab as the active tab in the main pin'''

        self.data['is_active_tab'] = True
        self.save_dict()

        # Deactivate all other widgets in main pin
        for widget in self.story.widgets:
            if widget != self and widget.data['pin_location'] == "main" and widget.visible:
                widget.data['is_active_tab'] = False
                widget.save_dict()

        # Reload the workspace to reflect changes
        self.story.workspace.reload_workspace()


    # Called when a new mini note is created inside a widget
    def create_comment(self, title: str):
        ''' Creates a mini note inside an image or chapter '''
        from models.mini_widgets.comment import Comment

        self.mini_widgets.append(
            Comment(
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

        self.hide_tab_icon_button.icon_color = ft.Colors.ON_SURFACE
        self.tabs.indicator_color = self.data.get('color', ft.Colors.PRIMARY)

        # Handle when we're in main pin with multiple tabs
        if self.data['pin_location'] == "main" and len(self.story.workspace.main_pin.controls) > 1 and self.data['is_active_tab']:
            self.story.workspace.main_pin_tabs.indicator_color = self.data.get('color', ft.Colors.PRIMARY)
        
        self.p.update()

    # Called when mouse stops hovering over the tab part of the widget
    def stop_hover_tab(self, e):
        ''' Reverts the color change of the hide icon button '''

        self.hide_tab_icon_button.icon_color = ft.Colors.OUTLINE
        self.tabs.indicator_color = ft.Colors.with_opacity(0.8, self.data.get('color', ft.Colors.PRIMARY))

        # Handle when we're in main pin with multiple tabs
        if self.data['pin_location'] == "main" and len(self.story.workspace.main_pin.controls) > 1 and self.data['is_active_tab']:
            self.story.workspace.main_pin_tabs.indicator_color = ft.Colors.with_opacity(0.8, self.data.get('color', ft.Colors.PRIMARY))

        self.p.update()


    # Called when app clicks the hide icon in the tab
    def toggle_visibility(self, e=None, value: bool=None):
        ''' Hides the widget from our workspace and updates the json to reflect the change '''

        # If we want to specify we're visible or not, we can pass it in
        if value is not None:
            self.data['visible'] = value
            self.visible = value
        
        else:
            # Change our visibility data, save it, then apply it
            self.data['visible'] = not self.data['visible']
            self.visible = self.data['visible']

        # Save our changes and reload the UI
        self.save_dict()
        self.reload_widget()

        # Protect first launch
        if self.story.workspace is not None:
            self.story.workspace.reload_workspace()


    # Called to set the active mini widget in this widget
    def set_active_mini_widget(self, mini_widget):
        print(f"Setting active mini widget to {mini_widget.title} in widget {self.title}")
        if self.active_mini_widget is not None:
            if self.active_mini_widget != mini_widget:
                self.active_mini_widget.toggle_visibility(value=False, not_active=True)

        self.active_mini_widget = mini_widget

        #self.reload_widget()


    def focus(self):
        self.focused = True

        for widget in self.story.widgets:
            if widget != self:
                if widget.focused:
                    widget.padding = ft.padding.all(0)
                    widget.focused = False
                    break

        self.padding = ft.padding.all(2)
        self.p.update()
        

    # Called at end of constructor
    def reload_tab(self):
        ''' Creates our tab for our widget that has the title and hide icon '''

        # Grabs our tag to determine the icon we'll use
        tag = self.data.get('tag', None)

        if tag is None:
            self.icon = ft.Icon(ft.Icons.DESCRIPTION_OUTLINED)

        elif tag == "chapter":
            self.icon = ft.Icon(ft.Icons.DESCRIPTION_OUTLINED)

        elif tag == "note":
            self.icon = ft.Icon(ft.Icons.COMMENT_OUTLINED)

        elif tag == "character":
            self.icon = ft.Icon(ft.Icons.PERSON_OUTLINE)

        elif tag == "settings":
            self.icon = ft.Icon(ft.Icons.SETTINGS_OUTLINED)
        
        elif tag == "timeline":
            self.icon = ft.Icon(ft.Icons.TIMELINE_ROUNDED)

        elif tag == "map":
            self.icon = ft.Icon(ft.Icons.MAP_OUTLINED)

        else:
            self.icon = ft.Icon(ft.Icons.FOLDER_OUTLINED)
        
        # Set the color and size
        self.icon.color = self.data.get('color', ft.Colors.PRIMARY)
        #self.icon.scale = 0.8

        self.tab_text = ft.Text(
            weight=ft.FontWeight.BOLD, # Make the text bold
            #color=ft.,   # Set our color to the tab color
            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,     # Set to a built in theme (mostly for font size)
            value=self.title,   # Set the text to our title
            
        )

        # Initialize our tabs control that will hold our tab. We only have one tab, but this is needed for it to render
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            #indicator_color = "transparent",
            indicator_color = ft.Colors.with_opacity(0.7, self.data.get('color', ft.Colors.PRIMARY)),
            divider_color=ft.Colors.TRANSPARENT,
        )

        # Our icon button that will hide the widget when clicked in the workspace
        self.hide_tab_icon_button = ft.IconButton(    # Icon to hide the tab from the workspace area
            scale=0.8,
            on_click=lambda e: self.toggle_visibility(),
            icon=ft.Icons.CLOSE_ROUNDED,
            icon_color=ft.Colors.OUTLINE,
            tooltip="Hide",
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
                    content=ft.Row([
        
                        self.icon,

                        # The text control that holds our title of the object
                        self.tab_text,

                        # Our icon button that hides the widget when clicked
                        self.hide_tab_icon_button, 
                    ])
                )
            )                    
        )


    # Called by child classes at the end of their constructor, or when they need UI update to reflect changes
    def reload_widget(self):
        ''' Children build their own content of the widget in their own reload_widget functions '''

        # TODO Have option in the mini_widget column to show on mini widgets on right vs left side of widget

        # Rebuild out tab to reflect any changes
        self.reload_tab()

        # Set the body container.content to whatever control you build in the child
        self.body_container.content = ft.Container(expand=True, content=ft.Text(f"hello from: {self.title}"))
            
        # Call Render widget to handle the rest of the heavy lifting
        self._render_widget()

    # Called when changes inside the widget require a reload to be reflected in the UI, like when adding mini widgets
    def _render_widget(self):
        ''' Takes the 'reload_widget' content and builds the full UI with mini widgets and tab around it '''

        # Set the mini widgets visibility to false so we can check later if we want to add it to the page
        #self.mini_widgets_container.visible = False
        #self.content_row.controls.clear()   # Clear our content row so we can rebuild it


        # Add the body container to our content row
        #self.content_row.controls.append(self.body_container)


        # BUILDING MINI WIDGETS - Column that holds our mini note controls on the side 1/3 of the widget
        #self.mini_widgets_column.controls = self.mini_widgets   
        
        # Add our column that we build to our mini widgets container
        #self.mini_widgets_container.content = self.mini_widgets_column

        # Check if we are showing any mini widgets. If we are, add the container to our content row
        #for mini_widget in self.mini_widgets_column.controls:
            # TODO: Add check for right or left side mini widgets. Either insert at controls[0] or append
            #if mini_widget.visible:
                #self.mini_widgets_container.visible = True
                #self.content_row.controls.append(self.mini_widgets_container)
                #break


        # Overlay mini widget stuf on top of body container
        # Using ratio starting with 10, render mini widgets on right or left side depending on setting
        # Keep our mini widgets using the mini widgets list

        # Set ratio for our body container and mini widgets
        self.body_container.expand = 6
        #self.body_container.padding = ft.padding.only(left=6, right=6, top=0, bottom=6)
        self.body_container.border_radius = ft.border_radius.all(8)


        

        # Put our mini widgets on the right side
        row = ft.Row(expand=True, spacing=0, controls=[self.body_container])
        

        # Add our mini widget if we have one active
        if self.active_mini_widget is not None:
            #self.active_mini_widget.expand = 4
            row.controls.append(self.active_mini_widget)
            
        
        # BUILD OUR TAB CONTENT - Our tab content holds the row of our body and mini widgets containers
        self.tab.content = row  # We add this in combo with our 'tabs' later
        
        # Add our tab to our tabs control so it will render. Set our widgets content to our tabs control and update the page
        self.tabs.tabs = [self.tab]

        outer_container = ft.Container(
            expand=True,
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.only(top=0, bottom=6, left=6, right=6),
            gradient=ft.LinearGradient(
                colors=[
                    
                    ft.Colors.ON_INVERSE_SURFACE,
                    ft.Colors.SURFACE
                ]
            ),
            content=self.tabs
        )

        # For adding focus outline
        hover_gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            
            on_tap_down=lambda e: self.focus(),
            #on_exit=self.stop_hover_tab,
            content=outer_container
        )

        self.content = self.tabs

        #self.content = row
        self.p.update()