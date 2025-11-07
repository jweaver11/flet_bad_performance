

# Class for the drop down to add more arcs or plotpoints to a timeline or arc
import flet as ft
from models.story import Story
from styles.menu_option_style import Menu_Option_Style


class Arcs_Or_Plotpoints_Dropdown(ft.GestureDetector):

    # Constructor
    def __init__(
        self, 
        title: str,                                             # Title of our dropdown             
        story: Story,                                           # Our story object that was passed in
        additional_menu_options: list[ft.Control] = None,       # Additional menu options to add to the right click menu
    ):

        # Set our parameters
        self.title = title                          
        self.story = story     
        self.additional_menu_options = additional_menu_options if additional_menu_options else []                     


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
            #on_blur=self.on_new_item_blur,
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

    # Called when right clicking our dropdown to get menu options
    def get_menu_options(self) -> list[ft.Control]:

        menu_options = [] 

        # Run through our additional menu options if we have any, and set their on_click methods
        for option in self.additional_menu_options or []:

            # Set their on_click to call our on_click method, which can handle any type of widget
            option.on_tap = lambda e, t=option.data: self.new_item_clicked(type=t)

            # Add them to the list
            menu_options.append(option)

        # Color changing popup menu
        menu_options.append(    
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
            )
        )

        return menu_options
    

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

    def reload(self):
        expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=self.title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            #initially_expanded=self.is_expanded,
            tile_padding=ft.Padding(0, 0, 0, 0),
            controls_padding=ft.Padding(10, 0, 0, 0),       # Keeps all sub children indented
            leading=ft.Icon(ft.Icons.TIMELINE_ROUNDED),
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            adaptive=True,
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(),
            #on_change=lambda e: self.toggle_expand(),
            controls=[self.new_item_textfield], 
        )

        self.content = expansion_tile

