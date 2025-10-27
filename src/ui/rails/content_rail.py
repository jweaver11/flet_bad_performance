""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail
from styles.styles import Timeline_Expansion_Tile
import os


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
        self.reload_rail()

    # Called when creating a new note
    def submit_note(self, title: str, story: Story):
        ''' Submits our notes title to create a new note file inside our notes directory '''
        
        # Pass in default path for now, but accepts new ones in future for organization
        story.create_note(title, directory_path=story.data['notes_directory_path'])
        self.reload_rail()

    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the content rail '''

        # Depending on story type, we can have different content creation options
        # Creating a chapter for comics creates a folder to store images and drawings
        # Creating a chapter for novels creates a text document for writing, and allows

        # Add parameter to accept expansion tile
        def _load_content_directory_data(current_directory: str, parent_expansion_tile: ft.ExpansionTile=None):
            ''' Loads our content directory data for building the rail dynamically '''

            #print("Loading content directory data from: ", current_directory)

            nonlocal content 

            # Gives us a list of all files and folders in our current directory
            entrys = os.listdir(current_directory)

            # Keep track of directories vs files so we can add them in the order we want
            directories = []
            files = []  

            # Goes through them all
            for entry in entrys:

                # Sets the new path
                full_path =  os.path.join(current_directory, entry)

                # For directory names, create the expansion tile
                if os.path.isdir(full_path):

                    directories.append(entry)

                # For files, just add them to the list
                elif os.path.isfile(full_path):

                    files.append(entry)

            for directory_name in directories:

                full_path = os.path.join(current_directory, directory_name)

                # Create the expansion tile here
                new_expansion_tile = Timeline_Expansion_Tile(title=directory_name)

                # Recursively go on through
                _load_content_directory_data(
                    current_directory=full_path,
                    parent_expansion_tile=new_expansion_tile
                )

                if parent_expansion_tile is not None:
                    #parent_expansion_tile.controls.append(new_expansion_tile)
                    
                    parent_expansion_tile.controls.append(new_expansion_tile)

                else:
                    content.controls.append(new_expansion_tile)


            for file_name in files:

                # Need to get rid fof extentions for file names

                # Add them to parent expansion tile if one exists, otherwise just add it to the rail
                if parent_expansion_tile is not None:

                    parent_expansion_tile.controls.append(ft.TextButton(file_name))
                else: 
                    content.controls.append(ft.TextButton(file_name))
                pass
                

            

        # Build the content of our rail
        content = ft.Column(
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

                ft.Container(height=30)

            ]
        )

        try:

            # Load our content directory data into the rail
            _load_content_directory_data(self.story.data['content_directory_path'])

        except Exception as e:
            print(f"Error loading content directory data: {e}")

        content.controls.append(ft.Container(expand=True))

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
        

