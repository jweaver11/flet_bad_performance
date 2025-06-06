''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from workspaces.character.character_styles import button_style
from workspaces.story import story

# References for button and text field
button_ref = ft.Ref[ft.TextButton]()
textfield_ref = ft.Ref[ft.TextField]()
page_ref = ft.Ref[ft.Page]()

def popout_on_click(e):
    print("popout clicked")

def pin_on_click(e):
    print("pin clicked")

def delete_on_click(e):
    print("delete clicked")


# Control when 'Create Character' button is clicked
def add_character_button_click(e):
    button_ref.current.visible = False
    button_ref.current.update()
    textfield_ref.current.visible = True
    textfield_ref.current.focus()
    textfield_ref.current.update()

# Control submits in textfield when creating character
def add_character_textfield_submit(e):
    name = textfield_ref.current.value
    if name:
        story.create_character(name)    # Add char to char list of story object
        print("added", story.character_list[-1].name, "to story object")
        characters_rail.insert(len(characters_rail) - 3, name)  # Add char to char rail
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


character_list = ft.ReorderableListView(padding=0)
character_list_container = ft.Container(expand=True, content=character_list)



# List of controls for the rail container
characters_rail = [

    # Filter system goes here
    # Checkboxes, or Chip
    # add character button
    ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        padding=10,
        #expand=True,
        content=ft.TextButton(  # 'Create Character button'
            "Filter characters", 
            icon=ft.Icons.WAVES_OUTLINED, 
            style=button_style, 
            ref=button_ref,
            on_click=add_character_button_click,
        ),
    ),
    


    # List of characters are inserted here 
    # Shows image, char name, 3 dot options button
    # Either a column or some sort of list
    # Insert LV here
    character_list_container,


    # Create Character Button. Button turns into an inputtable
    # text field when clicked
    ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the
        padding=10,
        content=ft.Row(
            expand=True,
            controls=[
                ft.TextButton(  # 'Create Character button'
                    "Create Character", 
                    expand=True,
                    icon=ft.Icons.WAVES_OUTLINED, 
                    style=button_style, 
                    ref=button_ref,
                    on_click=add_character_button_click
                ),
                ft.TextField(
                    ref=textfield_ref,
                    visible=False,
                    hint_text="Enter Character Name",
                    width=184,
                    on_submit=add_character_textfield_submit,
                    on_tap_outside=on_textfield_deselect,
                ),
            ]
        )
    ),
]


# Runs on app startup - adds a tile to our character list
# Tile has image, character name, popup menu options
for character in story.character_list:
    new_char = ft.ListTile(
        horizontal_spacing=0,
        leading=ft.Image(src=f"src/assets/icon.png", width=20, height=20),  # Add image of the character
        
        title=ft.TextButton(
            expand=True, 
            style=button_style,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(
                        character.name,
                        max_lines=1,
                        width=88,
                        overflow=ft.TextOverflow.CLIP,
                        no_wrap=True,
                    ), 
                ], 
            )
        ),
        
        trailing=ft.PopupMenuButton(icon_color=ft.Colors.GREY_400, tooltip="", items=[
            ft.PopupMenuItem(text="popout", on_click=popout_on_click),
            ft.PopupMenuItem(text="Pin", on_click=pin_on_click),
            ft.PopupMenuItem(text="delete", on_click=delete_on_click),
            ],
        ),
    )
    character_list.controls.append(new_char)