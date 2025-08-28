""" WIP """

import flet as ft
from models.story import Story


def create_notes_rail(page: ft.Page, story: Story=None) -> ft.Control:

    return ft.Column(
        controls=[
            ft.Text("Notes Rail", ),
            ft.TextButton(
                "Add Note",
                icon=ft.Icons.ADD,
            ),
            ft.TextButton(
                "View Notes",
                icon=ft.Icons.VIEW_LIST,
            ),
            ft.Text("This is where you can manage your notes.")
        ]
    )