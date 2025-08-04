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

        def change_name_colors_switch(e):

            for char in user.active_story.characters:
                char.check_morality()
                char.reload_widget()
            from workspaces.character.character_rail import reload_character_rail
            reload_character_rail(self.p)

        self.change_name_colors = ft.Switch(
            label="Change characters name colors for good, evil, and neutral", 
            value=True,
            on_change=change_name_colors_switch
            )


        super().__init__(
            expand=True, 
            padding=6,
            visible=False,  # Start invisible
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            bgcolor = ft.Colors.GREY_900,
            content=ft.Column([
                ft.TextButton(
                    "make rail reorderable", 
                    icon=ft.Icons.REORDER_ROUNDED,
                    on_click=lambda e: user.all_workspaces_rail.make_rail_reorderable()
                ),
                self.change_name_colors,
            ])

        )
