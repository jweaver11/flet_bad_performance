import flet as ft

from models.user import user
from ui.rails.character_rail import create_characters_rail  
from ui.rails.content_rail import content_rail
from ui.rails.plot_timeline_rail import plot_timeline_rail
from ui.rails.world_building_rail import world_building_rail
from ui.rails.drawing_board_rail import drawing_board_rail
from ui.rails.notes_rail import notes_rail



# Creates our 'active_rail', which holds all of our rails, and renderes the selected one
def create_active_rail(page: ft.Page):
    
    # Create our rails
    characters_rail = create_characters_rail(page)
    print(characters_rail)

    # Add our rails to the dict/map
    user.active_story.workspace_rails.update({
        0: content_rail,
        1: characters_rail,
        2: plot_timeline_rail, 
        3: world_building_rail,
        4: drawing_board_rail,
        5: notes_rail,
    })

    # Container for the active workspace rail.
    active_workspace_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
        width=200,  # Sets the width
        content=user.active_story.active_rail,  # Sets our active rail column
    )


    return active_workspace_rail_container
