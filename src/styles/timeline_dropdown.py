'''
Extended flet controls that implement the same styling for easy access
'''

import flet as ft
from styles.menu_option_style import Menu_Option_Style
from models.story import Story

# Expansion tiles used for the dropdowns of arcs, plotpoints, timeskips, and even timelines (if there are multiple)
class Timeline_Expansion_Tile(ft.GestureDetector):

    # Constructor
    def __init__(
        self, 
        #full_path: str,                                    # Full path to this directory
        title: str,                                             # Title of this folder
        story: Story,                                           # Story reference for mouse positions and other logic
        #is_expanded: bool = False,                              # Whether this directory is expanded or not
        #color: str = "primary",                                 # Color of the folder icon
        #father: 'Tree_View_Directory' = None,                   # Optional parent directory tile, if there is one
        additional_menu_options: list[ft.Control] = None,       # Additional menu options when right clicking a category, depending on the rail
    ):

        # Set our parameters
        self.title = title.capitalize()
        self.story = story
        self.additional_menu_options = additional_menu_options
        self.color = ft.Colors.PRIMARY
        
        # Set our text style
        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.ON_SURFACE,
            weight=ft.FontWeight.BOLD,
        )
        
        # Textfield for creating new items (sub-categories, chapters, notes, characters, etc.)
        self.new_item_textfield = ft.TextField(  
            hint_text="Sub-Arc Name",          
            #data="arc",                                       # Data for logic routing on submit
            #on_submit=self.new_sub_category_clicked,               # Called when enter is pressed
            autofocus=True,
            on_blur=self.on_new_item_blur,
            visible=False,
            text_style=self.text_style
        )
        
        # Parent constructor
        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
            #on_enter=self.on_hover,
            #on_exit=self.on_stop_hover,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
        )

        self.reload()

    def get_menu_options(self) -> list[ft.Control]:

        # Declare our menu options list, and add our category option first
        menu_options = [
            Menu_Option_Style(
                #on_click=self.new_category_clicked,
                data="arc",
                content=ft.Row([
                    ft.Icon(ft.Icons.ALARM_ADD_OUTLINED),
                    ft.Text("Arc", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                #on_click=self.new_character_clicked,
                data="plot_point",
                content=ft.Row([
                    ft.Icon(ft.Icons.EXPAND_CIRCLE_DOWN_OUTLINED),
                    ft.Text("Plot Point", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                #on_click=self.new_character_clicked,
                data="time_skip",
                content=ft.Row([
                    ft.Icon(ft.Icons.FAST_FORWARD_OUTLINED),
                    ft.Text("Time skip", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
        ]

        # Run through our additional menu options if we have any, and set their on_click methods
        for option in self.additional_menu_options or []:

            # Set their on_click to call our on_click method, which can handle any type of widget
            option.on_tap = lambda e, t=option.data: self.new_item_clicked(type=t)

            # Add them to the list
            menu_options.append(option)

        # Add our remaining built in options: rename, color change, delete
        menu_options.extend([
            # Rename button
            Menu_Option_Style(
                #on_click=self.rename_clicked,
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
            Menu_Option_Style(
                content=ft.PopupMenuButton(
                    expand=True,
                    tooltip="",
                    padding=None,
                    content=ft.Row(
                        expand=True,
                        controls=[
                            ft.Icon(ft.Icons.COLOR_LENS_OUTLINED, color=ft.Colors.PRIMARY),
                            ft.Text("Color", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True), 
                            ft.Icon(ft.Icons.ARROW_DROP_DOWN_OUTLINED, color=ft.Colors.ON_SURFACE, size=16),
                        ]
                    ),
                    items=self.get_color_options()
                )
            ),
        
            # Delete button
            Menu_Option_Style(
                #on_click=lambda e: self.delete_clicked(e),
                content=ft.Row([
                    ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED),
                    ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True),
                ]),
            ),
        ])

        # Return our menu options list
        return menu_options

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
        if type == "plot_point":
            self.new_item_textfield.on_change = self.category_check
            self.new_item_textfield.on_submit = self.category_submit

        elif type == "time_skip":
            self.new_item_textfield.on_change = self.chapter_check
            self.new_item_textfield.on_submit = self.chapter_submit

        elif type == "arc":
            self.new_item_textfield.on_change = self.note_check
            self.new_item_textfield.on_submit = self.note_submit

        # Check our expanded state. Rebuild if needed
        if self.is_expanded == False:
            #self.toggle_expand()
            self.reload()

        # Close the menu, which will also update the page
        #self.story.close_menu()

    def get_color_options(self) -> list[ft.Control]:
        ''' Returns a list of all available colors for icon changing '''

        # Called when a color option is clicked on popup menu to change icon color
        def _change_icon_color(color: str):
            ''' Passes in our kwargs to the widget, and applies the updates '''

            # Change the data
            self.story.change_folder_data(self.full_path, 'color', color)
            self.color = color
            
            # Change our icon to match, apply the update
            self.story.active_rail.content.reload_rail()
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


    # Called when we need to reload this directory tile
    def reload(self):
        expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=self.title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            #initially_expanded=self.is_expanded,
            tile_padding=ft.Padding(0, 0, 0, 0),
            controls_padding=ft.Padding(10, 0, 0, 0),       # Keeps all sub children indented
            leading=ft.Icon(ft.Icons.TIMELINE_ROUNDED, color=self.color),
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            adaptive=True,
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(),
            #on_change=lambda e: self.toggle_expand(),
            controls=[self.new_item_textfield], 
        )

        # Re-adds our content controls so we can keep states
        if self.content is not None:        # Protects against first loads
            if self.content.content.controls is not None:
                for control in self.content.content.controls:
                    if control != self.new_item_textfield:      # Don't re-add our textfield, its already there
                        expansion_tile.controls.append(control)

        
        # Set the content
        self.content = expansion_tile



