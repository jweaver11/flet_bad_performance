""" WIP """

import flet as ft
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
            story=story
        )

        # Reload the rail on start
        self.reload_rail()

    def create_new_book(self, title: str, story: Story):
        # TODO: Make it accept the type of story to give a structure for new books, seasons, etc.
        pass

    def create_new_season(self, title: str, story: Story):
        pass

    # Called when user creates a new chapter
    def submit_chapter(self, title: str, story: Story):
        ''' Grabs our story.type object and creates a new chapter directory inside it.
         Chapter directory can contain images, notes, and the text content for the chapter itself '''
        
        # Pass in default path for now, but accepts new ones in future for organization
        story.create_chapter(title, directory_path=story.data['content_directory_path'])

    # Called when creating a new note
    def submit_note(self, title: str, story: Story):
        ''' Submits our notes title to create a new note file inside our notes directory '''
        
        # Pass in default path for now, but accepts new ones in future for organization
        story.create_note(title, directory_path=story.data['notes_directory_path'])

    def open_menu(self, e):
            
        #print(f"Open menu at x={story.mouse_x}, y={story.mouse_y}")

        def close_menu(e):
            self.p.overlay.clear()
            self.p.update()
        
        menu = ft.Container(
            left=self.story.mouse_x,     # Positions the menu at the mouse location
            top=self.story.mouse_y,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.Colors.ON_SECONDARY,
            padding=2,
            alignment=ft.alignment.center,
            content=ft.Column([
                ft.TextButton("Option 1"),
                ft.TextButton("Option 2"),
                ft.TextButton("Option 3"),
            ]),
        )
        outside_detector = ft.GestureDetector(
            expand=True,
            on_tap=close_menu,
            on_secondary_tap=close_menu,
        )

        self.p.overlay.append(outside_detector)
        self.p.overlay.append(menu)
        
        self.p.update()

    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the content rail '''

        # Depending on story type, we can have different content creation options
        # Categories get colors as well??
        # Creating a chapter for comics creates a folder to store images and drawings
        # Creating a chapter for novels creates a text document for writing, and allows
        # Right clicking allows to create, upload, delete, rename
        # -- Create allows new categories (One folder), books/seasons (multiple folders), chapter, note, drawing, etc.
        
        # Drag a file/category to move it into another folder/category
        # -- Needs to highlight the category its hovering above
                 

        # Build the content of our rail
        content = ft.Column(
            controls=[
                ft.TextButton(  # 'Create boook button'
                    "Create New Book", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                ),
                ft.TextButton(  # 'Create season button'
                    "Create New Season", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                ),
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

        # Gesture detector to put on top of stack on the rail to pop open menus on right click
        gd = ft.GestureDetector(
            expand=True,
            on_secondary_tap=self.open_menu,
        )

        content.controls.append(gd)

        content.controls.append(
            ft.TextField(
                label="New Chapter Title",
                hint_text="put title here dummy",
                on_submit=lambda e: self.submit_chapter(e.control.value, self.story)
            )
        )

        content.controls.append(
            ft.TextField(
                label="New Note Title",
                hint_text="put title here dummy",
                on_submit=lambda e: self.submit_note(e.control.value, self.story)
            )
        )

        self.content = content

        
        # Apply our update
        self.p.update()
        

