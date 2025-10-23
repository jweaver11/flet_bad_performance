""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail


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
        self.reload_rail(story)

    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the content rail '''

        # Depending on story type, we can have different content creation options
        # Creating a chapter for comics creates a folder to store images and drawings
        # Creating a chapter for novels creates a text document for writing, and allows

        # Build the content of our rail
        self.content = ft.Column(
            controls=[
                ft.TextButton(  # 'Create boook button'
                    "Create New Book", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                    #on_click=lambda e: self.create_chapter("Chapter 1", story)
                ),
                ft.TextButton(  # 'Create season button'
                    "Create New Season", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                    #on_click=lambda e: self.create_chapter("Chapter 1", story)
                ),
                ft.TextField(
                    label="New Chapter Title",
                    hint_text="put title here dummy",
                    on_submit=lambda e: self.submit_chapter(e.control.value, self.story)
                )
            ]
        )

        # Apply our update
        self.p.update()
        

