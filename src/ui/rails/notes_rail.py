""" WIP """

import flet as ft
from models.story import Story
from models.notes import Notes


def create_notes_rail(page: ft.Page, story: Story) -> ft.Control:

    return ft.Column(
        controls=[
            ft.Text("Notes Rail"),
            ft.TextButton(
                "Add Note",
                icon=ft.Icons.ADD,
                #title="Note Title",
                on_click=lambda e: story.create_note("note_title") if story else None
            ),
            ft.TextButton(
                "View Notes",
                icon=ft.Icons.VIEW_LIST,
            ),
            ft.Text("This is where you can manage your notes.")
        ]
    )