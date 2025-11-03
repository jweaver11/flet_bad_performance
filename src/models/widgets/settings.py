''' 
Model for our settings widget. Settings widget stores app and story settings, and displays them in a tab
A Settings object is created for every story
'''

import flet as ft
from models.story import Story
from models.widget import Widget
from handlers.verify_data import verify_data


class Settings(Widget):
    # Constructor
    def __init__(self, page: ft.Page, directory_path: str, story: Story=None, data: dict=None):
        
        # Constructor the parent widget class
        super().__init__(
            title = "Settings",  # Name of character, but all objects have a 'title' for identification, so characters do too
            page = page,   # Grabs our original page, as sometimes the reference gets lost. with all the UI changes that happen. p.update() always works
            story = story,
            directory_path = directory_path,
            data = data,
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "settings",  # Tag for logic, should be overwritten by child classes
                'active_story': "/",    # this works as a route for the correct story
                'is_maximized': True,   # If the window is maximized or not
                'tab_title_color': "primary",        # the tab color
                'theme_mode': "system",       # the apps theme mode, dark or light
                'active_rail_width': 200,  # Width of our active rail that we can resize
                'theme_color_scheme': "blue",   # the color scheme of the app
                'change_name_colors_based_on_morality': True,   # If characters names change colors in char based on morality
                'workspaces_rail_order': list,      # Order of the workspace rail
                'workspaces_rail_is_collapsed': False,  # If the all workspaces rail is collapsed or not
                'workspaces_rail_is_reorderable': False,  # If the all workspaces rail is reorderable or not
                'is_maximized': bool,   # If the window is maximized or not
                'workspaces_rail_order': [      # Order of the workspace rail
                    "content",
                    "characters",
                    "timelines",
                    "world_building",
                    "drawing_board",
                    "planning",
                ],
            },
        )

        self.reload_tab()
        self.reload_widget()  # Loads our settings widget UI


    # Called when the button to reorder the workspaces is clicked
    def toggle_rail_reorderable(self):
        ''' Toggles if the all workspaces rail is reorderable or not '''

        # Grabs our active story from the view on page, and toggles its reorder logic
        try:
            story = self.p.views[0]
            story.all_workspaces_rail.toggle_reorder_rail(story)
        except Exception as e:
            print(f"Error toggling rail reorderable: {e}")

    
    # Called when someone expands the drop down holding the color scheme options
    def reload_widget(self):
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
            
            # Theme is set to system by default, this checks for that
            else:  
                
                if self.p.theme_mode == ft.ThemeMode.DARK:
                    self.data['theme_mode'] = "dark"
                    self.theme_button.icon = ft.Icons.LIGHT_MODE
                else:
                    self.data['theme_mode'] = "light"
                    self.theme_button.icon = ft.Icons.DARK_MODE
               
            # Save the updated settings to the JSON file, apply to the page and update
            self.save_dict()
            self.p.theme_mode = self.data['theme_mode']
            self.p.update()
            

        # Icon of the theme button that changes depending on if we're dark or light mode
        self.theme_icon = ft.Icons.DARK_MODE if self.p.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE

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

        # OPTION TO NOT HAVE CHARACTERS SEX CHANGE COLORS?
        # Option to change where certain widgets default display to in pins
        # NOTE: Add is_first_launch check to run a tutorial
        # Option for compact vs spread on view in the rails



        
    
        
