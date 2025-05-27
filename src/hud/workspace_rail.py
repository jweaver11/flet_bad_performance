import flet as ft
from models.characters import characters  # Import the characters list

button_ref = ft.Ref[ft.ElevatedButton]()
textfield_ref = ft.Ref[ft.TextField]()

# Control when 'Create Character' button is clicked
def on_button_click(e):
    button_ref.current.visible = False
    button_ref.current.update()
    textfield_ref.current.visible = True
    textfield_ref.current.focus()
    textfield_ref.current.update()

# Control submits in textfield when creating character
def on_textfield_submit(e):
    name = textfield_ref.current.value
    if name:
        characters.append({"name": name})
        print("Added character:", name)
    textfield_ref.current.value = ""
    textfield_ref.current.visible = False
    textfield_ref.current.update()
    button_ref.current.visible = True
    button_ref.current.update()

# Rail for when the character workspace is selected
character_rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_width=100,
    min_extended_width=400,
    trailing=ft.Column([
        ft.ElevatedButton(
            "Create Character",
            ref=button_ref,
            visible=True,
            width=200,
            on_click=on_button_click
        ),
        ft.TextField(
            ref=textfield_ref,
            visible=False,
            hint_text="Enter Character Name",
            width=200,
            on_submit=on_textfield_submit
        )
    ]),
    group_alignment=0,
    destinations=[
        ft.NavigationRailDestination(label="Main Characters"),
        ft.NavigationRailDestination(label="Side Characters"),
        ft.NavigationRailDestination(label="Background Characters"),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index)
)

workspace_rail = character_rail