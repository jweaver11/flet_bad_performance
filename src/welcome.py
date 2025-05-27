'''The welcome page for app. Will start here if user has no projects'''
import flet as ft


def create_welcome_page(page: ft.Page):
    
    page.title = "Basic outlined buttons"

    outlined_button = ft.OutlinedButton(
        text="Outlined button",
        on_click=lambda e: print("Outlined button clicked!"),
    )
    page.add(
        ft.OutlinedButton(text="Outlined button"),
        ft.OutlinedButton("Disabled button", disabled=True),
    )
    
    hello = ft.Text("Hello, World!")
    page.add(hello)
    print(hello in page)  # True