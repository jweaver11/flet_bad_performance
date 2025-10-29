''' 
Loads all data in a directory and adds it to expansion tiles or to rail for uniform look 
When called recursively, only the parent expansion tile argument is provided
When called initially when there is no parent dropdown, a column is provided instead
'''

import flet as ft
import os
import json
from models.story import Story
from styles.tree_view_styles import Tree_View_Directory
from styles.tree_view_styles import Tree_View_File


def load_directory_data(
    page: ft.Page,                                        # Page reference for overlays if needed    
    story: Story,                                         # Story reference for any story related data
    directory: str,                                       # The directory to load data from
    dir_dropdown: Tree_View_Directory = None,             # Optional parent expansion tile for when recursively called
    column: ft.Column = None,                             # Optional parent column to add elements too when not starting inside a tile
    # Only dir_dropdown OR column should be provided, but one is required
) -> ft.Control:
    
    def _canon_path(p: str) -> str:
        return os.path.normcase(os.path.normpath(p))
    
    # Options that all folders and files/widgets using tree view will have. Like rename, delete
    folder_options = [
        ft.TextButton(content=ft.Text("Option 1", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ft.TextButton(content=ft.Text("Option 2", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ft.TextButton(content=ft.Text("Option 3", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
    ]

    file_options = [
        ft.TextButton(content=ft.Text("Rename", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ft.TextButton(content=ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
        ft.TextButton(content=ft.Text("Option 3", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300)),
    ]

    try: 

        # Gives us a list of all files and folders in our current directory
        entrys = os.listdir(directory)

        # Keep track of directories vs files so we can add them in the order we want
        directories = []
        files = []  

        # Goes through them all
        for entry in entrys:

            # Sets the new path
            full_path =  os.path.join(directory, entry)

            # Add directories to their own list
            if os.path.isdir(full_path):
                directories.append(entry)

            # Add files to their own list
            elif os.path.isfile(full_path):
                files.append(entry)

        # Go through our directories first
        for directory_name in directories:

            # Set the path and give us the capitalized name
            full_path = os.path.join(directory, directory_name)
            capital_dir_path = directory_name.capitalize()
            
            # Build a normalized map of folder metadata once per call in order to get the call
            folders_meta = { _canon_path(k): v for k, v in story.data.get('folders', {}).items() }

            # Set our data to pass in for the folder
            color = folders_meta.get(_canon_path(full_path), {}).get('color', "primary")
            is_expanded = folders_meta.get(_canon_path(full_path), {}).get('is_expanded', False)

            # Create the expansion tile here
            new_expansion_tile = Tree_View_Directory(
                directory_path=full_path,
                title=capital_dir_path,
                story=story,
                page=page,
                color=color,
                is_expanded=is_expanded,
                father=dir_dropdown if dir_dropdown is not None else None,
            )

            # Recursively go through this directory as well to load its data, and any sub directories
            load_directory_data(
                page=page,
                story=story,
                directory=full_path,
                dir_dropdown=new_expansion_tile
            )

            # Add our expansion tile for the directory to its parent, or the column if top most directory
            if dir_dropdown is not None:
                dir_dropdown.content.controls.append(new_expansion_tile)
            else:
                column.controls.append(new_expansion_tile)

        # Now go through our files
        for file_name in files:

            # Get rid of the extension and capitalize the name
            name = os.path.splitext(file_name)[0] 
          
            # Find our widget based on the filename
            for widget in story.widgets:
                #print("Widget title check: ", widget.title, " vs ", name)
                #print("Widget dir path check: ", widget.directory_path, " vs ", os.path.join(directory))
                if widget.title == name and widget.directory_path == os.path.join(directory):  
                    #print("Passed")
                    widget = widget
                    break
                #else:
                    #print("Failed")

            # Create the file item
            item = Tree_View_File(
                widget,
                menu_options=file_options
            )        

            # Add them to parent expansion tile if one exists, otherwise just add it to the column
            if dir_dropdown is not None:
                dir_dropdown.content.controls.append(item)
            else: 
                column.controls.append(item)
            pass

        # Return the parent expansion tile or column depending on what was provided
        return dir_dropdown if dir_dropdown is not None else column
    
    # Handle errors
    except Exception as e:
        print(f"Error loading directory data from {directory}: {e}")
        return None