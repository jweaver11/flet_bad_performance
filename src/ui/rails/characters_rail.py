''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from models.app import app
from models.character import Character
from handlers.reload_workspace import reload_workspace
import json


# Called when hovered over a character on the rail
def show_options(e):
    ''' Shows our button that has the rename and delete options '''

    e.control.content.controls[2].opacity = 1
    e.control.content.controls[2].update()
    

# Called when mouse leaves a character on the rail
def hide_options(e):
    ''' Hides our button that shows rename and delete options '''

    e.control.content.controls[2].opacity = 0
    e.control.content.controls[2].update()
    

# Called when app clicks rename button on the character on the rail
def rename_character(character, page: ft.Page):
    ''' Opens a dialog to rename the character object '''

    print("rename character called")

    # Called by submitting the new name in the dialog
    def rename_char(e=None):
        ''' Handles the logic for renaming a character '''
        
        # Make sure we have a new name from the dialog, then close the dialog
        if e is not None:
            new_name = e.control.value
        else:
            new_name = dialog_textfield_ref.current.value
        dlg.open = False
        page.update()   # apply closed dialog state

        # Old name for snackbar alert
        old_name = character.title

        # Set our new name and update its widget to reflect the change
        character.title = new_name
        character.reload_widget()
        
        # Reload our character rail and widgets to reflect the changes
        reload_character_rail(page)
        reload_workspace(page)

        # Open a snackbar alert to confirm to the app that the char was renamed
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

    # Create a reference for our dialog text field
    dialog_textfield_ref = ft.Ref[ft.TextField]()

    # Define our actual alert dialog that pops up when renaming a character
    dlg = ft.AlertDialog(
        content=ft.TextField(
            ref=dialog_textfield_ref,
            label=f"{character.title}'s New Name",
            value=character.title,
            hint_text=character.title,
            on_submit=rename_char,  # When enter is pressed
            autofocus=True,  # Focus on this text field when dialog opens
        ),
        # Two action buttons in the dialog
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Rename", on_click=lambda e: rename_char()),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!")
    )

    # Adds our dialog to the page and applys the changes
    page.overlay.append(dlg)
    dlg.open = True
    page.update()

# Called when the 'color' button next to character on the rail is clicked
def change_character_color(character: Character, color, page: ft.Page):
    ''' Changes the characters tab color (not finished) '''

    #print(character.title)
    #print(color)

    #character.color = color

    reload_character_rail(page)
    character.reload_widget()
    page.update()


# Called when app clicks the delete button on the character on the rail
def delete_character(character, page: ft.Page):
    ''' Opens a dialog to confirm the deletion of the character object '''

    print("delete character called")

    # Called when app confirms the deletion of the character
    def del_char(character):
        ''' Handles the logic for deleting a character '''

        # Closes the dialog 
        dlg.open = False
        page.update()

        # Deletes the object from our live story object
        #app.active_story.delete_object(character)

        # Reloads the character rail and widgets to reflect the changes
        reload_character_rail(page)
        reload_workspace(page)

        # Open a snackbar alert to confirm to the app that the char was deleted
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


# Called when the app clicks the 'plus' buttons under either main, side, or background characters
def create_character(role_tag, page: ft.Page):
    ''' Opens a dialog to submit the name our the new character. 
    Accepts a role_tag depending on which category was clicked, and adds character to that category. '''

    print("create character clicked")


    textfield = ft.TextField(
        label="Character Name",
        hint_text="Enter character name",
        on_submit=create_new_character,  # When enter is pressed
        autofocus=True,  # Focus on this text field when dialog opens
    )
    
    # Called upon submission of the new name in the dialog to create the new character
    def create_new_character(e):
        ''' Handles the logic for creating a new character '''
        from models.story import Story

        # Grab our name from the textfield
        name = textfield.value 
        if name and name.strip() and check_character(name):   
            name = name.strip()
            name = name.capitalize()  # Auto capitalize names
            
            # Create the temporary character object so we can check tags for logic
            new_character = Character(name, page)

            # Set the appropriate tag based on the category
            if role_tag == "main":
                new_character.data["Role"] = "Main"
            elif role_tag == "side":
                new_character.data["Role"] = "Side"
            elif role_tag == "background":
                new_character.data["Role"] = "Background"

            # Adds our new character to the story
            #app.active_story.save_object(new_character)
            reload_character_rail(page)   
            reload_workspace(page)  

            # Close the dialog
            dlg.open = False
            page.update()
        else:       # When character name is empty or already exists
            dlg.open = False
            page.update()
            print("Character name is empty")
    
    # Our actual dialog that pops up when the add character button is clicked
    dlg = ft.AlertDialog(
        title=ft.Text("Enter Character Name"), 
        content=textfield,
        # Our two action buttons in the dialog
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
            ft.TextButton("Create", on_click=create_new_character),
        ],
        on_dismiss=lambda e: print("Dialog dismissed!")
    )

    # Called by out logic to check our characters name for uniqueness
    def check_character(name) -> bool:
        ''' Checks all our characters names and makes sure the name is unique '''
        '''
        for character in app.active_story.characters:
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
        '''
        return True

    # Add our dialog to the page and apply the changes
    page.overlay.append(dlg)
    dlg.open = True
    page.update()


# Called when app drags a character to a new category in the rail
def make_main_character(e, page: ft.Page):
    ''' Changes the character role to main when dragged onto rail. Phasing out.'''
    # Phasing out ^ because moving to folder storage rather than roles

    # Load our object that is passed through the event data
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
        
    # Change our character tags to reflect its new category and save the changes
    if hasattr(object, 'data'):
        object.data["Role"] = "Main"
        object.save_dict()
    else:
        print("Object does not have tags attribute, cannot change character type")

    # Reload our character rail to reflect the changes
    reload_character_rail(page) 

# Called when app drags a character to the side category in the rail
def make_side_character(e, page: ft.Page):
    ''' Changes the character role to side when dragged onto rail.'''

    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")
        
    if hasattr(object, 'data'):
        object.data["Role"] = "Side"
        object.save_dict()
    else:
        print("Object does not have tags attribute, cannot change character type")

    reload_character_rail(page)

# Called when app drags a character to the background category in the rail
def make_background_character(e, page: ft.Page):
    ''' Changes the character role to background when dragged onto rail '''

    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")
        
    if hasattr(object, 'data'):
        object.data["Role"] = "Background"
        object.save_dict()
    else:
        print("Object does not have tags attribute, cannot change character type")

    reload_character_rail(page)



# The 3 main categories of characters and how they will be rendered on the screen
# There list of controls are populated from our character list in the story
# (Phased out later for tree view, but for now this categorizes the characters)
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
    ''' Rebuilds our character rail from scratch whenever changes are made in data to the rail (add or del character, etc.)
    Will likely be phased out later when tree view is implemented, and replaces with an object '''

    # Clear our current lists so we can rebuild them
    main_characters.controls.clear()
    side_characters.controls.clear()
    background_characters.controls.clear()

    '''
    # Run through each character in our story
    for character in app.active_story.characters:
        # Create a new character tile for the rail

        new_char = ft.Draggable(
            content_feedback=ft.TextButton(text=character.title),   # Feedback when dragging
            data=character,     # Pass in our character object when dragging
            group="widgets",
            content=ft.Container(
                padding=ft.padding.only(left=4, right=4),   # padding
                margin=ft.margin.only(bottom=2),    # Margin between characters on rail
                border_radius=ft.border_radius.all(10),
                content=ft.GestureDetector(
                    #on_double_tap=lambda e, char=character: rename_character(e, char),  # Rename character on double click.. Causes other buttons to be delayed rn
                    on_hover=show_options,
                    on_exit=hide_options,
                    on_tap_down=lambda e, char=character: char.show_widget(),  # Show our widget if hidden when character clicked
                    mouse_cursor=ft.MouseCursor.CLICK,      # Change our cursor to the select cursor (not working)
                    expand=True,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    value=character.title,
                                    color=character.data['name_color'],
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
                                icon_color=character.data['name_color'], 
                                items=[
                                    # Button to rename a character
                                    ft.PopupMenuItem(
                                        icon=ft.Icons.EDIT_ROUNDED,
                                        text="Rename",
                                        # Needs to save a character reference because of pythons late binding, or this wont work
                                        on_click=lambda e, char=character: rename_character(char, page),
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
                    )
                    )
            )

        )
    '''


        
    '''
        # Still in the for loop, add our character to category based on its tag (Phased out later)
        if character.data["Role"] == "Main":
            main_characters.controls.append(new_char)
        elif character.data["Role"] == "Side":
            side_characters.controls.append(new_char)
        elif character.data["Role"] == "Background":
            background_characters.controls.append(new_char)

        # Start collapsed if no characters in that category
        if len(main_characters.controls) == 0:
            main_characters.initially_expanded=False
        else:
            main_characters.initially_expanded=True
        if len(side_characters.controls) == 0:
            side_characters.initially_expanded=False
        else:
            side_characters.initially_expanded=True
        if len(background_characters.controls) == 0:
            background_characters.initially_expanded=False
        else:
            background_characters.initially_expanded=True
    '''

    # Add our 'create character' button at bottom of each category
    main_characters.controls.append(
        ft.IconButton(
            ft.Icons.ADD_ROUNDED, 
            tooltip="Create Main Character",
            on_click=lambda e: create_character("main", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    side_characters.controls.append(
        ft.IconButton(
            ft.Icons.ADD_ROUNDED, 
            tooltip="Create Side Character",
            on_click=lambda e: create_character("side", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    background_characters.controls.append(
        ft.IconButton(
            ft.Icons.ADD_ROUNDED, 
            tooltip="Create Background Character",
            on_click=lambda e: create_character("background", page),
            icon_color=ft.Colors.PRIMARY,  # Match expanded color
        )
    )
    page.update()

# Called by main to create our container that will hold our character rail
def create_characters_rail(page: ft.Page) -> ft.Control:
    ''' Creates our character rail container that holds our character lists '''

    # Set our drag targets on accept methods here so we can pass in our page
    main_characters_drag_target.on_accept=lambda e: make_main_character(e, page)
    side_characters_drag_target.on_accept=lambda e: make_side_character(e, page)
    background_characters_drag_target.on_accept=lambda e: make_background_character(e, page)

    # List of controls that we return from our page. 
    characters_rail = ft.Column(
        spacing=0, 
        expand=True, 
        #scroll=ft.ScrollMode.AUTO, # Enable scrolling. Rn it formats to middle of rail so its disabled
        controls=[
            # Our drag targets that hold each character list for each category
            main_characters_drag_target,
            side_characters_drag_target,
            background_characters_drag_target,
        ], 
    )

    # Initially load our rail
    reload_character_rail(page)

    # Return our created character rail (which is a list of controls)
    return characters_rail