''' Parent class for our settings widget'''

import flet as ft
import os
#from models.app import app
from models.story import Story
from models.widget import Widget
from constants.data_paths import settings_path
import json

# 
# OPTION TO NOT HAVE CHARACTERS SEX CHANGE COLORS?
#


class Settings(Widget):
    # Constructor
    def __init__(self, page: ft.Page, directory_path: str, story: Story=None, data: dict = None):
        
        # Constructor the parent widget class
        super().__init__(
            title = "Settings",  # Name of character, but all objects have a 'title' for identification, so characters do too
            tag = "settings",  # Tag for logic, mostly for routing it through our story object
            p = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            story = story,
            directory_path = directory_path,
            data = data,
        )

        # Loads our settings data from the JSON file
        self.load_from_dict()

        # Called when someone expands the drop down holding the color scheme options
        def get_color_scheme_options():
            ''' Adds our choices to the color scheme dropdown control'''

            # Our dropdown options for our color scheme dropdown control
            color_scheme_options = [
                ft.Colors.RED,
                ft.Colors.BLUE,
                ft.Colors.YELLOW,
                ft.Colors.PURPLE,
                ft.Colors.LIME,
                ft.Colors.CYAN,
            ]

            # Create a list to hold our dropdown options
            options = []

            # Runs through our colors above and adds them to the dropdown
            for color in color_scheme_options:
                options.append(
                    ft.DropdownOption(
                        key=color.value.capitalize(),
                        content=ft.Text(
                            value=color.value.capitalize(),
                            color=color,
                        ),
                    )
                )
            return options
        
        # Called when a dropdown option is selected. Saves our choice, and applies it to the page
        def change_color_scheme_picked(e):
            ''' Saves our color scheme choice and applies it to the page '''

            # Save our color scheme choice to our objects data
            self.data['theme_color_scheme'] = e.control.value

            # Applies this theme to our page, for both dark and light themes
            self.p.theme = ft.Theme(color_scheme_seed=self.data['theme_color_scheme'])
            self.p.dark_theme = ft.Theme(color_scheme_seed=self.data['theme_color_scheme'])
            
            # Save the updated settings to the JSON file and update the page
            self.save_dict()
            self.p.update()

        # Dropdown so app can change their color scheme
        self.color_scheme_dropdown = ft.Dropdown(
            label="Theme Color",
            capitalization= ft.TextCapitalization.SENTENCES,    # Capitalize our options
            options=get_color_scheme_options(),
            on_change=change_color_scheme_picked,
        )

        # Runs when the switch toggling the color change of characters names based on morality is clicked
        def change_name_colors_switch(e):
            ''' Changes the name color of characters based on morality when toggled '''

            # Change our data to reflect the switch state
            self.data['change_name_colors_based_on_morality'] = e.control.value
            self.save_dict()  

            # Runs through all our characters, and updates their name color accordingly and reloads their widget
            #for char in app.active_story.characters:  
                #char.check_morality()
                #char.reload_widget() 

            # Reloads the rail. Its better here than running it twice for no reason in character class    
            from ui.rails.characters_rail import reload_character_rail
            reload_character_rail(self.p)

        # The switch for toggling if characters names change colors based on morality
        self.change_name_colors = ft.Switch(
            label="Change characters name colors for good, evil, and neutral", 
            value=self.data['change_name_colors_based_on_morality'],
            on_change=change_name_colors_switch
        )

        # Called when theme switch is changed. Switches from dark to light theme, or reverse
        def toggle_theme(e):
            ''' Changes our settings theme data from dark to light or reverse '''

            print("switch_theme called")

            # Change theme mode data, and the icon to match
            if self.data['theme_mode'] == "dark":   # Check which theme we're on
                self.data['theme_mode'] = "light"   # change the theme mode so we can save it
                self.theme_button.icon = ft.Icons.DARK_MODE # Change the icon of theme button
            elif self.data['theme_mode'] == "light":
                self.data['theme_mode'] = "dark"
                self.theme_button.icon = ft.Icons.LIGHT_MODE
               
            # Save the updated settings to the JSON file, apply to the page and update
            self.save_dict()
            self.p.theme_mode = self.data['theme_mode']
            self.p.update()
            

        # Icon of the theme button that changes depending on if we're dark or light mode
        self.theme_icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE

        # Button that changes the theme from dark or light when clicked
        self.theme_button = ft.IconButton(icon=self.theme_icon, on_click=toggle_theme)
        
        # Sets our widgets content. May need a 'reload_widget' method later, but for now this works
        self.content=ft.Column([
            ft.TextButton(
                "Reorder Workspaces", 
                icon=ft.Icons.REORDER_ROUNDED,
                #on_click=lambda e: story.all_workspaces_rail.toggle_rail_reorderable(),
                on_click=lambda e: self.toggle_rail_reorderable()
            ),
            self.change_name_colors,
            self.theme_button,
            self.color_scheme_dropdown,
        ])

        # Sets our content to our tab so it shows up
        self.tab.content = self.content

        # Sets our header
        tab = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Sets our object content to be our tab
        self.content = tab


    # Called when new settings object is created
    def load_from_dict(self):
        ''' Loads our settings data from the JSON file. If its first launch, we create the file with default data '''

        #print("load from dict called")

        # Set the path to our settings file
        file_path = os.path.join(settings_path, "settings.json")

        # Data set upon first launch of program, or if file can't be loaded
        default_data = {
            'visible': False,   # If our settings widget is visible or not
            'pin_location': "main", 
            'active_story': "/",    # this works as a route for the correct story
            'is_maximized': True,   # If the window is maximized or not
            
            'tab_color': "blue",        # the tab color
            'theme_mode': "dark",       # the apps theme mode, dark or light
            'theme_color_scheme': "blue",   # the color scheme of the app
            'change_name_colors_based_on_morality': True,   # If characters names change colors in char based on morality
            'workspaces_rail_order': [      # Order of the workspace rail
                "content",
                "characters",
                "plot_and_timeline",
                "world_building",
                "drawing_board",
                "notes",
            ],
            'workspaces_rail_is_collapsed': False,  # If the all workspaces rail is collapsed or not
            'workspaces_rail_is_reorderable': False,  # If the all workspaces rail is reorderable or not
            'active_rail_width': 200,   # Width of our active rail that we can resize
        }
        
        try:
            # Try to load existing settings from file
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    loaded_data = json.load(f)
                
                # Start with default data and update with loaded data
                self.data = default_data.copy()
                self.data.update(loaded_data)
                self.visible = self.data.get('visible', False)
                
                #print(f"Settings loaded successfully from {settings_file_path}")

            else:
                # File doesn't exist, use default data
                self.data = default_data
                #print("Settings file does not exist, using default values.")
                
                # Optionally create the file with default data
                self.save_dict()
                
        # Handle JSON parsing errors or file access issues
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            # Handle JSON parsing errors or file access issues
            #print(f"Error loading settings: {e}")
            #print("Using default values.")
            self.data = default_data
            
            # Optionally create/overwrite the file with default data
            try:
                self.save_dict()  # This will save the default data to file
            except Exception as save_error:
                print(f"Could not save default settings: {save_error}")

    # Called when the button to reorder the workspaces is clicked
    def toggle_rail_reorderable(self):
        ''' Toggles if the all workspaces rail is reorderable or not '''

        # Grabs our active story from the view on page, and toggles its reorder logic
        try:
            story = self.p.views[0]
            story.all_workspaces_rail.toggle_reorder_rail(story)
        except Exception as e:
            print(f"Error toggling rail reorderable: {e}")



        
    
        
