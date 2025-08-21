import flet as ft
from models.user import user
#from ui.rails import content_rail, characters_rail, plot_and_timeline_rail, world_building_rail, drawing_board_rail, notes_rail


class All_Workspaces_Rail(ft.Container):
    def __init__(self, page: ft.Page):

        self.p = page

        # Our variables we store in the rail object so we are not constantly reading from settings
        self.is_collapsed = user.settings.data['workspaces_rail_is_collapsed']
        self.is_reorderable = user.settings.data['workspaces_rail_is_reorderable']
        self.selected_workspace = user.settings.data['selected_workspace']

        # Saves our workspaces order, and the list we will add the controls too
        self.workspaces_order = user.settings.data['workspaces_rail_order']

        # Construct our rail
        super().__init__(
            alignment=ft.alignment.center,  # Aligns content to the 
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),
            padding=ft.padding.only(bottom=10),
        )
        # Build our rail on start
        self.reload_rail()

    def reload_rail(self):
        workspaces_rail = []

        # Creates our workspace selections (rails)
        content_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,    # All rails start unselected, we set the right one later
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_ROUNDED, color=ft.Colors.PRIMARY), #icons
                    label="Content", padding=ft.padding.only(top=10, bottom=10), data="content"
                ),
            ],
        )
        characters_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PEOPLE_OUTLINE_ROUNDED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PEOPLE_ROUNDED, color=ft.Colors.PRIMARY),
                    label="Characters", padding=ft.padding.only(top=10, bottom=10), data="characters"
                ),
            ],
        )
        plot_and_timeline_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.TIMELINE_ROUNDED, color=ft.Colors.PRIMARY, scale=1.2), 
                    selected_icon=ft.Icon(ft.Icons.TIMELINE_OUTLINED, color=ft.Colors.PRIMARY, scale=1.2),
                    label="Plot & Timeline", padding=ft.padding.only(top=10, bottom=10), data="plot_and_timeline"
                ),
            ],
        )
        world_building_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PUBLIC_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.PRIMARY),
                    label="World Building", padding=ft.padding.only(top=10, bottom=10), data="world_building"
                ),
            ],
        )
        drawing_board_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.DRAW_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.DRAW, color=ft.Colors.PRIMARY),
                    label="Drawing Board", padding=ft.padding.only(top=10, bottom=10), data="drawing_board"
                ),
            ],
        )
        notes_workspace = ft.NavigationRail(
            height=70,  # Set height of each rail
            bgcolor=ft.Colors.TRANSPARENT,
            selected_index=None,
            on_change=self.on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.STICKY_NOTE_2_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2, color=ft.Colors.PRIMARY),
                    label="Notes", padding=ft.padding.only(top=10, bottom=10), data="notes",
                ),
            ],
        )

        # Reads our selected workspace, and selects the correct workspace icon
        if self.selected_workspace == "content":
            content_workspace.selected_index = 0    # Only one destination per rail, so selected = 0
            # Set the new correct active_rail 
        elif self.selected_workspace == "characters":
            characters_workspace.selected_index = 0
            #user.active_story.active_rail = user.active_story.workspace_rails[1]
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
        for workspace in self.workspaces_order:

            if workspace == "content":
                # Add the content workspace to the rail
                workspaces_rail.append(content_workspace)
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


        # If we're collapsed, make the rail smaller and get rid of labels
        if self.is_collapsed:
            self.width = 50

            content_workspace.destinations[0].label = None 
            characters_workspace.destinations[0].label = None
            plot_and_timeline_workspace.destinations[0].label = None
            world_building_workspace.destinations[0].label = None
            drawing_board_workspace.destinations[0].label = None
            notes_workspace.destinations[0].label = None

            # Set our collapsed icon buttons icon depending on collapsed state
            collapse_icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED

        # If not collapsed, make rail normal size
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

        # If we're reorderable, make our reorderable rail
        if self.is_reorderable:
            reorderable_list = ft.ReorderableListView(
                on_reorder=self.handle_rail_reorder,
            )
            # Add our workspaces (rails) to the list. Add the list to our column
            reorderable_list.controls.extend(workspaces_rail)  
            self.content.controls.append(reorderable_list)

        # If we're not reorderable, just add the workspaces (rails) to the column
        else:
            self.content.controls.extend(workspaces_rail)  # Add our workspaces rail to the content

        self.content.controls.append(ft.Container(expand=True))

        self.content.controls.append(ft.Row(
            spacing=0, 
            controls=[
                ft.Container(expand=True),
                collapse_icon_button,
            ]), 
        )

        self.p.update()

    # Called whenever we select a new workspace
    # This changes our selected workspace in settings, and selects our correct workspace icon
    def on_workspace_change(self, e):

        # Save our newly selected workspace in the settings, and save it for our object
        user.settings.data['selected_workspace'] = e.control.destinations[0].data
        user.settings.save_dict()
        self.selected_workspace = user.settings.data['selected_workspace']


        self.reload_rail()  # Reload the rail to apply the new selection

    # Called by clicking button on bottom right of rail
    # Collapses or expands the rail
    def toggle_collapse_rail(self, e=None):
        print("collapse called") 

        # Disable reorder before collapsing.
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
    # Makes our rail reorderable, and saves
    def toggle_reorder_rail(self):

        # If we're collapsed, expand the rail first
        if self.is_collapsed:
            self.is_collapsed = False
            user.settings.data['workspaces_rail_is_collapsed'] = self.is_collapsed
            user.settings.save_dict()


        self.is_reorderable = not self.is_reorderable
        user.settings.data['workspaces_rail_is_reorderable'] = self.is_reorderable
        user.settings.save_dict()

        self.reload_rail()  # Reload the rail to apply changes

    # Called whenever the rail is reordered. Saves our new order and reloads the rail
    def handle_rail_reorder(self, e: ft.OnReorderEvent):

        # Reorders our list based on the drag and drop
        item = self.workspaces_order.pop(e.old_index)
        self.workspaces_order.insert(e.new_index, item)
        
        # Save the new order to settings
        user.settings.data['workspaces_rail_order'] = self.workspaces_order
        user.settings.save_dict()

        self.reload_rail()  # Reload the rail to apply changes
        