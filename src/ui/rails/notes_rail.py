""" WIP """

import flet as ft
from models.story import Story
from models.notes import Notes


def create_notes_rail(page: ft.Page, story: Story=None) -> ft.Control:

    return ft.Column(
        controls=[
            ft.Text("Notes Rail", ),
            ft.TextButton(
                "Add Note",
                icon=ft.Icons.ADD,
                on_click=lambda e: story.create_note() if story else None
                #url_target="",
            ),
            ft.TextButton(
                "View Notes",
                icon=ft.Icons.VIEW_LIST,
                #on_click=lambda e: story.load_from_dict() if story else None
            ),
            ft.Text("This is where you can manage your notes.")
        ]
    )