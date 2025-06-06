''' The master navigation bar for the 'widgets' on the left side of the screen'''
import flet as ft
from workspaces.character.character_rail import characters_rail  
from workspaces.content.content_rail import content_rail
from workspaces.story import story


def create_rails(page: ft.Page):

    # Map of all the workspace rails
    # Rails must be a list of controls that use containers for spacing
    workspace_rails = {
        0: content_rail,
        1: characters_rail,
        2: content_rail,  # Replace with actual rails as needed
        3: characters_rail,
        4: content_rail,
        5: characters_rail,
    }  

    # Sets our active rail as a column for page updates
    active_rail = ft.Column(  # Adds rail for he active workspace
        spacing=0,
        # horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
        # scroll=ft.ScrollMode.AUTO,
        controls=workspace_rails[1],    # On startup, set to char rail
    )       


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

        # Turn off all other rails
        deselect_all_other_rails(rail_index)
        new_rail = workspace_rails.get(rail_index, content_rail) # Grab our mapped rail, default to cont rail
        # Set our new rail to the active rail
        active_rail.controls = new_rail
        print("New rail selected", rail_index)
        page.update()

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
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TRANSPARENT,
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
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TRANSPARENT,
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
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TRANSPARENT,
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
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TRANSPARENT,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2),
                label="Notes", padding=6,
            ),
        ],
    )
    

    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        padding=0,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            alignment=ft.alignment.center,
            controls=[
                r0, # Add all our rail elements
                r1,
                r2,
                r3,
                r4,
                r5,
                ft.Container(expand=True),
                ft.Container(margin=10, width=156, padding=0, alignment=ft.alignment.center, content=
                    ft.TextButton(
                        icon=ft.Icons.ADD_CIRCLE_ROUNDED, 
                        text="Add Workspace", 
                        on_click=lambda e: print("FAB clicked!"),
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