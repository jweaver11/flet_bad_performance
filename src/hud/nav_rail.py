import flet as ft

# Design the navigation rail on the left
rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    bgcolor=ft.Colors.TRANSPARENT,
    min_width=80,
    min_extended_width=400,
    group_alignment=-0.9,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER,
            selected_icon=ft.Icons.FAVORITE,
            label="Content",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
            selected_icon=ft.Icon(ft.Icons.BOOKMARK),
            label="Characters",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label_content=ft.Text("Timeline"),
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER,
            selected_icon=ft.Icons.FAVORITE,
            label="World Building",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.FAVORITE_BORDER,
            selected_icon=ft.Icons.FAVORITE,
            label="Drawing Board",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label_content=ft.Text("Notes"),
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index),
    trailing=ft.FloatingActionButton(
        icon=ft.Icons.CREATE, 
        text="Add Custom", 
        on_click=lambda e: print("FAB clicked!"),
        scale=.85
    ),
)




