import flet as ft

splitter_horizontal = ft.Draggable(
    group="splitter",
    content=ft.Container(
        height=20,
        expand=True,
    ),
    content_feedback=ft.Divider(
        height=20
    )
)
