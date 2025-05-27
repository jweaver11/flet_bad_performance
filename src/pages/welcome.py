'''The welcome page for app. Will start here if user has no projects'''
import flet as ft

def welcome_page(page: ft.Page):

    return ft.View(
        "/welcome",
        [
            ft.Text("Welcome page"),
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
            ft.ElevatedButton("Go to settings", on_click=lambda _: page.go("/settings")),
        ]
    )
