import flet as ft

from models.user import user
from ui.rails.characters_rail import create_characters_rail  
from ui.rails.content_rail import create_content_rail
from ui.rails.plot_timeline_rail import create_plot_and_timeline_rail
from ui.rails.world_building_rail import create_world_building_rail
from ui.rails.drawing_board_rail import create_drawing_board_rail
from ui.rails.notes_rail import create_notes_rail
from handlers.render_widgets import render_widgets


# Class for creating our active rail inside of our active_story object.
# This is freely re-created on program launch, and manages which rail is active
# Depending on the workspace selection
class Active_Rail(ft.Container):
    def __init__(self, page: ft.Page):
    
        self.p = page  # Store the page reference
  
        # Consistent styling for all our rails
        super().__init__(
            alignment=ft.alignment.center,  # Aligns content to the
            padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            width=user.settings.data['active_rail_width'],  # Sets the width
        )

        # Give us the correct rail on program startup based on our selected workspace
        if user.all_workspaces_rail.selected_workspace == "content":
            self.content = create_content_rail(page)
        elif user.all_workspaces_rail.selected_workspace == "characters":
            self.content = create_characters_rail(page)
        elif user.all_workspaces_rail.selected_workspace == "plot_and_timeline":
            self.content = create_plot_and_timeline_rail(page)
        elif user.all_workspaces_rail.selected_workspace == "world_building":
            self.content = create_world_building_rail(page)
        elif user.all_workspaces_rail.selected_workspace == "drawing_board":
            self.content = create_drawing_board_rail(page)
        elif user.all_workspaces_rail.selected_workspace == "notes":
            self.content = create_notes_rail(page)



   
