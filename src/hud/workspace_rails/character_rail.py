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

# When textbox is clicked off and nothing in it, reset to button
def on_textfield_deselect(e):
    name = textfield_ref.current.value
    if name == "":
        textfield_ref.current.visible = False
        button_ref.current.visible = True
        textfield_ref.current.update()
        button_ref.current.update()

# Rail for when the character workspace is selected
character_rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_width=70,
    min_extended_width=300,
    group_alignment=-0.9,
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
            width=150,
            on_submit=on_textfield_submit,
            on_tap_outside=on_textfield_deselect,
        )
    ]),
    destinations=[
        ft.NavigationRailDestination(
            label="Filter Characters",  # Option to filter how all characters are show below (main, side, background, good, evil, neutral)
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),  
        ft.NavigationRailDestination(
            label="Character 1", 
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),
        ft.NavigationRailDestination(
            label="Character 2", 
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),
        ft.NavigationRailDestination(
            label="Character 3",
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS)
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index)
)
