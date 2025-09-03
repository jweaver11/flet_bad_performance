'''
UI model for our active rail, which is stored at app.active_story.active_rail
Keeps consistent styling and width between different workspace rails, 
And gives us the correct rail on startup based on selected workspace
'''

import flet as ft
from models.app import app
from models.story import Story
from ui.rails.characters_rail import create_characters_rail  
from ui.rails.content_rail import create_content_rail
from ui.rails.plotline_rail import Plotline_Rail
from ui.rails.world_building_rail import create_world_building_rail
from ui.rails.drawing_board_rail import create_drawing_board_rail
from ui.rails.notes_rail import create_notes_rail


# Class is created in main on program startup
class Active_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story=None):
    
        self.p = page  # Store the page reference
  
        # Consistent styling for all our rails
        super().__init__(
            alignment=ft.alignment.center,  # Aligns content to the
            padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            width=app.settings.data['active_rail_width'],  # Sets the width
        )

        self.reload_rail(page, story)

        
    # Called when other stories are selected and we need to reload the rail
    def reload_rail(self, page: ft.Page, story: Story):
        ''' Reloads the active rail based on the selected workspace in all_workspaces_rail '''

        if story is not None:

            # Check if all_workspaces_rail is initialized yet
            if story.all_workspaces_rail is None:
                # Default to content rail if all_workspaces_rail is not yet initialized
                self.content = create_characters_rail(page)
                print("Warning: all_workspaces_rail is None, defaulting to characters rail.")
                return

            # Give us the correct rail on program startup based on our selected workspace
            if story.all_workspaces_rail.selected_rail == "content":
                self.content = create_content_rail(page)
            elif story.all_workspaces_rail.selected_rail == "characters":
                self.content = create_characters_rail(page)
            elif story.all_workspaces_rail.selected_rail == "plotline":
                story.plotline_rail = Plotline_Rail(page, story)
                self.content = story.plotline_rail
            elif story.all_workspaces_rail.selected_rail == "world_building":
                self.content = create_world_building_rail(page)
            elif story.all_workspaces_rail.selected_rail == "drawing_board":
                self.content = create_drawing_board_rail(page)
            elif story.all_workspaces_rail.selected_rail == "notes":
                self.content = create_notes_rail(page, story)
            else:
                self.content = create_characters_rail(page)

            # Update the page to reflect changes
            self.p.update()

        else:
            print("Warning: Story is None, cannot load active rail.")
            self.content = ft.Text("Create a story to get started!")
            self.p.update()



   
