""" WIP """

import flet as ft
import os
from models.story import Story
from ui.rails.rail import Rail
from handlers.tree_view import load_directory_data


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

        # State variables used for our UI to track logic
        self.item_is_unique = True          # If the new category, chapter, note, etc. title is unique within its directory
        self.are_submitting = False         # If we are currently submitting this item

        # UI elements for easier referencing later
        self.new_chapter_textfield = ft.TextField(  
            hint_text="Chapter Name",
            data="chapter",
            on_submit=self.submit_item,
            on_change=self.on_new_item_change,
            on_blur=self.on_new_item_blur,
            autofocus=True,
            visible=False
        )

        self.new_note_textfield = ft.TextField(  
            hint_text="Note Name",
            data="note",
            on_submit=self.submit_item,
            on_change=self.on_new_item_change,
            on_blur=self.on_new_item_blur,
            autofocus=True,
            visible=False
        )

        # Reload the rail on start
        self.reload_rail()
    
    

    # Called to return our list of menu options for the content rail
    def get_menu_options(self) -> list[ft.Control]:

        # Functions to handle when one of menu options is selected
        def _new_category_clicked(e):
            
            # Makes sure the right textfield is visible and the others are hidden
            self.new_category_textfield.visible = True
            self.new_chapter_textfield.visible = False
            self.new_note_textfield.visible = False

            # Close the menu, which will update the page as well
            self.story.close_menu()

        # New chapters
        def _new_chapter_clicked(e):
            self.new_chapter_textfield.visible = True
            self.new_category_textfield.visible = False
            self.new_note_textfield.visible = False
            self.story.close_menu()
            
        # New notes
        def _new_note_clicked(e):
            self.new_note_textfield.visible = True
            self.new_category_textfield.visible = False
            self.new_chapter_textfield.visible = False
            self.story.close_menu()
            
        # Builds our buttons that are our options in the menu
        return [
            ft.TextButton(
                on_click=_new_category_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER_OPEN),
                    ft.Text("New Category"),
                ])
            ),
            ft.TextButton(
                on_click=_new_chapter_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.BOOK),
                    ft.Text("New Chapter"),
                ])
            ),
            ft.TextButton(
                on_click=_new_note_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.STICKY_NOTE_2_OUTLINED),
                    ft.Text("New Note"),
                ])
            ),

            # New and upload options? or just upload?? or how do i wanna do this?? Compact vs spread out view??
        ]

        

    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the content rail '''

        # Depending on story type, we can have different content creation options
        # Categories get colors as well??
        # Creating a chapter for comics creates a folder to store images and drawings
        # Creating a chapter for novels creates a text document for writing, and allows
        # Right clicking allows to create, upload, delete, rename
                 

        # Build the content of our rail
        content = ft.Column(
            controls=[

                # Add here, story name, and buttons to create new stuff.
                # As well as right click options here that work like normal
                
                ft.Container(height=30)
            ]
        )

        # Load our content directory data into the rail
        load_directory_data(
            page=self.p,
            story=self.story,
            directory=self.story.data['content_directory_path'],
            column=content
        )

        # Append our hiddent textfields for creating new categories, chapters, and notes
        content.controls.append(self.new_category_textfield)
        content.controls.append(self.new_chapter_textfield)
        content.controls.append(self.new_note_textfield)

        # Gesture detector to put on top of stack on the rail to pop open menus on right click
        gd = ft.GestureDetector(
            expand=True,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options())
        )

        content.controls.append(gd)

        self.content = content
        
        # Apply our update
        self.p.update()
        

