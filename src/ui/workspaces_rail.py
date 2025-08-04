''' The master navigation bar for the 'workspaces' on the left side of the screen'''
import flet as ft
from models.user import user


# Our container that holds our all_workspaces_rail
# Its an object so we can call methods like reorder and collapse from outside of itself
class All_Workspaces_Rail(ft.Container):

    # easier sytax, grab out active story
    story = user.active_story

    # When rail is in reorderable mode, handle the reorders
    def handle_reorder(self, e: ft.OnReorderEvent):
        print(f"Reordered from {e.old_index} to {e.new_index}")

        item = self.workspaces_order.pop(e.old_index)
        self.workspaces_order.insert(e.new_index, item)
        # Update the ReorderableListView's controls
        self.all_workspaces_rail.controls = self.workspaces_order
        self.update()

    # Called by clicking button on bottom right of rail
    # Collapses or expands the rail
    def collapse_rail(self, e=None):
        print("collapse called") 

        # Disable reorder before collapsing. Phasing out later
        if self.is_reorderable:
            self.make_rail_reorderable()

        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:
            self.r0.destinations[0].label = None
            self.r1.destinations[0].label = None
            self.r2.destinations[0].label = None
            self.r3.destinations[0].label = None
            self.r4.destinations[0].label = None
            self.r5.destinations[0].label = None
            self.width = 50
            print("awrc width: ", self.width)
            self.content.controls = [
                self.all_workspaces_rail,
                ft.Container(expand=True, width=50),
                ft.IconButton(
                        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
                        on_click=self.collapse_rail,
                    ),
            ]
        else:
            self.r0.destinations[0].label = "Content"
            self.r1.destinations[0].label = "Characters"
            self.r2.destinations[0].label = "Plot & Timeline"
            self.r3.destinations[0].label = "World Building"
            self.r4.destinations[0].label = "Drawing Board"
            self.r5.destinations[0].label = "Notes"
            self.width = 130
            self.content.controls = [
                self.all_workspaces_rail,
                ft.Container(expand=True),
                ft.Row(spacing=0, controls=[
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                        on_click=self.collapse_rail,
                    ),
                ]),
            ]

            #check is reorderable or not before collapsing

        self.update()
       

    # Called by clicking button on bottom left of rail. Only available when expanded
    # Set sthe rail to reordeable or not 
    def make_rail_reorderable(self, e=None):

        # If we're collapsed, expand the rail first
        if self.is_collapsed:
            self.collapse_rail()
        
        # Change our variable
        self.is_reorderable = not self.is_reorderable

        # If reorderable, make out list a reordable list view
        if self.is_reorderable:
            print("true called")
            self.all_workspaces_rail = ft.ReorderableListView(
                on_reorder=self.handle_reorder,
                controls=self.workspaces_order,
            )
        # If not, make it a column
        else:
            print("false called")
            self.all_workspaces_rail = ft.Column(
                spacing=0, 
                alignment=ft.alignment.center,
                controls=self.workspaces_order
            )

        # Reset our columns control to apply updates
        self.content.controls[0] = self.all_workspaces_rail
        self.update()

    # Constructor
    def __init__(self, page: ft.Page):
        # Checks to see if we are reordering or collapsed
        self.is_reorderable = False
        self.is_collapsed = False

        # Method that is called whenever a new workspace is selected
        # It figures out which one was clicked, and loads the corresponding rail
        # It also updates the icon to be active, and deselects the rest
        def on_workspace_change(e):
            # controls which of our nav rails r selected and which active workspace rail we use
            rail_index : int  
            if e.control == self.r0:
                rail_index = 0  # Select our rail
            elif e.control == self.r1:
                rail_index = 1
            elif e.control == self.r2:
                rail_index = 2
            elif e.control == self.r3:
                rail_index = 3
            elif e.control == self.r4:
                rail_index = 4
            elif e.control == self.r5:
                rail_index = 5

            new_rail = user.active_story.workspace_rails.get(rail_index, user.active_story.default_rail) # Grab our active rail from dict/map
            
            deselect_all_other_rails(rail_index)    # De-select all rails icons but selected one
            user.active_story.active_rail.controls = new_rail     # Set our new rail to the active rail
            print("New workspace selected", rail_index)

            # Update our UI
            self.update()
            page.update()
          

        # Called on workspace changes. Deselects all the other rails
        def deselect_all_other_rails(rail_index):
            rail_index = rail_index
            if rail_index != 0:
                self.r0.selected_index = None
            if rail_index != 1:
                self.r1.selected_index = None
            if rail_index != 2:
                self.r2.selected_index = None
            if rail_index != 3:
                self.r3.selected_index = None
            if rail_index != 4:
                self.r4.selected_index = None
            if rail_index != 5:
                self.r5.selected_index = None

        

        # Saves our Navigation rail as their own variables rather than destinations...
        # so we can reorder them
        self.r0 = ft.NavigationRail(
            height=70,  # Set height of each rail
            on_change=on_workspace_change,  # When the rail is clicked
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.LIBRARY_BOOKS_ROUNDED, color=ft.Colors.PRIMARY), #icons
                    label="Content", padding=10,
                ),
            ],
        )
        self.r1 = ft.NavigationRail(
            height=70,
            on_change=on_workspace_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PEOPLE_OUTLINE_ROUNDED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PEOPLE_ROUNDED, color=ft.Colors.PRIMARY),
                    label="Characters", padding=6,
                ),
            ],
        )
        self.r2 = ft.NavigationRail(
            height=70,
            on_change=on_workspace_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.TIMELINE_ROUNDED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.TIMELINE_OUTLINED, color=ft.Colors.PRIMARY),
                    label="Plot & Timeline", padding=6,
                ),
            ],
        )
        self.r3 = ft.NavigationRail(
            height=70,
            on_change=on_workspace_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.PUBLIC_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.PUBLIC, color=ft.Colors.PRIMARY),
                    label="World Building", padding=6,
                ),
            ],
        )
        self.r4 = ft.NavigationRail(
            height=70,
            on_change=on_workspace_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.DRAW_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.DRAW, color=ft.Colors.PRIMARY),
                    label="Drawing Board", padding=6,
                ),
            ],
        )
        self.r5 = ft.NavigationRail(
            height=70,
            on_change=on_workspace_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.STICKY_NOTE_2_OUTLINED, color=ft.Colors.PRIMARY), 
                    selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2, color=ft.Colors.PRIMARY),
                    label="Notes", padding=6,
                ),
            ],
        )

        # This is the order of our workspace icons from top to bottom
        self.workspaces_order = [self.r0, self.r1, self.r2, self.r3, self.r4, self.r5]

        # Control that holds the workspaces. This is the main content of the object
        self.all_workspaces_rail = ft.Column(
            spacing=0, 
            alignment=ft.alignment.center,
            controls=self.workspaces_order
        )


        # Construct our rail
        super().__init__(
            alignment=ft.alignment.center,  # Aligns content to the 
            width=130,
            padding=ft.padding.only(bottom=10),
            content=ft.Column(
                alignment=ft.alignment.center,
                controls=[
                    self.all_workspaces_rail,
                    ft.Container(expand=True),
                    ft.Row(spacing=0, controls=[
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                            on_click=self.collapse_rail,
                        ),
                    ]), 
                ]
            ),
        )
        