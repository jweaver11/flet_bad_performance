''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from models.user import user
from models.character import Character
from handlers.render_widgets import render_widgets
import json

story = user.active_story  # Get our story object from the user

# Called when user clicks a character on the rail, and it shows its widget
def show_character_widget(character, page: ft.Page):
    # Show our widget and update it
    character.visible = True
    page.update()

# Called when hovered over a character on the rail
# Shows our two buttons rename and delete
def show_options(e):
    e.control.content.controls[2].opacity = 1
    e.control.content.controls[2].update()

# Called when mouse leaves a character on the rail
# Hides our two buttons rename and delete
def hide_options(e):
    e.control.content.controls[2].opacity = 0
    e.control.content.controls[2].update()

# Called when user clicks rename button on the character on the rail
# Opens an alert dialog to change the characters name
def rename_character(character, page: ft.Page):
    print("rename character called")

    def rename_char(e=None):
        
        if e is not None:
            new_name = e.control.value
        else:
            new_name = dialog_textfield_ref.current.value
        dlg.open = False
        page.update()

        # Old name for snackbar alert
        old_name = character.title

        # Set our new name and update its widget to reflect the change
        character.title = new_name
        character.reload_widget()
        
        reload_character_rail(page)
        render_widgets(page)
        page.open(
            ft.SnackBar(
                bgcolor=ft.Colors.TRANSPARENT,  # Make SnackBar bg transparent
                content=ft.Container(
                    border_radius=ft.border_radius.all(6),  # Rounded corners on container
                    border=ft.border.all(2, ft.Colors.PRIMARY),  # Red border on container
                    bgcolor=ft.Colors.GREY_900,  # Background color on container
                    padding=ft.padding.all(10),  # Add padding for better appearance
                    content=ft.Text(f"{old_name} was renamed to {new_name}", color=ft.Colors.PRIMARY)
                ),   
            )
        )
        page.update()

        for char in story.characters:
            print (char.title)

    dialog_textfield_ref = ft.Ref[ft.TextField]()

    dlg = ft.AlertDialog(
        content=ft.TextField(
            ref=dialog_textfield_ref,
            label=f"{character.title}'s New Name",
            value=character.title,
            hint_text=character.title,
            on_submit=rename_char,  # When enter is pressed
            autofocus=True,  # Focus on this text field when dialog opens
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Rename", on_click=lambda e: rename_char()),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!")
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()

# Called when the 'color' button next to character on the rail is clicked
# Changed the charactesr 'color' of the background of widget and bg of rail tile
def change_character_color(character, page: ft.Page):
    print("Change character color called")

    # Does the heavy lifting to change the characters color
    def change_color():
        print("Change color called")

        color = radio_group_ref.current.value

        dlg.open = False
        page.update()
        
        character.color = color

        # Check our color and change our 'rendered_color' to match
        # rendered_color is what can be directly used by controls from the object
        if color == "red":
            character.rendered_color = ft.Colors.RED_900
        elif color == "pink":
            character.rendered_color = ft.Colors.PINK_900
        elif color == "purple":
            character.rendered_color = ft.Colors.PURPLE_900
        elif color == "blue":
            character.rendered_color = ft.Colors.BLUE_900
        elif color == "cyan":
            character.rendered_color = ft.Colors.CYAN_900
        elif color == "teal":
            character.rendered_color = ft.Colors.TEAL_900
        elif color == "green":
            character.rendered_color = ft.Colors.GREEN_900
        elif character.color == "lime":
            character.rendered_color = ft.Colors.LIME_900
        elif color == "yellow":
            character.rendered_color = ft.Colors.YELLOW_900
        elif color == "orange":
            character.rendered_color = ft.Colors.ORANGE_900
        elif color == "brown":
            character.rendered_color = ft.Colors.BROWN_900
        elif color == "light_grey":
            character.rendered_color = ft.Colors.GREY_500
        elif color == "grey":
            character.rendered_color = ft.Colors.GREY_800
        else:
            character.rendered_color = ft.Colors.TRANSPARENT
        print(character.color)
        
        
        print(f"Character color changed to: {character.color}")
        # Update the widget to reflect the changes
        character.reload_widget()
        reload_character_rail(page)

    # Reference for our radio selection of colors
    radio_group_ref = ft.Ref[ft.RadioGroup]()

    dlg = ft.AlertDialog(
        title=character.title,
        content=ft.RadioGroup(
            ref=radio_group_ref,
            content=ft.Row([
                ft.Radio(value="red", label="Red", adaptive=True),
                ft.Radio(value="pink", label="Pink", adaptive=True),
                ft.Radio(value="purple", label="Purple", adaptive=True),
                ft.Radio(value="blue", label="Blue", adaptive=True),
                ft.Radio(value="cyan", label="Cyan", adaptive=True),
                ft.Radio(value="teal", label="Teal", adaptive=True),
                ft.Radio(value="green", label="Green", adaptive=True),
                ft.Radio(value="lime", label="Lime", adaptive=True),
                ft.Radio(value="yellow", label="Yellow", adaptive=True),
                ft.Radio(value="orange", label="Orange", adaptive=True),
                ft.Radio(value="brown", label="Brown", adaptive=True),
                ft.Radio(value="light_grey", label="Light Grey", adaptive=True),
                ft.Radio(value="grey", label="Grey", adaptive=True),
                ft.Radio(value="none", label="None", adaptive=True),
            ]),
        ),
        actions=[
            # Both buttons at bottom just dismiss the popup, which runs the change_color command
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Submit", on_click=lambda e: change_color()),    
        ],
        # Whenever this is dismissed, run the change color command.
        # Since the radio will start selected with active color, this will function as a cancel button if no change to color is made
        on_dismiss=lambda e: print("dialog dismissed")
    )

    page.overlay.append(dlg)
    dlg.open = True
    page.update()


# Called when user clicks the delete button on the character on the rail
# Delete our character object from the story, and its reference in its pin
def delete_character(character, page: ft.Page):
    print("delete character called")

    # Mini function to handle closing our confirmation dialog, UI updates, and deleting the character
    def del_char(character):
        dlg.open = False
        page.update()
        story.delete_object_from_story(character)
        reload_character_rail(page)
        render_widgets(page)
        page.open(
            ft.SnackBar(
                bgcolor=ft.Colors.TRANSPARENT,  # Make SnackBar bg transparent
                content=ft.Container(
                    border_radius=ft.border_radius.all(6),  # Rounded corners on container
                    border=ft.border.all(2, ft.Colors.PRIMARY),  # Red border on container
                    bgcolor=ft.Colors.GREY_900,  # Background color on container
                    padding=ft.padding.all(10),  # Add padding for better appearance
                    content=ft.Text(f"{character.title} was deleted", color=ft.Colors.PRIMARY)
                ),   
            )
        )
        page.update()

    # Sets our title for our alert dialog
    title=f"Are you sure you want to delete {character.title} forever?"
    # Our alert dialog that pops up on screen to confirm the delete or cancel
    dlg=ft.AlertDialog(
        title=ft.Text(title), 
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Delete", on_click=lambda e: del_char(character)),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!")
    )


    # Runs to open the dialog
    page.overlay.append(dlg)
    dlg.open = True
    page.update()


# Create a new character
# Accepts a 'tag' passed through depending on which category the user is creating...
# The character from (main, side, or background)
def create_character(tag, page: ft.Page):
    print("create character clicked")

    # Create a reference for the dialog text field
    dialog_textfield_ref = ft.Ref[ft.TextField]()
    
    # Create a new character object when one of the three 'plus' buttons is clicked
    def create_new_character(e):
        name = dialog_textfield_ref.current.value  # Get name from dialog text field
        if name and name.strip() and check_character(name):   
            name = name.strip()
            name = name.capitalize()  # Auto capitalize names
            
            # temporary character object so we can check tags
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
            
            # Add our object (in this case character) to the story.
            # This story function handles pinning it and adding it to any lists
            story.add_object_to_story(new_character)
            reload_character_rail(page)   
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
            on_submit=create_new_character,  # When enter is pressed
            autofocus=True,  # Focus on this text field when dialog opens
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Create", on_click=create_new_character),
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


# Feature to change a character to main, side, or background by dragging them on the rail.
def make_main_character(e, page: ft.Page):
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

    reload_character_rail(page)  # Reload our character rail to show new character
    print("Character added to main characters")
# Side character
def make_side_character(e, page: ft.Page):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
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
    reload_character_rail(page)

# Background character
def make_background_character(e, page: ft.Page):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
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
    reload_character_rail(page)



# The 3 main categories of characters and how they will be rendered on the screen
# There list of controls are populated from our character list in the story
main_characters = ft.ExpansionTile(
    title=ft.Text("Main"),
    collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
    tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
    shape=ft.RoundedRectangleBorder(),
    controls_padding=None,
    maintain_state=True,
    initially_expanded=True,
)
side_characters = ft.ExpansionTile(
    title=ft.Text("Side"),
    collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
    tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
    shape=ft.RoundedRectangleBorder(),
    maintain_state=True,
    initially_expanded=True,
)
background_characters = ft.ExpansionTile(
    title=ft.Text("Background"),
    collapsed_icon_color=ft.Colors.PRIMARY,  # Trailing icon color when collapsed
    tile_padding=ft.padding.symmetric(horizontal=8),  # Reduce tile padding
    controls_padding=None,
    shape=ft.RoundedRectangleBorder(),
    maintain_state=True,
    initially_expanded=True,
)

# Our drag targets so we can easily drag and drop characters into their categories
# These hold the expansion tiles lists from above, and are directly rendered in the rail
main_characters_drag_target = ft.DragTarget(
    group="widgets",
    #on_accept=make_main_character,     # We set this later because we need to pass in the page
    content=main_characters
)
side_characters_drag_target = ft.DragTarget(
    group="widgets",
    #=make_side_character,  # We set this later because we need to pass in the page
    content=side_characters
)
background_characters_drag_target = ft.DragTarget(
    group="widgets",
    #on_accept=make_background_character,   # We set this later because we need to pass in the page
    content=background_characters
)

# Rebuilds our character rail from scratch whenever changes are made in data to the rail (add or del character, etc.)
# Characters are organized based on their tag of main, side, or background
# Have their colors change based on good, evil, neutral. Widget will reflect that
def reload_character_rail(page: ft.Page):
    # Clear our controls so they start fresh, doesnt effect our stored characters
    main_characters.controls.clear()
    side_characters.controls.clear()
    background_characters.controls.clear()

    # Run through each character in our story
    for character in story.characters:
        # Create a new character widget for the rail
        new_char = ft.Container(
            #border=ft.border.all(2, character.rendered_color),  # Gives a border to match the widgets border
            padding=ft.padding.only(left=4, right=4),   # padding
            margin=ft.margin.only(bottom=2),    # Margin between characters on rail
            border_radius=ft.border_radius.all(10),
            content=ft.Draggable(
            content_feedback=ft.TextButton(text=character.title),   # Feedback when dragging
            data=character,     # Pass in our character object when dragging
            group="widgets",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                expand=True,
                controls=[
                    ft.GestureDetector(
                        content=ft.Row(
                            spacing=0,
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        value=character.title,
                                        color=character.name_color,
                                        max_lines=1,    # Handle too long of names
                                        overflow=ft.TextOverflow.CLIP,  # Handle too long of names
                                        weight=ft.FontWeight.BOLD,  # Make text bold
                                        no_wrap=True,
                                    ),
                                ),
                                # Space between name of character in the rail and menu button on right
                                ft.Container(expand=True),
                                # Menu button for options to edit character in the rail
                                ft.PopupMenuButton(
                                    opacity=0,
                                    scale=.9,
                                    tooltip="",
                                    icon_color=character.name_color, 
                                    items=[
                                        # Button to rename a character
                                        ft.PopupMenuItem(
                                            icon=ft.Icons.EDIT_ROUNDED,
                                            text="Rename",
                                            # Needs to save a character reference because of pythons late binding, or this wont work
                                            on_click=lambda e, char=character: rename_character(char, page),
                                            
                                        ),
                                        # Button for changing a characters color (background of widget and rail)
                                        ft.PopupMenuItem(
                                            icon=ft.Icons.COLOR_LENS,
                                            text="Color",
                                            on_click=lambda e, char=character: change_character_color(char, page),
                                        ),
                                        # Button to delete a character
                                        ft.PopupMenuItem(  
                                            icon=ft.Icons.DELETE,
                                            text="Delete",
                                            on_click=lambda e, char=character: delete_character(char, page),
                                        ),
                                    ]
                                ),
                                
                                
                            ],
                        ),
                        #on_double_tap=lambda e, char=character: rename_character(e, char),  # Rename character on double click
                        on_hover=show_options,
                        on_exit=hide_options,
                        on_tap_down=lambda e, char=character: show_character_widget(char, page),  # Show our widget if hidden when character clicked
                        mouse_cursor=ft.MouseCursor.CLICK,      # Change our cursor to the select cursor (not working)
                        expand=True,
                    ),
                    
                ], 
            )
        )
        )
        

        # Still in for loop, add our character to category based on its tag
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
            on_click=lambda e: create_character("main", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    side_characters.controls.append(
        ft.IconButton(
            ft.Icons.ADD_ROUNDED, 
            on_click=lambda e: create_character("side", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    background_characters.controls.append(
        ft.IconButton(
            ft.Icons.ADD_ROUNDED, 
            on_click=lambda e: create_character("background", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    page.update()


def create_characters_rail(page: ft.Page):

    # Initially create some characters to test with
    story.add_object_to_story(Character("Bob", page))
    story.add_object_to_story(Character("Alice", page))
    story.add_object_to_story(Character("Joe", page))

    # Set our drag targets on accept methods here so we can pass in our page
    main_characters_drag_target.on_accept=lambda e: make_main_character(e, page)
    side_characters_drag_target.on_accept=lambda e: make_side_character(e, page)
    background_characters_drag_target.on_accept=lambda e: make_background_character(e, page)

    # List of controls that we return from our page. 
    # This is static and should not change
    characters_rail = [

        # Our drag targets that hold each character list for each category
        main_characters_drag_target,
        side_characters_drag_target,
        background_characters_drag_target,

    ]

    # Initially load our rail
    reload_character_rail(page)
    render_widgets(page) 


    return characters_rail