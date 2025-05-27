import flet as ft

def settings_page(page: ft.Page):

    return ft.View(
        "/settings",
        [
            ft.Text("Settings page"),
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            ft.ElevatedButton("Go to welcome", on_click=lambda _: page.go("/welcome")),
        ]
    )