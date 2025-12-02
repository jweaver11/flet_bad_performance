""" WIP """

import flet as ft
import os
from models.story import Story
from ui.rails.rail import Rail
from handlers.tree_view import load_directory_data
from styles.menu_option_style import Menu_Option_Style


# Class is created in main on program startup
class Content_Rail(Rail):

    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Rail class first
        super().__init__(
            page=page,
            story=story,
            directory_path=story.data['content_directory_path']
        )

        # Reload the rail on start
        self.reload_rail()

    # Called when new category button is clicked
    def new_category_clicked(self, e):
        ''' Set our textfields hint text, data, value and visibility '''
        
        self.new_item_textfield.hint_text = "Category Name"
        self.new_item_textfield.data = "category"
        self.new_item_textfield.value = None
        self.new_item_textfield.visible = True

        # Close the menu, which will update the page as well
        self.story.close_menu()

    # New chapters
    def new_chapter_clicked(self, e):
        self.new_item_textfield.hint_text = "Chapter Title"
        self.new_item_textfield.data = "chapter"
        self.new_item_textfield.value = None
        self.new_item_textfield.visible = True
        self.story.close_menu()
        
    # New notes
    def new_note_clicked(self, e):
        self.new_item_textfield.hint_text = "Note Title"
        self.new_item_textfield.data = "note"
        self.new_item_textfield.value = None
        self.new_item_textfield.visible = True
        self.story.close_menu() 


    # Called to return our list of menu options for the content rail
    def get_menu_options(self) -> list[ft.Control]:
            
        # Builds our buttons that are our options in the menu
        return [
            Menu_Option_Style(
                on_click=self.new_category_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.CREATE_NEW_FOLDER_OUTLINED),
                    ft.Text("Category", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                on_click=self.new_chapter_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.NOTE_ADD_OUTLINED),
                    ft.Text("Chapter", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                on_click=self.new_note_clicked,
                content=ft.Row(expand=True, controls=[
                    ft.Icon(ft.Icons.NOTE_ALT_OUTLINED),
                    ft.Text("Note", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True)
                ])
            ),

            # New and upload options? or just upload?? or how do i wanna do this?? Compact vs spread out view??
        ]
    
    def get_directory_menu_options(self) -> list[ft.Control]:
        return [
            Menu_Option_Style(
                on_click=self.new_chapter_clicked,
                data="chapter",
                content=ft.Row([
                    ft.Icon(ft.Icons.NOTE_ADD_OUTLINED),
                    ft.Text("Chapter", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                on_click=self.new_note_clicked,
                data="note",
                content=ft.Row([
                    ft.Icon(ft.Icons.NOTE_ALT_OUTLINED),
                    ft.Text("Note", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
        ]

        

    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the content rail '''

        # Depending on story type, we can have different content creation options
        # Categories get colors as well??
        # Creating a chapter for comics creates a folder to store images and drawings
        # Creating a chapter for novels creates a text document for writing, and allows
        # Right clicking allows to upload
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
                tooltip="New Chapter",
                icon=ft.Icons.NOTE_ADD_OUTLINED,
                on_click=self.new_chapter_clicked
            ),
            ft.IconButton(
                tooltip="New Note",
                icon=ft.Icons.NOTE_ALT_OUTLINED,
                on_click=self.new_note_clicked
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
            directory=self.directory_path,
            column=content,
            additional_directory_menu_options=self.get_directory_menu_options()
        )

        content.controls.append(ft.Container(height=6))

        # Append our hiddent textfields for creating new categories, chapters, and notes
        content.controls.append(self.new_item_textfield)

        # Add container to the bottom to make sure the drag target and gesture detector fill the rest of the space
        content.controls.append(ft.Container(expand=True))


        # Wrap the gd in a drag target so we can move characters here
        dt = ft.DragTarget(
            group="widgets",
            content=content,     # Our content is the content we built above
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
        #self.content = content
        
        # Apply our update
        self.p.update()
        

