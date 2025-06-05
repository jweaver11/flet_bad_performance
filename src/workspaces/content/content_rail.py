import flet as ft

listtile = ft.ListTile(
    title=ft.Text("Character 4"), data="Character 4",
    # on_click=add_character_click
),

content_rail = [
    ft.TextButton(  # 'Create Character button'
        "Chapters", 
        icon=ft.Icons.WAVES_OUTLINED, 
    ),
    ft.TextButton(  # 'Create Character button'
        "Stuff", 
        icon=ft.Icons.WAVES_OUTLINED, 
    ),
    ft.TextButton(  # 'Create Character button'
        "More stuff", 
        icon=ft.Icons.WAVES_OUTLINED, 
    ),
]