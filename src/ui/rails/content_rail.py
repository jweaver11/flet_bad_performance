""" WIP """

import flet as ft
from models.story import Story



# Class is created in main on program startup
class Content_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__()
            
        # Page reference
        self.p = page

        # Reload the rail on start
        self.reload_rail(story)

    # Reload the rail whenever we need
    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''

        # Build the content of our rail
        self.content = ft.Column(
            controls=[
                ft.TextButton(  # 'Create Character button'
                    "Chapters", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                    on_click=lambda e: self.create_chapter("Chapter 1", story)
                ),
                ft.TextButton(  # 'Create Character button'
                    "Stuff", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                ),
                ft.TextButton(  # 'Create Character button'
                    "More stuff", 
                    icon=ft.Icons.WAVES_OUTLINED, 
                ),
                ft.Text("hi there")
            ]
        )

        # Apply our update
        self.p.update()

    # Called when user creates a new chapter
    def create_chapter(self, title: str, story: Story):
        ''' Creates a new chapter object current story '''
        
        # Pass in default path for now, but accepts new ones in future for organization
        story.create_chapter(title, directory_path=story.data['content_directory_path'])
        self.reload_rail(story)
        

