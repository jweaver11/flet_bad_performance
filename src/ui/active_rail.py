'''
UI model for our active rail, which is stored at app.active_story.active_rail
Keeps consistent styling and width between different workspace rails, 
And gives us the correct rail on startup based on selected workspace
'''

import flet as ft
from models.app import app
from models.story import Story
from ui.rails.characters_rail import create_characters_rail  
from ui.rails.content_rail import Content_Rail
from ui.rails.timeline_rail import Timeline_Rail
from ui.rails.world_building_rail import World_Building_Rail
from ui.rails.drawing_board_rail import Drawing_Board_Rail
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

        self.display_active_rail(page, story)

        
    # Called when other workspaces are selected
    def display_active_rail(self, page: ft.Page, story: Story):
        ''' Reloads the active rail based on the selected workspace in all_workspaces_rail '''

        # If no story is passed in, just load a rail prompting user to create a story
        if story is None:

            print("Warning: Story is None, cannot load active rail.")
            self.content = ft.Text("Create a story to get started!")
            self.p.update()

        # Otherwise build our active rail based on the selected workspace
        else:

            # Give us the correct rail on program startup based on our selected workspace
            if story.all_workspaces_rail.selected_rail == "content":
                self.content = Content_Rail(page, story)

            elif story.all_workspaces_rail.selected_rail == "characters":
                self.content = create_characters_rail(page)

            elif story.all_workspaces_rail.selected_rail == "timeline":
                self.content = Timeline_Rail(page, story)

            elif story.all_workspaces_rail.selected_rail == "world_building":
                self.content = World_Building_Rail(page, story)

            elif story.all_workspaces_rail.selected_rail == "drawing_board":
                self.content = Drawing_Board_Rail(page, story)

            elif story.all_workspaces_rail.selected_rail == "notes":
                self.content = create_notes_rail(page, story)

            else:
                # Default to the content rail
                self.content = Content_Rail(page, story)

            # Update the page to reflect changes
            self.p.update()
