import flet as ft
from models.user import user

# Auto green characters = good, red = bad
# Checkbox labeled 'reorder_workspaces' that triggers the reorder event

# re-order the list of workspaces in the rail, show and hide them
'''
# Inside of workspaces rail to make reorderable or not,
# But will move here
# from hud.workspaces.rail import make_reorderable
ft.TextButton( 
    text="Reorder", 
    on_click=make_reorderable,
),
'''
# Snackbar alerts?


class Settings(ft.Container):
    def __init__(self, page: ft.Page):
        self.yo_momma = "yo mommaa"
        self.pin_location = "main"
        self.p = page

        # Runs when the switch toggling the color change of characters names based on morality is clicked
        def change_name_colors_switch(e):
            # runs through all our characters, and updates their name color accordingly
            for char in user.active_story.characters:  
                char.check_morality()
                char.reload_widget()    # Updates their widget accordingly

            # Reloads the rail. Its better here than running it twice for no reason in character class    
            from workspaces.character.character_rail import reload_character_rail
            reload_character_rail(self.p)

        # The switch for toggling if characters names change colors based on morality
        self.change_name_colors = ft.Switch(
            label="Change characters name colors for good, evil, and neutral", 
            value=True,
            on_change=change_name_colors_switch
        )

        # Called when thme switch is changed. Switches from dark to light theme
        def toggle_theme(e):
            print("switch_theme called")
            print(self.p.theme_mode)
            if self.p.theme_mode == ft.ThemeMode.DARK:
                self.p.theme_mode = ft.ThemeMode.LIGHT
                self.theme_button.icon = ft.Icons.DARK_MODE
            elif self.p.theme_mode == ft.ThemeMode.LIGHT:
                self.p.theme_mode = ft.ThemeMode.DARK
                self.theme_button.icon = ft.Icons.LIGHT_MODE

            self.p.update()
            print(self.p.theme_mode)
            #self.update()

        self.theme_icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
        self.theme_button = ft.IconButton(icon=self.theme_icon, on_click=toggle_theme)


        # Init our settings container(widget) with the uniform formatting of the other objects
        super().__init__(
            expand=True, 
            padding=6,
            visible=True,
            border = ft.border.all(2, ft.Colors.GREY_800),
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor = ft.Colors.ON_INVERSE_SURFACE,
            content=ft.Column([
                ft.TextButton(
                    "Reorder Workspaces", 
                    icon=ft.Icons.REORDER_ROUNDED,
                    on_click=lambda e: user.all_workspaces_rail.make_rail_reorderable()
                ),
                self.change_name_colors,
                self.theme_button,
            ])
        )
