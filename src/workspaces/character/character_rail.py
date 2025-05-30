import flet as ft
from workspaces.character.character_styles import button_style
from handlers.story import story

# References for button and text field
button_ref = ft.Ref[ft.TextButton]()
textfield_ref = ft.Ref[ft.TextField]()

def popout_on_click(e):
    print("popout clicked")

def pin_on_click(e):
    print("pin clicked")

def delete_on_click(e):
    print("delete clicked")


# Control when 'Create Character' button is clicked
def add_character_button_click(page, e):
    button_ref.current.visible = False
    button_ref.current.update()
    textfield_ref.current.visible = True
    textfield_ref.current.focus()
    textfield_ref.current.update()
    page.update()

# Control submits in textfield when creating character
def add_character_textfield_submit(e):
    name = textfield_ref.current.value
    if name:
        story.create_character(name)    # Add char to char list of story object
        print("added", story.character_list[-1].name, "to story object")
        characters_rail.insert(len(characters_rail) - 3, new_char)  # Add char to char rail
        print("Added ", name, "to character rail")
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


# List of controls for the rail container
characters_rail = [

    # Filter system goes here
    # Checkboxes, or Chip

    # List of characters. Shows img, char name, options button

    # Any spacers if needed
    ft.Container(expand=True),      # Fill space until bottom of column

    # add character button
    ft.TextButton(  # 'Create Character button'
        "Create Character", 
        icon=ft.Icons.WAVES_OUTLINED, 
        style=button_style, 
        ref=button_ref,
        on_click=add_character_button_click
    ),
    ft.TextField(
        ref=textfield_ref,
        visible=False,
        hint_text="Enter Character Name",
        width=200,
        on_submit=add_character_textfield_submit,
        on_tap_outside=on_textfield_deselect,
    ),
]

# Runs on app startup - adds all our characters names to the rail so we can see them
for character in story.character_list:
    new_char = ft.Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True, controls=[
        ft.Image(src=f"src/assets/icon.png", width=20, height=20),  # Add image of the character
        ft.TextButton(text=character.name, style=button_style),
        ft.PopupMenuButton(icon_color=ft.Colors.GREY_600, tooltip="", items=[
            ft.PopupMenuItem(text="popout", on_click=popout_on_click),
            ft.PopupMenuItem(text="Pin", on_click=pin_on_click),
            ft.PopupMenuItem(text="delete", on_click=delete_on_click),
            ],
        ),
    ])
    # Add our character to the rail
    characters_rail.insert(len(characters_rail) - 3, new_char)