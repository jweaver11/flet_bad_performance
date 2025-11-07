'''
Extended flet controls that implement the same styling for easy access
'''

import flet as ft
from styles.menu_option_style import Menu_Option_Style
from models.story import Story
from models.widgets.timeline import Timeline

# Expansion tiles used for timelines and arcs in the timelines rail, and for their plot points and sub-arcs
class Timeline_Dropdown(ft.GestureDetector):

    # Constructor
    def __init__(
        self, 
        #full_path: str,                                         # Full path to this directory
        title: str,                                              # Title of this folder
        story: Story,                                            # Story reference for mouse positions and other logic
        additional_menu_options: list[ft.Control],               # Additional menu options when right clicking a category, depending on the rail
        father: Timeline,                                        # Reference to the timeline or arc this dropdown represents
        type: str = "",                                          # Type of dropdown - either a timeline or arc, other two don't use
        #is_expanded: bool = False,                              # Whether this directory is expanded or not
        #color: str = "primary",                                 # Color of the folder icon
        #father: 'Tree_View_Directory' = None,                   # Optional parent directory tile, if there is one
    ):

        # Set our parameters
        self.title = title.title()
        self.story = story
        self.type = type
        self.father = father
        self.additional_menu_options = additional_menu_options


        # Set other variables
        self.color = ft.Colors.PRIMARY
        self.is_expanded = False

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

    # Called to return our menu options when right clicking our dropdown
    def get_menu_options(self) -> list[ft.Control]:
        ''' Filters the five options we received, and only returns what we need with correct logic '''
        #[
            # Create plot points    (Plotpoint-Dropdown)
            # Create arcs           (Sub-Arcs-Dropdown)
            # Rename.               (Timeline, Arc)
            # Change color.         (Timeline, Arc, Sub-Arcs-Dropdown, Plotpoint-Dropdown)
            # Delete.               (Timeline, Arc)
        #]

        # Create our menu options list
        menu_options = []

        # Only return options for arcs and sub-arcs dropdowns
        if self.title.lower() == "arcs" or self.title.lower() == "sub-arcs":
            menu_options.append(self.additional_menu_options[1])      # Create arc
            menu_options.append(self.additional_menu_options[3])      # Change color

        # Only return options for plot points dropdown
        elif self.title.lower() == "plot points":
            menu_options.append(self.additional_menu_options[0])      # Create plot point
            menu_options.append(self.additional_menu_options[3])      # Change color

        # Only return options for timeline and arc dropdowns
        elif self.type == "timeline" or self.type == "arc":
            menu_options.append(self.additional_menu_options[2])      # Rename
            menu_options.append(self.additional_menu_options[3])      # Change color
            menu_options.append(self.additional_menu_options[4])      # Delete
            
        # For dropdowns representing arcs themselves, return all options
        else:
            menu_options.extend(self.additional_menu_options)    


        # Run through our additional menu options if we have any, and set their on_click methods
        for option in self.additional_menu_options or []:

            # Set their on_click to call our on_click method, which can handle any type of widget
            option.on_tap = lambda e: self.option_clicked(e)

        # Return our menu options list
        return menu_options
    
    # Called when expanding/collapsing the directory
    def toggle_expand(self):
        ''' Makes sure our state and data match the updated expanded/collapsed state '''

        self.is_expanded = not self.is_expanded

        # Save the changes
        

    # Called when creating new category or when additional menu items are clicked
    def option_clicked(self, e):
        ''' Shows the textfield for creating new item. Requires what type of item (category, chapter, note, etc.) '''

        # Clear out any previous value
        self.new_item_textfield.value = None

        # Set the data from our option
        data = e.control.data

        # 
        data_title = data.replace("_", " ").title()

        # Make our textfield visible and set values
        self.new_item_textfield.visible = True
        self.new_item_textfield.data = data
        self.new_item_textfield.hint_text = f"{data_title} Title"


        # Check the type passed in by the option, and route our logic through that
        if data == "plot_point":
            self.new_item_textfield.on_change = self.plot_point_check
            self.new_item_textfield.on_submit = self.plot_point_submit

        elif data== "arc":
            self.new_item_textfield.on_change = self.arc_check
            self.new_item_textfield.on_submit = self.arc_submit

        # Check our expanded state. Rebuild if needed
        if self.is_expanded == False:
            self.toggle_expand()
            self.reload()

        # Close the menu, which will also update the page
        self.story.close_menu()

    def plot_point_check(self, e):
        pass
    def arc_check(self, e):
        pass
    def plot_point_submit(self, e):
        # Call our timeline or arc to create a new plot point
        pass

    def arc_submit(self, e):
        # Get our name and check if its unique
        title = e.control.value

        # Set submitting to True
        self.are_submitting = True

        # If it is, call the rename function. It will do everything else
        if self.item_is_unique:
            self.father.create_arc(title=title)
            
        # Otherwise make sure we show our error
        else:
            self.new_item_textfield.focus()                                  # Auto focus the textfield
            self.story.p.update()

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
                self.new_item_textfield.visible = False
                self.new_item_textfield.value = None
                self.new_item_textfield.error_text = None
                self.story.p.update()
                return
            
            # Otherwise its not unique, re-focus our textfield
            else:
                self.new_item_textfield.visible = True
                self.new_item_textfield.focus()
        
        # If we're not submitting, just hide the textfield and reset values
        else:
            self.new_item_textfield.visible = False
            self.new_item_textfield.value = None
            self.new_item_textfield.error_text = None
            self.story.p.update()


    # Called when we need to reload this directory tile
    def reload(self):
        expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=self.title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            initially_expanded=self.is_expanded,
            visual_density=ft.VisualDensity.COMPACT,
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
            if self.content.controls is not None:
                for control in self.content.controls:
                    if control != self.new_item_textfield:      # Don't re-add our textfield, its already there
                        expansion_tile.controls.append(control)

        
        # Set the content
        self.content = expansion_tile



