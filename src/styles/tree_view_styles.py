import flet as ft
from models.story import Story
from models.widget import Widget

# Expansion tile for all sub directories (folders) in a directory
class Tree_View_Directory(ft.GestureDetector):

    def __init__(
        self, 
        directory_path: str,            # Full path to this directory
        title: str,                     # Title of this item
        story: Story,                   # Story reference for mouse positions
        page: ft.Page,                  # Page reference for overlay menu
        is_expanded: bool = False,      # Whether this directory is expanded or not
        color: str = "primary",
        father: 'Tree_View_Directory' = None,

        # Optinos passed in by child classes
        buttons: list = None,           # Buttons to attach to the right side of the tile
        menu_options: list = None,      # Options to show when right clicking a directory
    ):
        
        self.directory_path = directory_path
        self.title = title
        self.story = story
        self.p = page
        self.father = father
        self.color = color
        self.is_expanded = is_expanded  

        #print(f"Color inside of tree view directory {title}:", color)

        folder_options = [
            ft.TextButton(content=ft.Text("Option 1", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
            ft.TextButton(content=ft.Text("Option 2", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
            ft.TextButton(content=ft.Text("Option 3", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ]


        self.expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            initially_expanded=is_expanded,
            tile_padding=ft.Padding(0, 0, 0, 0),
            controls_padding=ft.Padding(10, 0, 0, 0),
            leading=ft.Icon(ft.Icons.FOLDER_OPEN, color=color),
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(),
            on_change=lambda e: self.toggle_expand()
        )

        super().__init__(
            mouse_cursor=ft.MouseCursor.CLICK,
            #on_enter=self.on_hover,
            on_exit=self.on_stop_hover,
            content = self.expansion_tile,
        )

    def toggle_expand(self):
        self.is_expanded = not self.is_expanded
        self.story.change_folder_data(
            directory_path=self.directory_path,
            key='is_expanded',
            value=self.is_expanded
        )


    def on_hover(self, e):
        self.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.WHITE)
        if self.father is not None:
            self.father.content.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()
       

    def on_stop_hover(self, e):
        self.bgcolor = ft.Colors.TRANSPARENT
        self.p.update()
        


# Class for items within a tree view on the rail
class Tree_View_File(ft.GestureDetector):

    def __init__(
        self, 
        widget: Widget, 
        menu_options: list = None
    ):
        
        # Set our widget reference and tag
        self.widget = widget
        self.menu_options = menu_options

        tag = widget.data.get('tag', None)

        self.capital_title = widget.title.capitalize()

        if tag is None:
            self.icon = ft.Icons.DESCRIPTION_OUTLINED

        elif tag == "note":
            self.icon = ft.Icons.STICKY_NOTE_2_OUTLINED

        elif tag == "chapter":
            self.icon = ft.Icons.BOOK_OUTLINED

        else:
            self.icon = ft.Icons.DESCRIPTION_OUTLINED

        # Set our text style
        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.PRIMARY,
            #font_family="Consolas",
            weight=ft.FontWeight.BOLD,
        )

        # Get icon color from widget data if it exists
        self.icon_color = widget.data.get('rail_icon_color', 'primary')

        
    
        # Standard popup menu options all files/widgets have
        self.menu_options = [
            ft.TextButton(content=ft.Text("Rename", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300), on_click=self.rename_clicked),
            ft.PopupMenuButton(
                expand=True,
                tooltip="",
                content=ft.Row([
                    ft.Icon(ft.Icons.COLOR_LENS_OUTLINED, color=ft.Colors.GREY_300),
                    ft.Text("Color", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300), 
                ]),
                items=self.get_colors()
            ),
            ft.TextButton(content=ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ]

        # Parent constructor
        super().__init__(
            on_enter = self.on_hover,
            on_exit = self.on_stop_hover,
            on_secondary_tap = self.open_menu,
            on_tap = lambda e: self.widget.focus(),

            content = ft.Container(
                expand=True, 
                padding=ft.Padding(5, 2, 5, 2),
                content=ft.Row(
                    expand=True,
                    controls=[
                        ft.Icon(self.icon, color=self.icon_color), 
                        ft.Text(value=self.capital_title, style=self.text_style),
                    ],
                ),
            ),

            mouse_cursor = ft.MouseCursor.CLICK
        )

    def get_colors(self) -> list[ft.Control]:
        ''' Returns a list of all available colors for icon changing '''

        # Called when a color option is clicked on popup menu to change icon color
        def _change_icon_color(color: str):
            ''' Passes in our kwargs to the widget, and applies the updates '''

            # Change the data
            self.widget.change_data(**{'rail_icon_color': color})
            self.icon_color = color
            
            # Change our icon to match, apply the update
            self.reload()
            #self.close_menu(None)

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

        color_controls = [] 
        for color in colors:
            color_controls.append(
                ft.PopupMenuItem(
                    content=ft.Text(color.capitalize(), weight=ft.FontWeight.BOLD, color=color),
                    on_click=lambda e, col=color: _change_icon_color(col)
                )
            )

        return color_controls

    # Called when hovering mouse over a tree view item
    def on_hover(self, e):
        self.content.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        self.widget.p.update()

    def on_stop_hover(self, e):
        self.content.bgcolor = ft.Colors.TRANSPARENT
        self.widget.p.update()

    # Called when rename button is clicked
    def rename_clicked(self, e):

        # Track if our name is unique for checks, and if we're submitting or not
        is_unique = True
        submitting = False

        # Grab our current name for comparison
        current_name = self.widget.title

        # Called when clicking outside the input field to cancel renaming
        def _cancel_rename(e):
            ''' Puts our name back to static and unalterable '''

            # Grab our submitting state
            nonlocal submitting

            # Since this auto calls on submit, we need to check. If it is cuz of a submit, do nothing
            if submitting:
                submitting = not submitting     # Change submit status to False so we can de-select the textbox
                return
            
            # Otherwise we're not submitting (just clicking off the textbox), so we cancel the rename
            else:

                self.content.content.controls[1] = ft.Text(
                    value=self.capital_title,
                    style=ft.TextStyle(
                        size=14,
                        color=ft.Colors.PRIMARY,
                        weight=ft.FontWeight.BOLD,
                    )
                )
                self.widget.p.update()

        # Called everytime a change in textbox occurs
        def _name_check(e):
            ''' Checks if the name is unique within its type of widget '''

            # Grab the new name, and tag
            name = e.control.value
            tag = self.widget.data.get('tag', None)

            # Nonlocal variables
            nonlocal is_unique
            nonlocal submitting

            # Set submitting to false, and unique to True
            submitting = False
            is_unique = True


            # Check our widgets tag, and then check for uniqueness accordingly
            if tag is not None:

                # Chapters check (Not sure how, but it grabs the title as the objects so whatevs it works)
                if tag == "chapter":
                    for chapter in self.widget.story.chapters:
                        if chapter == name and chapter != current_name:
                            is_unique = False

                # Notes
                elif tag == "note":
                    for note in self.widget.story.notes:
                        if note == name and note != current_name:
                            is_unique = False

                # Characters
                elif tag == "character":
                    for character in self.widget.story.characters:
                        if character == name and character != current_name:
                            is_unique = False

                # Maps
                elif tag == "maps":
                    for map_widget in self.widget.story.maps:
                        if map_widget == name and map_widget != current_name:
                            is_unique = False

            # Give us our error text if not unique
            if not is_unique:
                e.control.error_text = "Name already exists"
            else:
                e.control.error_text = None

            # Apply the update
            self.widget.p.update()

        # Called when submitting our textfield.
        def _submit_name(e):
            ''' Checks that we're unique and renames the widget if so. on_blur is auto called after this, so we handle that as well '''

            # Get our name and check if its unique
            name = e.control.value

            # Non local variables
            nonlocal is_unique
            nonlocal text_field
            nonlocal submitting

            # Set submitting to True
            submitting = True

            # If it is, call the rename function. It will do everything else
            if is_unique:
                self.widget.rename(name)
                
            # Otherwise make sure we show our error
            else:
                text_field.error_text = "Name already exists"
                text_field.focus()                                  # Auto focus the textfield
                self.widget.p.update()
                
        # Our text field that our functions use for renaming and referencing
        text_field = ft.TextField(
            value=self.capital_title,
            expand=True,
            autofocus=True,
            on_submit=_submit_name,
            on_change=_name_check,
            on_blur=_cancel_rename,
        )

        # Replaces our name text with a text field for renaming
        self.content.content.controls[1] = text_field

        # Clears our popup menu button and applies to the UI
        self.widget.p.overlay.clear()
        self.widget.p.update()

    
    # Called clicking outside the menu to close it
    def close_menu(self, e):
        self.widget.p.overlay.clear()
        self.widget.p.update()

        
    # Called when we right click our object on the tree view
    def open_menu(self, e):
        ''' Pops open our options on the screen at the mouse location '''
        
        # Our container that contains a column of our options. Need to use container for positioning
        menu = ft.Container(
            left=self.widget.story.mouse_x,     # Positions the menu at the mouse location
            top=self.widget.story.mouse_y,
            border_radius=ft.border_radius.all(4),
            bgcolor=ft.Colors.ON_SECONDARY,
            padding=2,
            alignment=ft.alignment.center,
            content=ft.Column(controls=self.menu_options),
        )

        # Outside gesture detector to close the menu when clicking outside the menu container
        outside_detector = ft.GestureDetector(
            expand=True,
            on_tap=self.close_menu,
            on_secondary_tap=self.close_menu,
        )

        # Overlay is a stack, so add the detector, then the menu container
        self.widget.p.overlay.append(outside_detector)
        self.widget.p.overlay.append(menu)
        self.widget.p.update()


    def reload(self):
        self.content = ft.Container(
            expand=True, 
            padding=ft.Padding(5, 2, 5, 2),
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Icon(self.icon, color=self.icon_color), 
                    ft.Text(value=self.capital_title, style=self.text_style),
                ],
            ),
        )

        self.widget.p.update()



