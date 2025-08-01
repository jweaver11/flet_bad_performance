import flet as ft

from models.user import user
from workspaces.character.character_rail import characters_rail  
from workspaces.content.content_rail import content_rail
from workspaces.plot_timeline.plot_timeline_rail import plot_timeline_rail
from workspaces.world_building.world_building_rail import world_building_rail
from workspaces.drawing_board.drawing_board_rail import drawing_board_rail
from workspaces.notes.notes_rail import notes_rail


# Default active workspace rail if none selected/on startup rn
default_rail = [ft.TextButton("Select a workspace")]

# Map of all the workspace rails - Rails must be a list of flet controls
workspace_rails = {
    0: default_rail,
}  

# Format our active rail 
active_rail = ft.Column(  
    spacing=0,
    controls=workspace_rails[0],    # On startup, set to char rail
)  

# Creates our 'active_rail', which holds all of our rails, and renderes the selected one
def create_active_rail(page: ft.Page):

    #story = user.active_story
    
    # Create our rails
    chars_rail = characters_rail(page)

    # Default active workspace rail if none selected/on startup rn
    default_rail = [ft.TextButton("Select a workspace")]

    # Map of all the workspace rails - Rails must be a list of flet controls
    workspace_rails.update({
        0: default_rail,
        1: chars_rail,
        2: plot_timeline_rail, 
        3: world_building_rail,
        4: drawing_board_rail,
        5: notes_rail,
    } ) 

    # Container for the active workspace rail.
    active_workspace_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
        width=200,  # Sets the width
        content=active_rail,    # Sets our active rail column
    )


    return active_workspace_rail_container