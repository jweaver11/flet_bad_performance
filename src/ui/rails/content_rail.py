""" WIP """

import flet as ft
from models.story import Story



# Class is created in main on program startup
class Content_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__()
            
        self.p = page

        self.reload_rail(story)

    # Reload the rail whenever we need
    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''


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
        self.p.update()



    def create_chapter(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''

        
        # default path for now
        if story is not None:
            story.create_chapter(title, file_path=story.data['content_directory_path'])
            self.reload_rail(story)
        else:
            print("No story selected, how u hit dis button dumbo??")

