''' The master navigation bar for the 'widgets' on the left side of the screen'''
import flet as ft
from workspaces.character.character_rail import characters_rail  
from workspaces.content.content_rail import content_rail
from workspaces.story import story


def create_rails(page: ft.Page):
    workspace_rails = {
        0: content_rail,
        1: characters_rail,
        2: characters_rail,  # Replace with actual rails as needed
        3: characters_rail,
        4: characters_rail,
        5: characters_rail,
    }

    # Change which workspace rail we'll use.
    active_workspace_rail = characters_rail # on startup init

    # Change rail depending on which workspace is selected
    def on_workspace_change(e):
        rail_index = e.control.selected_index
        temp_rail = []
        aws = active_workspace_rail

        match rail_index:
            case 0:     # on startup??
                temp_rail = content_rail
                print("new workspace selected", rail_index)
                page.update()
            case 1:
                temp_rail = characters_rail
                page.update()
            case 2:     # on startup??
                print("new workspace selected", rail_index)
                temp_rail = characters_rail
            case 3:     # on startup??
                print("new workspace selected", rail_index)
                temp_rail = characters_rail
            case 4:     # on startup??
                print("new workspace selected", rail_index)
                temp_rail = characters_rail
            case 5:     # on startup??
                print("new workspace selected", rail_index)
                temp_rail = characters_rail

            case _:     # Default/fallback
                print("new workspace selected", rail_index)
                temp_rail = characters_rail

        
        active_workspace_rail = temp_rail
        return active_workspace_rail


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
        # on_change=lambda e: print("Selected destination:", e.control.selected_index),
        on_change=on_workspace_change,
    )

    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            alignment=ft.alignment.center,
            controls=[
                ft.Text(value=story.title, size=20),
                all_workspaces_rail,
                ft.TextButton(
                    icon=ft.Icons.ADD_CIRCLE_ROUNDED, 
                    text="Add Workspace", 
                    on_click=lambda e: print("FAB clicked!"),
                ),
            ]
        ),
    )

    # Container for the select/active workspace rail.
    active_workspace_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        content=ft.Column(  # Adds rail fot he active workspace
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            # scroll=ft.ScrollMode.AUTO,
            controls=active_workspace_rail,
        ),           
    )
    return all_workspaces_rail_container, active_workspace_rail_container