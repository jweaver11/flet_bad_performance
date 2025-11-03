import flet as ft
from models.story import Story
import os

# Expansion tile for all sub directories (folders) in a directory
class Tree_View_Directory(ft.GestureDetector):

    def __init__(
        self, 
        directory_path: str,                        # Full path to this directory
        title: str,                                 # Title of this item
        story: Story,                               # Story reference for mouse positions
        page: ft.Page,                              # Page reference for overlay menu
        is_expanded: bool = False,                  # Whether this directory is expanded or not
        color: str = "primary",                     # Color of the folder icon
        father: 'Tree_View_Directory' = None,       # Optional parent directory tile
        additional_menu_options: list = None,       # Options to show when right clicking a directory
    ):
        
        # Reference for all our passed in data
        self.directory_path = directory_path
        self.title = title
        self.story = story
        self.p = page
        self.father = father
        self.color = color
        self.is_expanded = is_expanded  
        self.additional_menu_options = additional_menu_options

        # State tracking variables
        self.are_submitting = False
        self.item_is_unique = True

        # Set our text style
        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.ON_SURFACE,
            weight=ft.FontWeight.BOLD,
        )

        # Textfield for creating new items (sub-categories, chapters, notes, characters, etc.)
        self.new_item_textfield = ft.TextField(  
            hint_text="Sub-Category Name",          
            #data="category",                                       # Data for logic routing on submit
            #on_submit=self.new_sub_category_clicked,               # Called when enter is pressed
            autofocus=True,
            on_blur=self.on_new_item_blur,
            visible=False,
            text_style=self.text_style
        )

        # Parent constructor
        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_enter=self.on_hover,
            on_exit=self.on_stop_hover,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
        )

        # Reload our directory tile to set up initial UI
        self.reload()

    # Called when right clicking over our expansion tile
    def get_menu_options(self) -> list[ft.Control]:
        ''' Returns our built in menu options all tree view rails have, and any additional ones passed in '''

        # Declare our menu options list, and add our category option first
        menu_options = [
            ft.TextButton(
                on_click=lambda e: self.new_item_clicked(type="category"),
                expand=True,
                content=ft.Row([
                    ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED),
                    ft.Text("Sub-Category", color=ft.Colors.ON_SURFACE),
                ])
            ),
        ]

        # Run through our additional menu options if we have any, and add them
        for option in self.additional_menu_options or []:

            # Set their on_click to call our on_click method, which can handle any type of widget
            option.on_click = lambda e: self.new_item_clicked(type=option.data)
            # Add them to the list
            menu_options.append(option)

        # Add our remaining built in options: rename, color change, delete
        menu_options.extend([
            # Rename button
            ft.TextButton(
                expand=True,
                on_click=self.rename_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED),
                    ft.Text(
                        "Rename", 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.ON_SURFACE
                    ), 
                ]),
            ),

            # Color changing popup menu
            ft.PopupMenuButton(
                expand=True,
                tooltip="",
                padding=ft.Padding(10,0,0,0),
                content=ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(),   # Spacer
                        ft.Icon(ft.Icons.COLOR_LENS_OUTLINED, color=ft.Colors.PRIMARY, size=20),
                        ft.Text("Color", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True), 
                        ft.Icon(ft.Icons.ARROW_RIGHT_OUTLINED, color=ft.Colors.ON_SURFACE, size=16),
                    ]
                ),
                items=self.get_color_options()
            ),
        
            # Delete button
            ft.TextButton(
                on_click=lambda e: self.delete_clicked(e),
                expand=True,
                content=ft.Row([
                    ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED),
                    ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True),
                ]),
            ),
        ])

        # Return our menu options list
        return menu_options

    # Called when expanding/collapsing the directory
    def toggle_expand(self):
        ''' Makes sure our state and data match the updated expanded/collapsed state '''

        self.is_expanded = not self.is_expanded
        self.story.change_folder_data(
            directory_path=self.directory_path,
            key='is_expanded',
            value=self.is_expanded
        )

    # Called when creating new category or when additional menu items are clicked
    def new_item_clicked(self, type: str = "category"):
        ''' Shows the textfield for creating new item. Requires what type of item (category, chapter, note, etc.) '''

        # Clear out any previous value
        self.new_item_textfield.value = None

        # Make our textfield visible and set values
        self.new_item_textfield.visible = True
        self.new_item_textfield.data = type
        self.new_item_textfield.hint_text = f"{type.capitalize()} Name"

        # Check the type passed in by the option, and route our logic through that
        if type == "category":
            self.new_item_textfield.on_change = self.category_check
            self.new_item_textfield.on_submit = self.category_submit

        elif type == "chapter":
            self.new_item_textfield.on_change = self.chapter_check
            #self.new_item_textfield.on_submit = self.chapter_submit

        elif type == "note":
            self.new_item_textfield.on_change = self.note_check
            #self.new_item_textfield.on_submit = self.note_submit

        elif type == "character":
            self.new_item_textfield.on_change = self.character_check
            #self.new_item_textfield.on_submit = self.character_submit

        elif type == "map":
            self.new_item_textfield.on_change = self.map_check
            #self.new_item_textfield.on_submit = self.map_submit

        # Check our expanded state. Rebuild if needed
        if self.is_expanded == False:
            self.toggle_expand()
            self.reload()

        # Close the menu, which will also update the page
        self.story.close_menu()

    # Called when clicking off the textfield and after submission
    def on_new_item_blur(self, e):
        ''' Handles if we need to hide our textfield or re-focus it based on submissions '''
        
        # Check if we're submitting, or normal blur
        if self.are_submitting:

            # Change submitting to false
            self.are_submitting = False     

            # If our item is unique, hide the textfield and update
            if self.item_is_unique:
                e.control.visible = False
                e.control.value = None
                e.control.error_text = None
                self.p.update()
                return
            
            # Otherwise its not unique, re-focus our textfield
            else:
                e.control.visible = True
                e.control.focus()
        
        # If we're not submitting, just hide the textfield and reset values
        else:
            e.control.visible = False
            e.control.value = None
            e.control.error_text = None
            self.p.update()

    # Called whenever our user inputs a new key into one of our textfields for new items
    def category_check(self, e):
        ''' Checks if our title is unique within its directory (default in this case) '''

        # Start out assuming we are unique
        self.item_is_unique = True

        # Grab out title from the textfield, and set our new key to compare
        title = e.control.value

        # Generate our new key to compare. Requires normalization
        nk = self.directory_path + "\\" + self.title + title
        new_key = os.path.normcase(os.path.normpath(nk))

        # Compare all our folders that would be inside of this folder, and check for uniqueness
        for key in self.story.data['folders'].keys():
            if os.path.normcase(os.path.normpath(key)) == new_key:
                self.item_is_unique = False
                self.new_item_textfield.error_text = "Category name already exists"
                self.p.update()
                return
            
    def chapter_check(self, e):
        pass

    def note_check(self, e):
        pass

    def character_check(self, e):
        pass

    def map_check(self, e):
        pass

    def category_submit(self, e):
        pass

    def chapter_submit(self, e):
        pass

    def note_submit(self, e):
        pass

    def character_submit(self, e):
        pass

    def map_submit(self, e):
        pass



    # Called when rename button is clicked
    def rename_clicked(self, e):

        # Track if our name is unique for checks, and if we're submitting or not
        self.is_unique = True
        self.are_submitting = False

        # Grab our current name for comparison
        current_name = self.title

        # Called when clicking outside the input field to cancel renaming
        def _cancel_rename(e):
            ''' Puts our name back to static and unalterable '''

            # Grab our submitting state

            # Since this auto calls on submit, we need to check. If it is cuz of a submit, do nothing
            if self.are_submitting:
                submitting = not submitting     # Change submit status to False so we can de-select the textbox
                return
            
            # Otherwise we're not submitting (just clicking off the textbox), so we cancel the rename
            else:

                self.reload()
                self.p.update()

        # Called everytime a change in textbox occurs
        def _name_check(e):
            ''' Checks if the name is unique within its type of widget '''

            # Grab the new name, and tag
            name = e.control.value

            # Nonlocal variables

             # Set submitting to false, and unique to True
            self.are_submitting = False
            self.is_unique = True
        

            for key in self.story.data['folders'].keys():
                if key == self.directory_path + "\\" + self.title:
                    self.is_unique = False





            # Give us our error text if not unique
            if not self.is_unique:
                e.control.error_text = "Category name already exists"
            else:
                e.control.error_text = None

            # Apply the update
            self.p.update()

        # Called when submitting our textfield.
        def _submit_name(e):
            ''' Checks that we're unique and renames the widget if so. on_blur is auto called after this, so we handle that as well '''

            # Get our name and check if its unique
            name = e.control.value

            # Non local variables
            nonlocal text_field
            

            # Set submitting to True
            self.are_submitting = True

            # If it is, call the rename function. It will do everything else
            if self.is_unique:
                #self.widget.rename(name)
                print("We're unique!")
                
            # Otherwise make sure we show our error
            else:
                text_field.error_text = "Name already exists"
                text_field.focus()                                  # Auto focus the textfield
                self.p.update()
                
        # Our text field that our functions use for renaming and referencing
        text_field = ft.TextField(
            value=self.title,
            expand=True,
            dense=True,
            autofocus=True,
            adaptive=True,
            text_size=14,
            text_style=self.text_style,
            on_submit=_submit_name,
            on_change=_name_check,
            on_blur=_cancel_rename,
        )

        # Replaces our name text with a text field for renaming
        self.content.title = text_field

        # Clears our popup menu button and applies to the UI
        self.story.close_menu()

    def get_color_options(self) -> list[ft.Control]:
        ''' Returns a list of all available colors for icon changing '''

        # Called when a color option is clicked on popup menu to change icon color
        def _change_icon_color(color: str):
            ''' Passes in our kwargs to the widget, and applies the updates '''

            # Change the data
            self.story.change_folder_data(self.directory_path, 'color', color)
            self.color = color
            
            # Change our icon to match, apply the update
            self.reload()
            self.p.update()
            #self.close_menu(None)      # Auto closing menu works, but has a grey screen bug

        # List of available colors
        colors = [
            "primary",
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "pink",
            "brown",
            "grey",
        ]

        # List for our colors when formatted
        color_controls = [] 

        # Create our controls for our color options
        for color in colors:
            color_controls.append(
                ft.PopupMenuItem(
                    content=ft.Text(color.capitalize(), weight=ft.FontWeight.BOLD, color=color),
                    on_click=lambda e, col=color: _change_icon_color(col)
                )
            )

        return color_controls
    
    # Called when the delete button is clicked in the menu options
    def delete_clicked(self, e):
        ''' Deletes this file from the story '''

        def _delete_confirmed(e):
            ''' Deletes the widget after confirmation '''

            self.p.close(dlg)
            self.story.delete_folder(self.directory_path)
            self.story.close_menu()
            

        # Append an overlay to confirm the deletion
        dlg = ft.AlertDialog(
            title=ft.Text(f"Are you sure you want to delete '{self.title}' forever?", weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            title_padding=ft.padding.all(25),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.p.close(dlg)),
                ft.TextButton("Delete", on_click=_delete_confirmed, style=ft.ButtonStyle(color=ft.Colors.ERROR)),
            ]
        )

        self.p.open(dlg)


    def on_hover(self, e):
        # Need to set the directory path when dragging stuff
        self.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.RED)
        #if self.father is not None:
            #self.father.content.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()
       

    def on_stop_hover(self, e):
        self.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()

    # Called when we need to reload this directory tile
    def reload(self):
        expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=self.title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            initially_expanded=self.is_expanded,
            tile_padding=ft.Padding(0, 0, 0, 0),
            controls_padding=ft.Padding(10, 0, 0, 0),
            leading=ft.Icon(ft.Icons.FOLDER_OUTLINED, color=self.color),
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(),
            on_change=lambda e: self.toggle_expand(),
            controls=[self.new_item_textfield],
        )

        self.content = expansion_tile
        




