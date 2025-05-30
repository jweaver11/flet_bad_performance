import flet as ft
from workspaces.character.character_pagelet import Character
from styles.styles import button_style
from handlers.story import story

# References for button and text field
button_ref = ft.Ref[ft.TextButton]()
textfield_ref = ft.Ref[ft.TextField]()

# Control when 'Create Character' button is clicked
def add_character_click(e):
    button_ref.current.visible = False
    button_ref.current.update()
    textfield_ref.current.visible = True
    textfield_ref.current.focus()
    textfield_ref.current.update()

# Control submits in textfield when creating character
def on_textfield_submit(e):
    name = textfield_ref.current.value
    if name:
        story.create_character(name)
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


# Function to add characters to char_rail. Returns a control. Call it through iteration of characters[]


# List of controls for the rail container
characters_rail = [

    ft.Row([
        ft.TextButton("Character 1", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
        ft.Icon(name=ft.Icons.FAVORITE)
    ]),
    ft.TextButton("Character 1", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 2", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 3", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 4", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.TextButton("Character 5", icon=ft.Icons.WAVES_OUTLINED, style=button_style),
    ft.Container(expand=True),      # Fill space until bottom of column
    ft.TextButton(  # 'Create Character button'
        "Create Character", 
        icon=ft.Icons.WAVES_OUTLINED, 
        style=button_style, 
        ref=button_ref,
        on_click=add_character_click
    ),
    ft.TextField(
        ref=textfield_ref,
        visible=False,
        hint_text="Enter Character Name",
        width=200,
        on_submit=on_textfield_submit,
        on_tap_outside=on_textfield_deselect,
    ),
]