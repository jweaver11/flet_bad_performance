''' The master navigation bar for the 'widgets' on the left side of the screen'''
import flet as ft
from workspaces.character.character_rail import characters_rail  

# Change which workspace rail we'll use.
active_workspace_rail = characters_rail

def on_workspace_change(index):
    print("new workspace selected", index)

# Design the navigation rail on the left
all_workspaces_rail = ft.NavigationRail(
    selected_index=0,
    expand=True,
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