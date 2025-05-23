''' Main productivity windows beneath the menu bar
and to the right of the navigation rail '''

import flet as ft

workspace = ft.Column(
    [
        ft.Text("Body!"),
        ft.Text("I wanne be to the right of the navbar"),
        # Add more widgets here as needed
    ],
    alignment=ft.MainAxisAlignment.START,
    expand=True,
)