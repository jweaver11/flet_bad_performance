''' 
Loads all data in a directory and adds it to expansion tiles or to rail for uniform look 
When called recursively, only the parent expansion tile argument is provided
When called initially when there is no parent dropdown, a column is provided instead
'''

import flet as ft
import os
from styles.tree_view_styles import Tree_View_Expansion_Tile
from styles.tree_view_styles import Tree_View_Item


def load_directory_data(
    directory: str,                                       # The directory to load data from
    parent_expansion_tile: ft.ExpansionTile = None,       # Optional parent expansion tile for when recursively called
    column: ft.Column = None,                             # Optional parent column to add elements too when not starting inside a tile
    # Only parent_expansion_tile OR column should be provided, but one is required
) -> ft.Control:

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

            # Create the expansion tile here
            new_expansion_tile = Tree_View_Expansion_Tile(title=capital_dir_path)

            # Recursively go through this directory as well to load its data, and any sub directories
            load_directory_data(
                directory=full_path,
                parent_expansion_tile=new_expansion_tile
            )

            # Add our expansion tile for the directory to its parent, or the column if top most directory
            if parent_expansion_tile is not None:
                parent_expansion_tile.controls.append(new_expansion_tile)
            else:
                column.controls.append(new_expansion_tile)

        # Now go through our files
        for file_name in files:
            
            # Get rid of the extension and capitalize the name
            name = os.path.splitext(file_name)[0]      
            capitalize_name = name.capitalize()

            item = Tree_View_Item(
                title=capitalize_name,
                on_exit=lambda e: print(f"exited hover over {capitalize_name}"),
            )        

            # Add them to parent expansion tile if one exists, otherwise just add it to the column
            if parent_expansion_tile is not None:
                parent_expansion_tile.controls.append(item)
            else: 
                column.controls.append(item)
            pass

        # Return the parent expansion tile or column depending on what was provided
        return parent_expansion_tile if parent_expansion_tile is not None else column
    
    # Handle errors
    except Exception as e:
        print(f"Error loading directory data from {directory}: {e}")
        return None