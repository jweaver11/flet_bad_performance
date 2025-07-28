''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from workspaces.character.character_styles import button_style
from models.user import user
from models.character import Character
from handlers.render_widgets import render_widgets
from handlers.arrange_widgets import arrange_widgets
import json

story = user.active_story  # Get our story object from the user


def characters_rail(page: ft.Page):

    # Initially create some characters to test with
    story.add_object_to_story(Character("Bob", page))
    story.add_object_to_story(Character("Alice", page))
    story.add_object_to_story(Character("Joe", page))

    arrange_widgets()  # Arrange our characters into their pin locations
        
    # Show the widget of character. Runs when character is clicked in the rail
    def popout_character_widget(e, name):
        # Show our widget
        for character in story.characters:
            if character.title == name:
                character.visible = True  # Set character visible

        render_widgets(page)
        page.update()
        
    # Rename our character
    def rename_character(e):
        print("pin clicked")

    # Delete our character object from the story, and its reference in its pin
    def delete_character(e, name):
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
            if name and name.strip() and check_character(name):   
                name = name.strip()
                name = name.capitalize()  # Auto capitalize names
                
                # Create new character with appropriate tag
                new_character = Character(name, page)
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
                
                #story.characters.append(new_character)
                story.add_object_to_story(new_character)
                story.left_pin.controls.append(new_character)  # Add to left pin
                reload_character_rail()   
                arrange_widgets() 
                render_widgets(page)  

        
                # Close the dialog
                dlg.open = False
                page.update()
            else:       # When character name is empty or already exists
                dlg.open = False
                page.update()
                print("Character name is empty")
        
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

        # checks if our character name is unique
        def check_character(name):
            for character in story.characters:
                if character.title.lower() == name.lower():
                    page.open(
                        ft.SnackBar(
                            bgcolor=ft.Colors.TRANSPARENT,  # Make SnackBar bg transparent
                            content=ft.Container(
                                border_radius=ft.border_radius.all(6),  # Rounded corners on container
                                border=ft.border.all(2, ft.Colors.PRIMARY),  # Red border on container
                                bgcolor=ft.Colors.GREY_900,  # Background color on container
                                padding=ft.padding.all(10),  # Add padding for better appearance
                                content=ft.Text("Character name must be unique", color=ft.Colors.PRIMARY)
                            ),   
                        )
                    )
                    page.update()
                    return False
        
            return True

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # Shows our popupmenubutton when hovering over a character, allowing for edit, rename, and delete
    def show_options(e):
        popup_button = e.control.content.content.content.controls[2]
        print(popup_button)
        popup_button.visible = True     # Show our options button

        e.control.mouse_cursor = ft.MouseCursor.CLICK  # Change cursor to pointer (hand)
        e.control.update()

        page.update()
        print("show options called")
    # Gets rid of our popupmenubutton when mouse exits character
    def hide_options(e):
        popup_button = e.control.content.content.content.controls[2]
        popup_button.visible = False    # Hide our options button
        page.update()
        print("hide options called")

    # Quality of life feature to change a character to main, side, or background by dragging them on the rail.
    def make_main_character(e):
        # Load our object
        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        # Check if we loaded our data correctly
        if src_id:
            # Get the Draggable control by ID. our object is stored in its data
            draggable = e.page.get_control(src_id)
            if draggable:
                # Set object variable to our object
                object = draggable.data
                print("object:\n", object) 
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")
            
        # Change our character tags to reflect its new category    
        if hasattr(object, 'tags'):
            object.tags['main_character'] = True
            object.tags['side_character'] = False
            object.tags['background_character'] = False
            print(object.tags)
        else:
            print("Object does not have tags attribute, cannot change character type")

        reload_character_rail()  # Reload our character rail to show new character
        object.update()     # Reflect our changes in the widget on the right
        print("Character added to main characters")

    def make_side_character(e):
        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
                print("object:\n", object) 
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")
            
        if hasattr(object, 'tags'):
            object.tags['main_character'] = False
            object.tags['side_character'] = True
            object.tags['background_character'] = False
            print(object.tags)
        else:
            print("Object does not have tags attribute, cannot change character type")
        reload_character_rail()
        object.update()

    def make_background_character(e):
        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
                print("object:\n", object) 
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")
            
        if hasattr(object, 'tags'):
            object.tags['main_character'] = False
            object.tags['side_character'] = False
            object.tags['background_character'] = True
            print(object.tags)
        else:
            print("Object does not have tags attribute, cannot change character type")
        reload_character_rail() 
        object.update()

    # The 3 main categories of characters and how they will be rendered on the screen
    # There list of controls are populated from our character list in the story
    main_characters = ft.ExpansionTile(
        title=ft.Text("Main"),
        collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
        tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
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

    # Our drag targets so we can easily drag and drop characters into their categories
    # These hold the expansion tiles lists from above, and are directly rendered in the rail
    main_characters_drag_target = ft.DragTarget(
        group="widgets",
        on_accept=make_main_character,
        content=main_characters
    )
    side_characters_drag_target = ft.DragTarget(
        group="widgets",
        on_accept=make_side_character,
        content=side_characters
    )
    background_characters_drag_target = ft.DragTarget(
        group="widgets",
        on_accept=make_background_character,
        content=background_characters
    )

        

    # Reloads our rail when changes happen in the character data
    # Characters are organized based on their tag of main, side, or background
    # Have their colors change based on good, evil, neutral. Widget will reflect that
    def reload_character_rail():
        # Clear our controls so they start fresh, doesnt effect our stored characters
        main_characters.controls.clear()
        side_characters.controls.clear()
        background_characters.controls.clear()

        # Run through each character in our story
        for character in story.characters:
            new_char = ft.GestureDetector(
                on_hover=show_options,  # Show our options button when hovering over character
                on_exit=hide_options,
                mouse_cursor=ft.MouseCursor.CLICK,
                expand=True,
                on_tap=lambda e, name=character.title: popout_character_widget(e, name),  # on click
                content=ft.Draggable(
                    content_feedback=ft.TextButton(
                        text=character.title,
                    ), 
                    data=character,  # Data to pass when dragging
                    group="widgets",
                    content=ft.Container(
                        expand=True, 
                        content=ft.Row(
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
                                    scale=.8,
                                    items=[
                                        ft.PopupMenuItem(text="Edit", on_click=lambda e, name=character.title: popout_character_widget(e, name)),
                                        ft.PopupMenuItem(text="Rename", on_click=rename_character),
                                        ft.PopupMenuItem(text="Delete", on_click=lambda e, name=character.title: delete_character(e, name)),
                                    ],
                                ),
                            ], 
                        )
                    )
                )
            )
            

            # Add our character to category based on its tag
            if character.tags['main_character'] == True:
                main_characters.controls.append(new_char)
            elif character.tags['side_character'] == True:
                side_characters.controls.append(new_char)
            elif character.tags['background_character'] == True:
                background_characters.controls.append(new_char)

        # Add our 'create character' button at bottom of each category
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

        # Our drag targets that hold each character list for each category
        main_characters_drag_target,
        side_characters_drag_target,
        background_characters_drag_target,

    ]

    # Initially load our rail
    reload_character_rail()
    arrange_widgets()
    render_widgets(page) 


    return characters_rail