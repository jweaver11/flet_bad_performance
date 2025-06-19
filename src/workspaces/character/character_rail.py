''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from workspaces.character.character_styles import button_style
from workspaces.story import story
from handlers.reload_widgets import reload_widgets


def characters_rail(page: ft.Page):
    # References for button and text field
    button_ref = ft.Ref[ft.TextButton]()
    textfield_ref = ft.Ref[ft.TextField]()
        
    # When popout is clicked
    def popout_on_click(e):
        print("popout clicked")
    # When rename is clicked
    def rename_on_click(e):
        print("pin clicked")

    # when delete is clicked. Delete our char from story obj, reload rail and widget
    def delete_on_click(e, char):
        del story.characters[char]
        reload_character_rail()     # Rebuild/reload our character rail
        reload_widgets(story)      # reload our workspace area
        page.update()


    # Control when 'Create Character' button is clicked. Button disappears, textfield appears focused
    def create_character_button_click(e):
        button_ref.current.visible = False
        button_ref.current.update()
        textfield_ref.current.visible = True
        textfield_ref.current.focus()
        textfield_ref.current.update()

    # When user presses enter after inputting 'create_character' button
    def add_character_textfield_submit(e):
        name = textfield_ref.current.value  # Passes our character name
        if name:
            story.create_character(name)    # Add char to characters dict in story object
            reload_character_rail()    
            reload_widgets(story)   
        
        # Bring back our button, hide textfield, update the page 
        textfield_ref.current.value = ""
        textfield_ref.current.visible = False
        textfield_ref.current.update()
        button_ref.current.visible = True
        button_ref.current.update()
        page.update()

    # When textbox is clicked off and nothing in it, reset to button
    def on_textfield_deselect(e):
        name = textfield_ref.current.value
        if name == "":
            textfield_ref.current.visible = False
            button_ref.current.visible = True
            textfield_ref.current.update()
            button_ref.current.update()
        page.update()

    # Clears our re-orderable list, then re-adds every character in story.characters
    # ListTile has image, character name, popup menu options
    def reload_character_rail():
        characters_reorderable_list.controls.clear()
        for char in story.characters:
            new_char = ft.ListTile( # Works as a formatted row
                horizontal_spacing=0,
                #leading=ft.Image(src=f"src/assets/icon.png", width=20, height=20),  # Add image of the character
                title=ft.TextButton(
                    expand=True, 
                    style=button_style,
                    on_click=lambda e, char=char: print(story.characters[char].name, "was clicked"),    # on click
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Text(
                                char,
                                max_lines=1,
                                width=104,  # for when name longer than button
                                overflow=ft.TextOverflow.CLIP,
                                no_wrap=True,
                            ), 
                        ], 
                    )
                ),
                trailing=ft.PopupMenuButton(
                    icon_color=ft.Colors.GREY_400, 
                    tooltip="", 
                    items=[
                        ft.PopupMenuItem(text="Popout", on_click=popout_on_click),
                        ft.PopupMenuItem(text="Rename", on_click=rename_on_click),
                        ft.PopupMenuItem(text="Delete", on_click=lambda e, char_name=char: delete_on_click(e, char_name)),
                    ],
                ),
            )
            characters_reorderable_list.controls.append(new_char)
        return page.update()

    # Our re-orderable list. We add/delete characters to this
    characters_reorderable_list = ft.ReorderableListView(padding=0)
    # Container for formatting this list better
    character_reorderable_list_container = ft.Container(expand=True, content=characters_reorderable_list)

    # List of controls that we return from our page. 
    # This is static and should not change
    characters_rail = [

        # Filter system goes here
        # Checkboxes, or Chip
        ft.Container(
            alignment=ft.alignment.center,  # Aligns content to the
            padding=10,
            content=ft.TextButton(  # 'Create Character button'
                "Filter characters", 
                icon=ft.Icons.WAVES_OUTLINED, 
                style=button_style, 
                ref=button_ref,
            ),
        ),
        
        # Our actual list of characters, within our container
        # Each char has an image, name, and 3 dot options button
        character_reorderable_list_container,

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
                        on_click=create_character_button_click
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
    reload_character_rail() # called initially so characters loaded on launch
    reload_widgets(story) 


    return characters_rail