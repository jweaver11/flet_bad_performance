''' UI model file to create our all_workspaces_rail on the left side of the screen.
This object is stored in user.all_workspaces_rail.
Handles new workspace selections, re-ordering, collapsing, and expanding the rail. '''

import flet as ft
from models.user import user
from ui.rails.characters_rail import create_characters_rail
from ui.rails.content_rail import create_content_rail
from ui.rails.plot_timeline_rail import create_plot_and_timeline_rail
from ui.rails.world_building_rail import create_world_building_rail
from ui.rails.drawing_board_rail import create_drawing_board_rail
from ui.rails.notes_rail import create_notes_rail

# Class so we can store our all workspaces rail as an object inside of user
class All_Workspaces_Rail(ft.Container):
    
    # Constructor for our all_workspaces_rail object. Needs a page reference passed in
    def __init__(self, page: ft.Page):

        self.p = page   # Page reference

        # Our variables we store in the rail object so we are not constantly reading from settings
        self.is_collapsed = user.settings.data['workspaces_rail_is_collapsed']
        self.is_reorderable = user.settings.data['workspaces_rail_is_reorderable']
        self.selected_workspace = user.settings.data['selected_workspace']

        # Saves our workspaces order, and the list we will add the controls too
        self.workspaces_order = user.settings.data['workspaces_rail_order']

        # Style our rail (container)
        super().__init__(
            alignment=ft.alignment.center,  # Aligns content to the 
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            padding=ft.padding.only(bottom=10),
        )

        # Build our rail on start
        self.reload_rail()

    # Called mostly when re-ordering or collapsing the rail. Also called on start
    def reload_rail(self):
        ''' Reloads our rail, and applies the correct styles and controls based on the state of the rail '''

        # Holds our list of controls that we will add in the rail later
        workspaces_rail = []

        # Creates our workspace selections (rails), that get added to the workspaces_rail list
        content_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,  # Make rail background transparent
            selected_index=None,    # All rails start unselected, we set the right one later
            on_change=self.on_workspace_change,  # When the rail is clicked

            destinations=[  # Each rail only has one destination
                # We do it this way so we can change the order when re-ordering the rail
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_OUTLINED, color=ft.Colors.PRIMARY), # Icon on the rail
                    selected_icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_ROUNDED, color=ft.Colors.PRIMARY), # Selected icon on the rail
                    # Label underneath the icon, padding for spacing, and the data we will use to identify the rail
                    label="Content", padding=ft.padding.only(top=10, bottom=10), data="content"
                ),
            ],
        )
        # Characters workspace rail
        characters_workspace = ft.NavigationRail(
            height=70,
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PEOPLE_OUTLINE_ROUNDED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PEOPLE_ROUNDED, color=ft.Colors.PRIMARY),
                    label="Characters", padding=ft.padding.only(top=10, bottom=10), data="characters"
                ),
            ],
        )
        # Plot and timeline workspace rail
        plot_and_timeline_workspace = ft.NavigationRail(
            height=70,  
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.TIMELINE_ROUNDED, color=ft.Colors.PRIMARY, scale=1.2), 
                    selected_icon=ft.Icon(ft.Icons.TIMELINE_OUTLINED, color=ft.Colors.PRIMARY, scale=1.2),
                    label="Plot & Timeline", padding=ft.padding.only(top=10, bottom=10), data="plot_and_timeline"
                ),
            ],
        )
        # World building workspace rail
        world_building_workspace = ft.NavigationRail(
            height=70,  
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PUBLIC_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.PRIMARY),
                    label="World Building", padding=ft.padding.only(top=10, bottom=10), data="world_building"
                ),
            ],
        )
        # Drawing board workspace rail
        drawing_board_workspace = ft.NavigationRail(
            height=70,  
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.DRAW_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.DRAW, color=ft.Colors.PRIMARY),
                    label="Drawing Board", padding=ft.padding.only(top=10, bottom=10), data="drawing_board"
                ),
            ],
        )
        # Notes workspace rail
        notes_workspace = ft.NavigationRail(
            height=70,  
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.STICKY_NOTE_2_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2, color=ft.Colors.PRIMARY),
                    label="Notes", padding=ft.padding.only(top=10, bottom=10), data="notes",
                ),
            ],
        )

        # Reads our selected workspace from ourself, and toggles the correct workspace selection icon
        if self.selected_workspace == "content":
            content_workspace.selected_index = 0    # Selects first destination in destination list (cuz there is only one)
        elif self.selected_workspace == "characters":
            characters_workspace.selected_index = 0
        elif self.selected_workspace == "plot_and_timeline":
            plot_and_timeline_workspace.selected_index = 0
        elif self.selected_workspace == "world_building":
            world_building_workspace.selected_index = 0
        elif self.selected_workspace == "drawing_board":
            drawing_board_workspace.selected_index = 0
        elif self.selected_workspace == "notes":
            notes_workspace.selected_index = 0


        # Goes through our workspace order, and adds the correct control to our list for the rail
        # We do it this way so when the user re-orders the rail, it will save their changes
        for workspace in self.workspaces_order:     # Just a list of strings
            if workspace == "content":
                workspaces_rail.append(content_workspace)   # Add our corresponding workspace selector rail to the list
            elif workspace == "characters":
                workspaces_rail.append(characters_workspace)    
            elif workspace == "plot_and_timeline":
                workspaces_rail.append(plot_and_timeline_workspace)
            elif workspace == "world_building":
                workspaces_rail.append(world_building_workspace)
            elif workspace == "drawing_board":
                workspaces_rail.append(drawing_board_workspace)
            elif workspace == "notes":
                workspaces_rail.append(notes_workspace)


        # If we're collapsed...
        if self.is_collapsed:

            self.width = 50     # Make the rail less wide
            
            # Remove our labels below the icons
            content_workspace.destinations[0].label = None 
            characters_workspace.destinations[0].label = None
            plot_and_timeline_workspace.destinations[0].label = None
            world_building_workspace.destinations[0].label = None
            drawing_board_workspace.destinations[0].label = None
            notes_workspace.destinations[0].label = None

            # Set our collapsed icon buttons icon depending on collapsed state
            collapse_icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED

        # If not collapsed, make rail normal size and set the correct icon
        else:
            self.width = 130
            collapse_icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED


        # Set our collapsed icon button using our defined icon above
        collapse_icon_button = ft.IconButton(
            icon=collapse_icon,
            on_click=self.toggle_collapse_rail,
        )

        # Sets our content as a column. This will fill our width and hold...
        # Either our list of workspaces, or a reorderable list of our workspaces
        self.content=ft.Column(
            alignment=ft.alignment.center,
            spacing=0,
        )

        # If we're reorderable, make our reorderable rail using a reorderable list
        if self.is_reorderable:
            reorderable_list = ft.ReorderableListView(
                on_reorder=self.handle_rail_reorder,
            )

            # Add our workspaces (rails) to the list. Add the list to our column
            reorderable_list.controls.extend(workspaces_rail)  
            self.content.controls.append(reorderable_list)

        # If we're not reorderable, add the selector workspaces (rails) to the column
        else:
            self.content.controls.extend(workspaces_rail) 

        # Fill in empty space under the rail, before the collapse icon button at the bottom
        self.content.controls.append(ft.Container(expand=True))

        # Add our collapse icon button to the right side of the rail
        self.content.controls.append(ft.Row(
            spacing=0, 
            controls=[
                ft.Container(expand=True),  # Fills left side of row
                collapse_icon_button,
            ]), 
        )

        self.p.update() # Update the page to show our changes

    # Called whenever we select a new workspace selector rail
    def on_workspace_change(self, e):
        ''' Changes our selected workspace in settings and for our object.
        Applies the correct active rail to match the selection '''
        
        # Save our newly selected workspace in the settings, and save it for our object
        user.settings.data['selected_workspace'] = e.control.destinations[0].data
        user.settings.save_dict()
        self.selected_workspace = user.settings.data['selected_workspace']

        # We change the active rail here rather than when we reload it because...
        # the active rail is created after this object, so if when we reload the rail...
        # on program start, it will break the program.
        if self.selected_workspace == "content":    # Set the active_rail content to the new selection
            user.active_story.active_rail.content = create_content_rail(self.p)
        elif self.selected_workspace == "characters":
            user.active_story.active_rail.content = create_characters_rail(self.p)
        elif self.selected_workspace == "plot_and_timeline":
            user.active_story.active_rail.content = create_plot_and_timeline_rail(self.p)
        elif self.selected_workspace == "world_building":
            user.active_story.active_rail.content = create_world_building_rail(self.p)
        elif self.selected_workspace == "drawing_board":
            user.active_story.active_rail.content = create_drawing_board_rail(self.p)
        elif self.selected_workspace == "notes":
            user.active_story.active_rail.content = create_notes_rail(self.p)

        self.reload_rail()  # Reload the rail to apply the new selection

    # Called by clicking button on bottom right of rail
    def toggle_collapse_rail(self, e=None):
        ''' Collapses or expands the rail, and saves the state in settings '''

        # Disable reorder before collapsing if reorder is enabled
        if self.is_reorderable:
            self.is_reorderable = False
            user.settings.data['workspaces_rail_is_reorderable'] = self.is_reorderable
            user.settings.save_dict()

        # Toggle our collapsed state
        self.is_collapsed = not self.is_collapsed
        user.settings.data['workspaces_rail_is_collapsed'] = self.is_collapsed
        user.settings.save_dict()
        
        self.reload_rail()  # Reload the rail to apply changes


    # Called by clicking re-order rail button in the settings.
    def toggle_reorder_rail(self):
        ''' Toggles the reorderable state of the rail, and saves the state in settings '''

        # If we're collapsed, expand the rail first
        if self.is_collapsed:
            self.is_collapsed = False
            user.settings.data['workspaces_rail_is_collapsed'] = self.is_collapsed
            user.settings.save_dict()

        # Toggle our reorderable state, and save it in settings
        self.is_reorderable = not self.is_reorderable
        user.settings.data['workspaces_rail_is_reorderable'] = self.is_reorderable
        user.settings.save_dict()

        self.reload_rail()  # Reload the rail to apply changes

    # Called whenever the rail is reordered
    def handle_rail_reorder(self, e: ft.OnReorderEvent):
        ''' Reorders our list based on the drag and drop, saves the new order in settings '''

        # Reorders our list based on the drag and drop
        item = self.workspaces_order.pop(e.old_index)
        self.workspaces_order.insert(e.new_index, item)
        
        # Save the new order to settings
        user.settings.data['workspaces_rail_order'] = self.workspaces_order
        user.settings.save_dict()

        self.reload_rail()  # Reload the rail to apply changes
        