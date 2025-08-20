import flet as ft
import os
from models.user import user
from models.widget import Widget
from constants.data_paths import settings_path
import json

# 
# OPTION TO NOT HAVE CHARACTERS SEX CHANGE COLORS?
#



class Settings(Widget):
    def __init__(self, page: ft.Page):
        # Arguments our widget needs
        super().__init__(
            title = "Settings",  # Name of character, but all objects have a 'title' for identification, so characters do too
            tag = "settings",  # Tag for logic, mostly for routing it through our story object
            p = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            pin_location = "main",  # Start in left pin location
            
        )

        self.__load_from_dict()


        # Our dropdown options for our color scheme dropdown control
        self.theme_color_scheme_options = [
            ft.Colors.RED,
            ft.Colors.BLUE,
            ft.Colors.YELLOW,
            ft.Colors.PURPLE,
            ft.Colors.LIME,
            ft.Colors.CYAN,
        ]

        # Function to add our color scheme options when our dropdown expands
        def get_color_scheme_options():
            options = []
            for color in self.theme_color_scheme_options:
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
            self.data['theme_color_scheme'] = e.control.value
            self.data['theme_color_scheme'] = e.control.value  # Keep for backward compatibility if used elsewhere
            self.p.theme = ft.Theme(color_scheme_seed=self.data['theme_color_scheme'])
            self.p.dark_theme = ft.Theme(color_scheme_seed=self.data['theme_color_scheme'])
            
            # Save the updated settings to the JSON file
            self.__save_dict()
            
            self.p.update()

        # Dropdown so user can change their color scheme
        self.color_scheme_dropdown = ft.Dropdown(
            #editable=True,
            label="Theme Color",
            capitalization= ft.TextCapitalization.SENTENCES,
            options=get_color_scheme_options(),
            on_change=change_color_scheme_picked,
        )
        


        # Runs when the switch toggling the color change of characters names based on morality is clicked
        def change_name_colors_switch(e):
            self.data['change_name_colors_based_on_morality'] = e.control.value
            self.__save_dict()  # Save the updated settings to the JSON file
            # runs through all our characters, and updates their name color accordingly
            for char in user.active_story.characters:  
                char.check_morality()
                char.reload_widget()    # Updates their widget accordingly

            # Reloads the rail. Its better here than running it twice for no reason in character class    
            from ui.rails.character_rail import reload_character_rail
            reload_character_rail(self.p)

        # The switch for toggling if characters names change colors based on morality
        self.change_name_colors = ft.Switch(
            label="Change characters name colors for good, evil, and neutral", 
            value=True,
            on_change=change_name_colors_switch
        )

        # Called when thme switch is changed. Switches from dark to light theme, or reverse
        def toggle_theme(e):
            print("switch_theme called")
            print(self.p.theme_mode)
            print("datta: ", self.data['theme_mode'])
            if self.data['theme_mode'] == "dark":   # Check which theme we're on
                self.data['theme_mode'] = "light"   # change the theme mode so we can save it
                self.theme_button.icon = ft.Icons.DARK_MODE # Change the icon of theme button
                
            elif self.data['theme_mode'] == "light":
                self.data['theme_mode'] = "dark"
                self.theme_button.icon = ft.Icons.LIGHT_MODE
               
            # Save the updated settings to the JSON file
            self.__save_dict()

            #user.workspace.bgcolor = self.workspace_bgcolor
            self.p.theme_mode = self.data['theme_mode']
            self.p.update()
            print(self.data['theme_mode'])

        # Icon of the theme button that changes depending on if we're dark or light mode
        self.theme_icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        # Button that changes the theme from dark or light when clicked
        self.theme_button = ft.IconButton(icon=self.theme_icon, on_click=toggle_theme)


        
        self.content=ft.Column([
            ft.TextButton(
                "Reorder Workspaces", 
                icon=ft.Icons.REORDER_ROUNDED,
                on_click=lambda e: user.all_workspaces_rail.toggle_rail_reorderable()
            ),
            self.change_name_colors,
            self.theme_button,
            self.color_scheme_dropdown,

        ])

        self.tab.content = self.content

        # Sets our header
        tab = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
          
        
        # Set our content
        self.content = tab

    # Save our object as a dictionary for json serialization
    def __save_dict(self):
        print("save settings dict called")
        settings_file_path = os.path.join(settings_path, "settings.json")
        
        with open(settings_file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def __load_from_dict(self):
        print("load from dict called")
        settings_file_path = os.path.join(settings_path, "settings.json")

        # Data set upon first launch of program, or if file can't be loaded
        default_data = {
            'visible': False,   # If our settings widget is visible or not
            'tab_color': "blue",        # the tab color
            'theme_mode': "dark",       # the apps theme mode, dark or light
            'theme_color_scheme': "blue",   # the color scheme of the app
            'change_name_colors_based_on_morality': True,   # If characters names change colors in char based on morality
            'workspaces_rail_order': [
                "content",
                "characters",
                "plot_and_timeline",
                "world_building",
                "drawing_board",
                "notes",
            ],
            'all_workspaces_rail_is_collapsed': False,  # If the all workspaces rail is collapsed or not
            'all_workspaces_rail_is_reorderable': False,  # If the all workspaces rail is reorderable or not
        }
        
        try:
            # Try to load existing settings from file
            if os.path.exists(settings_file_path):
                with open(settings_file_path, "r") as f:
                    loaded_data = json.load(f)
                
                # Start with default data and update with loaded data
                self.data = default_data.copy()
                self.data.update(loaded_data)
                self.visible = self.data.get('visible', False)
                
                print(f"Settings loaded successfully from {settings_file_path}")
            else:
                # File doesn't exist, use default data
                self.data = default_data
                print("Settings file does not exist, using default values.")
                
                # Optionally create the file with default data
                self.__save_dict()  # This will save the default data to file
                
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            # Handle JSON parsing errors or file access issues
            print(f"Error loading settings: {e}")
            print("Using default values.")
            self.data = default_data
            
            # Optionally create/overwrite the file with default data
            try:
                self.__save_dict()  # This will save the default data to file
            except Exception as save_error:
                print(f"Could not save default settings: {save_error}")

    # Make our settings visible or not
    def change_visibility(self):
        self.visible = not self.visible
        self.data['visible'] = self.visible
        self.__save_dict()


        
    
        
