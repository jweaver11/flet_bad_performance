''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from workspaces.character.character_styles import button_style
from models.story import story
from workspaces.character.character import Character
from handlers.render_widgets import render_widgets
from handlers.create_widget import create_widget
from handlers.arrange_widgets import arrange_widgets


def characters_rail(page: ft.Page):
    # References for button and text field
    button_ref = ft.Ref[ft.TextButton]()
    textfield_ref = ft.Ref[ft.TextField]()

    story.characters.append(Character("bob"))
    story.characters.append(Character("joe"))
    arrange_widgets()  # Arrange our characters into their pin locations
    for char in story.characters:
        if char.title == "bob":
            char.widget = create_widget(char, page)
        if char.title == "joe":
            char.widget = create_widget(char, page)
        
    # When popout is clicked
    def popout_on_click(e, name):
        # Show our widget
        for character in story.characters:
            if character.title == name:
                character.visible = True  # Set character visible

        render_widgets(page)
        page.update()
        
    # When rename is clicked
    def rename_on_click(e):
        print("pin clicked")

    # when delete is clicked. Delete our char from story obj, reload rail and widget
    def delete_on_click(e, name):
        print("delete was run")
        for character in story.characters:
            if character.title == name:
                story.characters.remove(character)  # delete from characters list
                if character in story.bottom_pin_obj:
                    story.bottom_pin_obj.remove(character)

                print(name, "was deleted")
        # del our widget
        reload_character_rail()     # Rebuild/reload our character rail
        arrange_widgets()     
        render_widgets(page)     # reload our workspace area
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
            # Add our character to our stories character list, create a widget, and add it to widget list
            c = Character(name)  # Create a new character object
            c.widget = create_widget(c, page)
            story.characters.append(c)
            reload_character_rail()   
            arrange_widgets() 
            render_widgets(page)  
            page.update()
        


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

    def handle_reorder(e: ft.OnReorderEvent):
        print("e.data:", e.data)
        print(f"Reordered from {e.old_index} to {e.new_index}")
        temp = story.characters[e.old_index]  # Get the character object at the old index
        story.characters.pop(e.old_index)  # Remove it from the old index
        story.characters.insert(e.new_index, temp)  # Insert it at the new index
        reload_character_rail()
        render_widgets(page)  # Reload the widgets to reflect the new order
        page.update()


    # Clears our re-orderable list, then re-adds every character in story.characters
    # ListTile has image, character name, popup menu options
    def reload_character_rail():
        characters_reorderable_list.controls.clear()
        for character in story.characters:
            new_char = ft.ListTile( # Works as a formatted row
                horizontal_spacing=0,
                title=ft.TextButton(
                    expand=True, 
                    style=button_style,
                    on_click=lambda e, name=character.title: print(name, "was clicked"),    # on click
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Text(
                                character.title,
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
                        ft.PopupMenuItem(text="Popout", on_click=lambda e, name=character.title: popout_on_click(e, name)),
                        ft.PopupMenuItem(text="Rename", on_click=rename_on_click),
                        ft.PopupMenuItem(text="Delete", on_click=lambda e, name=character.title: delete_on_click(e, name)),
                    ],
                ),
            )
            characters_reorderable_list.controls.append(new_char)
        return page.update()

    # Our re-orderable list. We add/delete characters to this
    characters_reorderable_list = ft.ReorderableListView(padding=0, on_reorder=handle_reorder)
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
    arrange_widgets()
    render_widgets(page) 


    return characters_rail