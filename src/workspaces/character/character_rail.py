''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from workspaces.character.character_styles import button_style
from models.user import user
from workspaces.character.character import Character
from handlers.render_widgets import render_widgets
from handlers.arrange_widgets import arrange_widgets

story = user.stories['empty_story']  # Get our story object from the user

def characters_rail(page: ft.Page):

    story.characters.append(Character("Bob", page))
    story.characters.append(Character("Joe", page))
    arrange_widgets()  # Arrange our characters into their pin locations
        
    # Show the widget of character. Runs when character is clicked in the rail
    def popout(e, name):
        # Show our widget
        for character in story.characters:
            if character.title == name:
                character.visible = True  # Set character visible

        render_widgets(page)
        page.update()
        
    # Rename our character
    def rename(e):
        print("pin clicked")

    # Delete our character object from the story, and its reference in its pin
    def delete(e, name):
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

    # Create a new character 
    def create_character(e, tag):
        print("create character clicked")

        # Create a reference for the dialog text field
        dialog_textfield_ref = ft.Ref[ft.TextField]()
        
        def add_character_from_dialog(e):
            name = dialog_textfield_ref.current.value  # Get name from dialog text field
            if name and name.strip():    
                # Create new character with appropriate tag
                new_character = Character(name.strip(), page)
                
                # Set the appropriate tag based on the category
                if tag == "main":
                    new_character.tags['main_character'] = True
                    new_character.tags['side_character'] = False
                    new_character.tags['background_character'] = False
                elif tag == "side":
                    new_character.tags['main_character'] = False
                    new_character.tags['side_character'] = True
                    new_character.tags['background_character'] = False
                elif tag == "background":
                    new_character.tags['main_character'] = False
                    new_character.tags['side_character'] = False
                    new_character.tags['background_character'] = True
                
                story.characters.append(new_character)
                reload_character_rail()   
                arrange_widgets() 
                render_widgets(page)  

        
                
                # Close the dialog
                dlg.open = False
                page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("Enter Character Name"), 
            content=ft.TextField(
                ref=dialog_textfield_ref,
                label="Character Name",
                hint_text="Enter character name",
                on_submit=add_character_from_dialog,  # When enter is pressed
                autofocus=True,  # Focus on this text field when dialog opens
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
                ft.TextButton("Create", on_click=add_character_from_dialog),
            ],
            on_dismiss=lambda e: print("Dialog dismissed!")
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def show_options(e):
        
        popup_button = e.control.content.content.content.controls[2]
        print(popup_button)
        popup_button.visible = True     # Show our options button
        page.update()
        print("show options called")

    def hide_options(e):
        popup_button = e.control.content.content.content.controls[2]
        popup_button.visible = False    # Hide our options button
        page.update()
        print("hide options called")

    main_characters = ft.ExpansionTile(
        title=ft.Text("Main"),
        collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
        tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
        controls_padding=None,
        shape=ft.RoundedRectangleBorder()
    )
    side_characters = ft.ExpansionTile(
        title=ft.Text("Side"),
        collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
        tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
        shape=ft.RoundedRectangleBorder()
    )
    background_characters = ft.ExpansionTile(
        title=ft.Text("Background"),
        collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
        tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
        controls_padding=None,
        shape=ft.RoundedRectangleBorder()
    )


    # Clears our re-orderable list, then re-adds every character in story.characters
    # ListTile has image, character name, popup menu options
    # Our actual list of characters, within our container
    # Each char has an image, name, and 3 dot options button
    #character_reorderable_list_container,
    def reload_character_rail():
        main_characters.controls.clear()
        side_characters.controls.clear()
        background_characters.controls.clear()
        for character in story.characters:
            new_char = ft.ListTile( # Works as a formatted row
                horizontal_spacing=0,
                expand=True,
                content_padding=None,
                title=ft.GestureDetector(
                    on_hover=show_options,  # Show our options button when hovering over character
                    on_exit=hide_options,
                    content=ft.TextButton(
                        expand=True, 
                        style=button_style,
                        on_click=lambda e, name=character.title: popout(e, name),    # on click
                        content=ft.Container(expand=True, content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text(
                                    value=character.title,
                                    color=ft.Colors.PRIMARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.CLIP,
                                    no_wrap=True,
                                ), 
                                ft.Container(expand=True,),
                                ft.PopupMenuButton(
                                    icon_color=ft.Colors.GREY_400, 
                                    tooltip="", 
                                    visible=False,
                                    items=[
                                        ft.PopupMenuItem(text="Edit", on_click=lambda e, name=character.title: popout(e, name)),
                                        ft.PopupMenuItem(text="Rename", on_click=rename),
                                        ft.PopupMenuItem(text="Delete", on_click=lambda e, name=character.title: delete(e, name)),
                                    ],
                                ),
                            ], 
                            
                        )
                ))),
        
            )

            # Format our character based on its tag
            if character.tags['main_character'] == True:
                main_characters.controls.append(new_char)
            elif character.tags['side_character'] == True:
                side_characters.controls.append(new_char)
            elif character.tags['background_character'] == True:
                background_characters.controls.append(new_char)

        # Add our 'create character' button in each category
        main_characters.controls.append(
            ft.IconButton(
                ft.Icons.ADD_ROUNDED, 
                on_click=lambda e: create_character(e, "main"),
                icon_color=ft.Colors.PRIMARY,  # Match expanded color
            )
        )
        side_characters.controls.append(
            ft.IconButton(
                ft.Icons.ADD_ROUNDED, 
                on_click=lambda e: create_character(e, "side"),
                icon_color=ft.Colors.PRIMARY,  # Match expanded color
            )
        )
        background_characters.controls.append(
            ft.IconButton(
                ft.Icons.ADD_ROUNDED, 
                on_click=lambda e: create_character(e, "background"),
                icon_color=ft.Colors.PRIMARY,  # Match expanded color
            )
        )
        return page.update()

    # List of controls that we return from our page. 
    # This is static and should not change
    characters_rail = [


        main_characters,
        side_characters,
        background_characters,

        ft.Container(expand=True),
    ]


    reload_character_rail() # called initially so characters loaded on launch
    arrange_widgets()
    render_widgets(page) 



    return characters_rail



# Make right clicking character pop open menu options
# Auto capitalize names of characters, check if name already exists before adding another