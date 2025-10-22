'''
UI model for our active rail, which is stored at app.active_story.active_rail
Keeps consistent styling and width between different workspace rails, 
And gives us the correct rail on startup based on selected workspace
'''

import flet as ft
from models.app import app
from models.story import Story
from ui.rails.characters_rail import Characters_Rail  
from ui.rails.content_rail import Content_Rail
from ui.rails.plotline_rail import Timeline_Rail
from ui.rails.world_building_rail import World_Building_Rail
from ui.rails.drawing_board_rail import Drawing_Board_Rail
from ui.rails.planning_rail import Planning_Rail  
from ui.rails.notes_rail import Notes_Rail


# Class is created in main on program startup
class Active_Rail(ft.Container):
    
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
    
        self.p = page  # Store the page reference
  
        # Consistent styling for all our rails
        super().__init__(
            alignment=ft.alignment.top_left,
            padding=ft.padding.only(top=10, bottom=10, left=4, right=4),
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            width=app.settings.data['active_rail_width'],  # Sets the width
        )

        # Add our 6 rails here first so they maintain consitent styling and don't have to be rebuilt on switches
        self.content_rail = Content_Rail(page, story)
        self.characters_rail = Characters_Rail(page, story)
        self.plotline_rail = Timeline_Rail(page, story)
        self.world_building_rail = World_Building_Rail(page, story)
        self.drawing_board_rail = Drawing_Board_Rail(page, story)
        self.planning_rail = Planning_Rail(page, story)
        self.notes_rail = Notes_Rail(page, story)

        # Displays our active rail on startup
        # All other rails have reload rail functions, but this one just displays the correct one
        self.display_active_rail(story)

        
    # Called when other workspaces are selected
    def display_active_rail(self, story: Story):
        ''' Reloads the active rail based on the selected workspace in workspaces_rail '''

        try:

            # Give us the correct rail based on our selected workspace
            if story.workspaces_rail.selected_rail == "content":
                self.content = self.content_rail

            elif story.workspaces_rail.selected_rail == "characters":
                self.content = self.characters_rail

            elif story.workspaces_rail.selected_rail == "plotline":
                self.content = self.plotline_rail

            elif story.workspaces_rail.selected_rail == "world_building":
                self.content = self.world_building_rail

            elif story.workspaces_rail.selected_rail == "drawing_board":
                self.content = self.drawing_board_rail

            elif story.workspaces_rail.selected_rail == "planning":
                self.content = self.planning_rail

            elif story.workspaces_rail.selected_rail == "notes":
                self.content = self.notes_rail

            else:
                # Default to the content rail
                self.content = self.content_rail

            # Update the page to reflect changes
            self.p.update()

        # Errors
        except Exception as e:
            print(f"Error displaying active rail: {e}")
