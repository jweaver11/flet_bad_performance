import flet as ft
from models.user import user
from models.widget import Widget

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

        self.visible = False

        self.workspace_order = []

        # Save theme mode of either light or dark
        self.user_theme_mode = ft.ThemeMode.DARK    # Can't call this theme_mode, since containers have their own theme mode
        self.theme_color_scheme = ft.Colors.BLUE    # Save our color scheme for the theme

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
            self.theme_color_scheme = e.control.value
            self.p.theme = ft.Theme(color_scheme_seed=self.theme_color_scheme)
            self.p.dark_theme = ft.Theme(color_scheme_seed=self.theme_color_scheme)
            self.p.update()

        # Dropdown so user can change their color scheme
        self.color_scheme_dropdown = ft.Dropdown(
            #editable=True,
            label="Theme Color",
            capitalization= ft.TextCapitalization.SENTENCES,
            options=get_color_scheme_options(),
            on_change=change_color_scheme_picked,
        )
        
        # Background color of widgets that changes depending if in light theme or dark theme
        #self.workspace_bgcolor = ft.Colors.ON_SECONDARY #if self.user_theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_200

        


        # Runs when the switch toggling the color change of characters names based on morality is clicked
        def change_name_colors_switch(e):
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
            if self.user_theme_mode == ft.ThemeMode.DARK:   # Check which theme we're on
                self.user_theme_mode = ft.ThemeMode.LIGHT   # change the theme mode so we can save it
                self.theme_button.icon = ft.Icons.DARK_MODE # Change the icon of theme button
                
            elif self.user_theme_mode == ft.ThemeMode.LIGHT:
                self.user_theme_mode = ft.ThemeMode.DARK
                self.theme_button.icon = ft.Icons.LIGHT_MODE
               

            #user.workspace.bgcolor = self.workspace_bgcolor
            self.p.theme_mode = self.user_theme_mode
            self.p.update()
            print(self.user_theme_mode)

        # Icon of the theme button that changes depending on if we're dark or light mode
        self.theme_icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        # Button that changes the theme from dark or light when clicked
        self.theme_button = ft.IconButton(icon=self.theme_icon, on_click=toggle_theme)


        

        self.content=ft.Column([
            ft.TextButton(
                "Reorder Workspaces", 
                icon=ft.Icons.REORDER_ROUNDED,
                on_click=lambda e: user.all_workspaces_rail.make_rail_reorderable()
            ),
            self.change_name_colors,
            self.theme_button,
            self.color_scheme_dropdown,

        ])

        self.tab.content = self.content

        
    
        
