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
    story = user.active_story

    def show_horizontal_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Method called when our divider (inside a gesture detector) is dragged
    # Updates the size of our pin in the story object
    def move_top_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_y > 0 and story.top_pin.height < page.height/2) or (e.delta_y < 0 and story.top_pin.height > 100):
            story.top_pin.height += e.delta_y
        active_workspace_rail_container.update()
        story.widgets.update() # Update the main pin, as it is affected by all pins resizing
        story.master_stack.update()

    # The control that holds our divider, which we drag to resize the top pin
    rail_resizer = ft.GestureDetector(
        content=ft.VerticalDivider(color=ft.Colors.TRANSPARENT, width=6, thickness=10),
        on_pan_update=move_top_pin_divider,
        on_hover=show_horizontal_cursor,
    )
    
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
        width=200,  # Sets the width
        content=user.active_story.active_rail,  # Sets our active rail column
        #ft.Row(
            #expand=True,
            #spacing=0,
            #controls=[
                #user.active_story.active_rail,    # Sets our active rail column
                #rail_resizer,
            #]
        #)
    )


    return active_workspace_rail_container
