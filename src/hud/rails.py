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
        rail_index = e.control.selected_index
        new_rail = workspace_rails.get(rail_index, content_rail) # Grab our mapped rail, default to cont rail

        # Set our new rail to the active rail
        active_rail.controls = new_rail
        print("New rail selected", rail_index)
        page.update()


    #;lakdjakfd
    # Reordable list
    #____________________________________________________________________________________________
    # Design the navigation rail on the left

    all_workspaces_rail = ft.NavigationRail(
        selected_index=0,
        expand=True,    # Fills rest of page as needed.
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TRANSPARENT,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.LIBRARY_BOOKS_OUTLINED, selected_icon=ft.Icons.LIBRARY_BOOKS_ROUNDED, #icons
                label="Content",
                padding=10,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINE_ROUNDED, selected_icon=ft.Icons.PEOPLE_ROUNDED,
                label="Characters",
                padding=6,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELINE_ROUNDED, selected_icon=ft.Icons.TIMELINE_OUTLINED,
                label_content=ft.Text("Plot & Timeline"),
                padding=6,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BUILD_OUTLINED, selected_icon=ft.Icons.BUILD_ROUNDED,
                label="World Building",
                padding=6,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.DRAW_OUTLINED, selected_icon=ft.Icons.DRAW,
                label="Drawing Board",
                padding=6,
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2),
                label_content=ft.Text("Notes"),
                padding=6,
            ),
        ],
        # Runs when new destination (workspace) is selected
        on_change=on_workspace_change
    )

    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        padding=0,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            alignment=ft.alignment.center,
            controls=[
                ft.Text(value="Workspaces", size=20, weight=ft.FontWeight.BOLD),
                all_workspaces_rail,
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