''' 
Rail for the character workspace. 
Includes the filter options at the top, a list of characters, and 
the create 'character button' at the bottom.
'''

import flet as ft
from models.widgets.character import Character
from styles.menu_option_style import Menu_Option_Style
from ui.rails.rail import Rail
from models.story import Story
from handlers.tree_view import load_directory_data

class Characters_Rail(Rail):
    def __init__(self, page: ft.Page, story: Story):

        # Initialize the parent Rail class first
        super().__init__(
            page=page,
            story=story,
            directory_path=story.data['characters_directory_path']
        )

        # UI elements for easier referencing later
        self.new_character_textfield = ft.TextField(  
            hint_text="Character Name",
            data="character",
            on_submit=self.submit_item,
            on_change=self.on_new_item_change,
            on_blur=self.on_new_item_blur,
            autofocus=True,
            visible=False,
            text_style=self.text_style
        )

        # Reload the rail on start
        self.reload_rail()

    # Called when new character button or menu option is clicked
    def new_character_clicked(self, e):
        ''' Handles setting our textfield for new character creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Character Name"
        self.new_item_textfield.data = "character"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()
        

    # Called to return our list of menu options for the content rail
    def get_menu_options(self) -> list[ft.Control]:
            
        # Builds our buttons that are our options in the menu
        return [
            Menu_Option_Style(
                on_click=self.new_category_clicked,
                data="category",
                content=ft.Row([
                    ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED),
                    ft.Text("Category", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                on_click=self.new_character_clicked,
                data="character",
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_OUTLINED),
                    ft.Text("Character", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),

            # New and upload options? or just upload?? or how do i wanna do this?? Compact vs spread out view??
        ]
    
    def get_sub_menu_options(self) -> list[ft.Control]:
        return [
            Menu_Option_Style(
                data="character",
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_OUTLINED),
                    ft.Text("Character", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
        ]


    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self):

        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            
            controls=[

            # Add here, story name, and buttons to create new stuff.
            # As well as right click options here that work like normal.

            ft.Container(expand=True),

            ft.IconButton(
                tooltip="New Category",
                icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                on_click=self.new_category_clicked
            ),
            
            ft.IconButton(
                tooltip="New Character",
                icon=ft.Icons.PERSON_ADD_ALT_OUTLINED,
                on_click=self.new_character_clicked
            ),
            
            ft.Container(expand=True),
        ])
                 

        # Build the content of our rail
        content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            controls=[]
        )

        # Load our content directory data into the rail
        load_directory_data(
            page=self.p,
            story=self.story,
            directory=self.story.data['characters_directory_path'],
            column=content,
            additional_menu_options=self.get_sub_menu_options()
        )

        # Append our hidden textfield for creating new items
        content.controls.append(self.new_item_textfield)

        # Add container to the bottom to make sure the drag target and gesture detector fill the rest of the space
        content.controls.append(ft.Container(expand=True))

        # Wrap the gd in a drag target so we can move characters here
        dt = ft.DragTarget(
            group="widgets",
            content=content,     # Our content is the gesture detector
            #on_will_accept=self.story.show_pin_drag_targets,
            on_accept=lambda e: self.on_drag_accept(e, self.directory_path)
        )

        # Gesture detector to put on top of stack on the rail to pop open menus on right click
        gd = ft.GestureDetector(
            expand=True,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
            content=dt
        )

        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                header,
                ft.Divider(),
                gd
            ]
        )
        
        # Apply our update
        self.p.update()



