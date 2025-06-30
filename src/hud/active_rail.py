import flet as ft

from workspaces.character.character_rail import characters_rail  
from workspaces.content.content_rail import content_rail
from workspaces.plot_timeline.plot_timeline_rail import plot_timeline_rail
from workspaces.world_building.world_building_rail import world_building_rail
from workspaces.drawing_board.drawing_board_rail import drawing_board_rail
from workspaces.notes.notes_rail import notes_rail
from handlers.layout_widgets import stack, widget_row, pin_drag_targets


# Default active workspace rail if none selected/on startup rn
default_rail = [ft.Text("Select a workspace")]

# Map of all the workspace rails - Rails must be a list of flet controls
workspace_rails = {
    0: default_rail,
}  

# Format our active rail 
active_rail = ft.Column(  
    spacing=0,
    controls=workspace_rails[0],    # On startup, set to char rail
)  

def create_active_rail(page: ft.Page):
    
    # Create our rails
    chars_rail = characters_rail(page)

    # Add our rails to the dict/map
    workspace_rails.update({
        0: content_rail,
        1: chars_rail,
        2: plot_timeline_rail, 
        3: world_building_rail,
        4: drawing_board_rail,
        5: notes_rail,
    })

    # Container for the active workspace rail.
    active_workspace_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        padding=ft.padding.only(top=10, bottom=10),
        width=200,  # Sets the width
        content=active_rail,    # Sets our active rail column
    )

    # Accept functions for each pin location
    def drag_accept(e):
        e.control.update()
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        #print("active rail drag target accepted")

    def drag_will_accept(e):
        #print("Entered active rail drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stack
        stack.update()
        page.open(
            ft.SnackBar(
                bgcolor=ft.Colors.GREY_900,
                duration=ft.Duration(seconds=3),
                content=ft.Text(color=ft.Colors.BLUE_200, value="Please don't drag widgets outside workspace area. You might break the program!")
            )
        )
        page.update()

    # When a draggable leaves a target
    def on_leave(e):
        #print("Left active rail target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        page.update()


    dt = ft.DragTarget(
        group="widgets", 
        content=ft.Column(expand=True, width=200), 
        on_accept=drag_accept,
        on_will_accept=drag_will_accept,
        on_leave=on_leave,
    )

    s = ft.Stack(
        controls=[active_workspace_rail_container, dt]
    )


    return s