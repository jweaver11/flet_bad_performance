'''
Extended flet controls that implement the same styling for easy access
'''

import flet as ft
from styles.menu_option_style import Menu_Option_Style
from models.story import Story
from models.widgets.timeline import Timeline


# TODO: When clicking and expanding, make sure to set the active_timeline to this timeline, 
# so we can use the buttons at top of rail when there are multiple timelines

# Expansion tiles used for timelines (when more than 1), plotpoints labels, and arcs labels
class Timeline_Dropdown(ft.GestureDetector):

    # Constructor
    def __init__(
        self,
        title: str,                                              # Title of this folder
        story: Story,                                            # Story reference for mouse positions and other logic
        additional_menu_options: list[ft.Control],               # Additional menu options when right clicking a category, depending on the rail
        timeline: Timeline,                                      # Reference to the timeline this dropdown represents 
        rail,     
    ):

        # Set our parameters
        self.title = title.title()
        self.story = story
        self.timeline = timeline
        self.additional_menu_options = additional_menu_options
        self.rail = rail


        # Set other variables
        self.color = ft.Colors.PRIMARY
        self.is_expanded = self.timeline.data.get("dropdown_is_expanded", True)

        # State tracking variables
        self.are_submitting = False
        self.item_is_unique = True
        self.is_focused = False
        
        # Set our text style
        self.text_style = ft.TextStyle(
            size=14,
            color=ft.Colors.ON_SURFACE,
            weight=ft.FontWeight.BOLD,
        )
        
        # Textfield for creating new items (sub-categories, chapters, notes, characters, etc.)
        self.new_item_textfield = ft.TextField(  
            hint_text=f"new_item Title",   
            data="data passed in",       
            autofocus=True,
            capitalization=ft.TextCapitalization.SENTENCES,
            on_change=self.new_item_check,
            on_blur=self.on_new_item_blur,
            on_submit=self.new_item_submit,
            visible=False,
            text_style=self.text_style,
            dense=True,
        )

        self.expansion_tile: ft.ExpansionTile = None

        
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
    
        # Our menu options list
        menu_options: list[ft.Control] = []

        # Run through our additional menu options if we have any, and set their on_click methods
        for option in self.additional_menu_options or []:

            # Set their on_click to call our on_click method, which can handle any type of widget
            option.on_tap = lambda e: self.new_item_clicked(e)

            # Add to our menu options list
            menu_options.append(option)

        # Return our menu options list
        return menu_options
    
    # Called when expanding/collapsing the directory
    def toggle_expand(self):
        ''' Makes sure our state and data match the updated expanded/collapsed state '''

        #print("Toggling expand for ", self.title)

        self.is_expanded = not self.is_expanded

        self.timeline.data["dropdown_is_expanded"] = self.is_expanded
        self.timeline.save_dict()

        #print("Active dropdown before:", self.rail.active_dropdown)
        if self.rail.active_dropdown is not None:
            if hasattr(self.rail.active_dropdown, "is_focused"):
                
                self.rail.active_dropdown.is_focused = False
                self.rail.active_dropdown.refresh_expansion_tile()
            
            else:
                self.rail.active_dropdown.timeline_dropdown.is_focused = False
                self.rail.active_dropdown.timeline_dropdown.refresh_expansion_tile()

        self.rail.active_dropdown = self
        self.rail.refresh_buttons()

        self.is_focused = True
        self.refresh_expansion_tile()
        

    # Called when creating a new plot point or arc only
    def new_item_clicked(self, e=None, tag: str=None):
        ''' Shows the textfield for creating new item. Requires what type of item (category, chapter, note, etc.) '''

        # If this is called from outside our object, pass in a tag instead
        if e is not None: 
            data = e.control.data
        else:
            data = tag
        
        # Check our expanded state. Rebuild if needed
        if self.is_expanded == False:
            self.toggle_expand()
            self.reload()
         
        # If the data passed in is a plotpoint
        if data == "plot_point":

            self.content.controls[0].new_item_clicked(tag="plot_point")

        # Otherwise we're an arc
        else:

            self.content.controls[1].new_item_clicked(tag="arc")

        # Close the menu, which will also update the page
        self.story.close_menu()

    # Called when our new item textfield changes
    def new_item_check(self, e):
        ''' Checks if our new item is unique in our timeline's dicts '''

        # Get our name and check if its unique
        title = e.control.value

        # Either plotpoint or arc, whatever we're submitting
        type = e.control.data

        # Check for plot points
        if type == "plot_point":

            # Run through our timeline timeline/arcs plot points to see if the name exists
            if title in self.timeline.plot_points.keys():
                self.item_is_unique = False
                e.control.error_text = "Title must be unique"
            else:
                self.item_is_unique = True
                e.control.error_text = None

        # Check for arcs
        elif type == "arc":
            if title in self.timeline.arcs.keys():
                self.item_is_unique = False
                e.control.error_text = "Title must be unique"
            else:
                self.item_is_unique = True
                e.control.error_text = None

        # Update the page to show changes
        self.story.p.update()

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
                self.story.p.update()
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
            self.story.p.update()


    def new_item_submit(self, e):
        # Get our name and check if its unique
        title = e.control.value

        # Set submitting to True
        self.are_submitting = True

        # Either plotpoint or arc, whatever we're submitting
        type = e.control.data

        # If we're unique, figure out what item we are creating
        if self.item_is_unique:

            # Plot points
            if type == "plot_point":
                self.timeline.create_plot_point(title=title)

            # Arcs
            elif type == "arc":
                self.timeline.create_arc(title=title)
            
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


    def refresh_expansion_tile(self):
        if self.is_focused:
            self.expansion_tile.bgcolor = ft.Colors.with_opacity(.05, "primary")
            self.expansion_tile.collapsed_bgcolor = ft.Colors.with_opacity(.05, "primary")
        else:
            self.expansion_tile.bgcolor = ft.Colors.TRANSPARENT
            self.expansion_tile.collapsed_bgcolor = ft.Colors.TRANSPARENT

        self.timeline.p.update()


    # Called when we need to reload this directory tile
    def reload(self):

        # Set our icon to a timeline unless we are labeld for Plot Points or Arcs dropdown
        icon = ft.Icon(ft.Icons.TIMELINE_ROUNDED, color=self.color) if self.title != "Plot Points" and self.title != "Arcs" else None

        self.expansion_tile = ft.ExpansionTile(
            title=ft.Text(value=self.title, weight=ft.FontWeight.BOLD, text_align="left"),
            dense=True,
            initially_expanded=self.is_expanded,
            visual_density=ft.VisualDensity.COMPACT,
            tile_padding=ft.Padding(6, 0, 0, 0),      # If no leading icon, give us small indentation
            controls_padding=ft.Padding(10, 0, 0, 0),       # Keeps all sub children indented
            leading=icon,
            maintain_state=True,
            expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
            adaptive=True,
            bgcolor=ft.Colors.TRANSPARENT if not self.is_focused else ft.Colors.with_opacity(.2, "primary"),
            collapsed_bgcolor=ft.Colors.TRANSPARENT if not self.is_focused else ft.Colors.with_opacity(.2, "primary"),
            shape=ft.RoundedRectangleBorder(),
            on_change=lambda e: self.toggle_expand(),
        )

        # Our controls should always be 3. Plot point dropdown, arcs dropdown, and a spacing container
        # Re-adds our content controls so we can keep states
        if self.content is not None:        # Protects against first loads
            if self.content.controls is not None:       # Re-add our controls when we reload
                for control in self.content.controls:
                    self.expansion_tile.controls.append(control)

        
        # Set the content
        self.content = self.expansion_tile

        self.refresh_expansion_tile()

        self.timeline.p.update()