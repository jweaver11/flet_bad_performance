''' The master navigation bar for the 'widgets' on the left side of the screen'''
import flet as ft

# Design the navigation rail on the left
all_workspaces_rail = ft.NavigationRail(
    selected_index=0,
    expand=True,
    label_type=ft.NavigationRailLabelType.ALL,
    bgcolor=ft.Colors.TRANSPARENT,
    min_width=80,
    min_extended_width=400,
    group_alignment=-0.9,
    leading=ft.FloatingActionButton(
        icon=ft.Icons.CREATE, 
        text="Project name", 
        on_click=lambda e: print("FAB clicked!"),
        scale=.85
    ),
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, #icons
            label="Content",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.BOOKMARK_BORDER), selected_icon=ft.Icon(ft.Icons.BOOKMARK),
            label="Characters",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label_content=ft.Text("Plot & Timeline"),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE,
            label="World Building",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE,
            label="Drawing Board",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label_content=ft.Text("Notes"),
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index),
    trailing=ft.FloatingActionButton(
        icon=ft.Icons.CREATE, 
        text="Add Workspace (premade)", 
        on_click=lambda e: print("FAB clicked!"),
        scale=.85
    ),
)