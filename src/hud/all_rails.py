''' The master navigation bar for the 'workspaces' on the left side of the screen'''
import flet as ft
from workspaces.character.character_rail import characters_rail  
from workspaces.content.content_rail import content_rail
from workspaces.plot_timeline.plot_timeline_rail import plot_timeline_rail
from workspaces.world_building.world_building_rail import world_building_rail
from workspaces.drawing_board.drawing_board_rail import drawing_board_rail
from workspaces.notes.notes_rail import notes_rail
from workspaces.story import story


def create_rails(page: ft.Page):


    # Change rail depending on which workspace is selected
    def on_workspace_change(e):
        # controls which of our nav rails r selected and which active workspace rail we use
        rail_index : int  
        if e.control == r0:
            rail_index = 0  # Select our rail
        elif e.control == r1:
            rail_index = 1
        elif e.control == r2:
            rail_index = 2
        elif e.control == r3:
            rail_index = 3
        elif e.control == r4:
            rail_index = 4
        elif e.control == r5:
            rail_index = 5

        new_rail = workspace_rails.get(rail_index, content_rail) # Grab our active rail from map
        
        deselect_all_other_rails(rail_index)    # De-select all rails but selected one
        active_rail.controls = new_rail # Set our new rail to the active rail
        print("New rail selected", rail_index)

        page.update()   # update our UI
    
    # Function for deselecting all rails except the one passed through
    def deselect_all_other_rails(rail_index):
        rail_index = rail_index
        if rail_index != 0:
            r0.selected_index = None
        if rail_index != 1:
            r1.selected_index = None
        if rail_index != 2:
            r2.selected_index = None
        if rail_index != 3:
            r3.selected_index = None
        if rail_index != 4:
            r4.selected_index = None
        if rail_index != 5:
            r5.selected_index = None

    # Our navigation rails as their own variable for manipulation
    r0 = ft.NavigationRail(
        height=70,  # Set height of each rail
        on_change=on_workspace_change,  # When the rail is clicked
        selected_index=0,   # starts as selected
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.LIBRARY_BOOKS_OUTLINED, selected_icon=ft.Icons.LIBRARY_BOOKS_ROUNDED, #icons
                label="Content", padding=10,
            ),
        ],
    )
    r1 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINE_ROUNDED, selected_icon=ft.Icons.PEOPLE_ROUNDED,
                label="Characters", padding=6,
            ),
        ],
    )
    r2 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELINE_ROUNDED, selected_icon=ft.Icons.TIMELINE_OUTLINED,
                label="Plot & Timeline", padding=6,
            ),
        ],
    )
    r3 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.BUILD_OUTLINED, selected_icon=ft.Icons.BUILD_ROUNDED,
                label="World Building", padding=6,
            ),
        ],
    )
    r4 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DRAW_OUTLINED, selected_icon=ft.Icons.DRAW,
                label="Drawing Board", padding=6,
            ),
        ],
    )
    r5 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2),
                label="Notes", padding=6,
            ),
        ],
    )

    # List our controls so we can save re-orders
    rail_controls = [r0, r1, r2, r3, r4, r5]

    def handle_reorder(e: ft.OnReorderEvent):
        print(f"Reordered from {e.old_index} to {e.new_index}")

        item = rail_controls.pop(e.old_index)
        rail_controls.insert(e.new_index, item)
        # Update the ReorderableListView's controls
        all_workspaces_rail.controls = rail_controls
        page.update()
 

    # Sets all wrkspaces rail as a reordable list view so
    # we can drag them and re-order them
    all_workspaces_rail = ft.ReorderableListView(
        on_reorder=handle_reorder,
        controls=rail_controls,
    )

    def add_workspace(e):
        print("Add Workspace Button clicked")

    char_rail = characters_rail(page)

    # Map of all the workspace rails
    # Rails must be a list of controls
    workspace_rails = {
        0: content_rail,
        1: char_rail,
        2: plot_timeline_rail, 
        3: world_building_rail,
        4: drawing_board_rail,
        5: notes_rail,
    }  

    # Format our active rail
    active_rail = ft.Column(  
        spacing=0,
        controls=workspace_rails[1],    # On startup, set to char rail
    )  

    
    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        padding=0,
        width=150,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            alignment=ft.alignment.center,
            controls=[
                all_workspaces_rail,
                ft.Container(expand=True),
                ft.Container(margin=10, width=156, padding=0, alignment=ft.alignment.center, content=
                    ft.TextButton(
                        icon=ft.Icons.ADD_CIRCLE_ROUNDED, 
                        text="Add Workspace", 
                        on_click=add_workspace,
                    ),
                )
            ]
        ),
    )

    # Container for the active workspace rail.
    active_workspace_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        width=200,  # Sets the width
        content=active_rail,    # Sets our active rail column
    )


    return all_workspaces_rail_container, active_workspace_rail_container