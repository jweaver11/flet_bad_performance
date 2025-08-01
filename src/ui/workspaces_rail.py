''' The master navigation bar for the 'workspaces' on the left side of the screen'''
import flet as ft
from ui.active_rail import workspace_rails, default_rail, active_rail

# Creates our container that holds all our different navigational raila
def create_rails(page: ft.Page):

    is_reorderable = False  # Flag to check if we are in reorder mode
    is_collapsed = False

    # Change rail depending on which workspace is selected
    def on_workspace_change(e):
        # controls which of our nav rails r selected and which active workspace rail we use
        rail_index : int  
        if e.control == r0:
            rail_index = 0  # Select our rail
        elif e.control == r1:
            rail_index = 1
        elif e.control == r2:
            rail_index = 2
        elif e.control == r3:
            rail_index = 3
        elif e.control == r4:
            rail_index = 4
        elif e.control == r5:
            rail_index = 5

        new_rail = workspace_rails.get(rail_index, default_rail) # Grab our active rail from dict/map
        
        deselect_all_other_rails(rail_index)    # De-select all rails icons but selected one
        active_rail.controls = new_rail     # Set our new rail to the active rail
        print("New workspace selected", rail_index)

        page.update()   # update our UI
    
    # Function for deselecting all rails except the one passed through
    # Need it to change icons on the workspaces rail
    def deselect_all_other_rails(rail_index):
        rail_index = rail_index
        if rail_index != 0:
            r0.selected_index = None
        if rail_index != 1:
            r1.selected_index = None
        if rail_index != 2:
            r2.selected_index = None
        if rail_index != 3:
            r3.selected_index = None
        if rail_index != 4:
            r4.selected_index = None
        if rail_index != 5:
            r5.selected_index = None

    # Our navigation rails as their own variable so we can reorder them
    r0 = ft.NavigationRail(
        height=70,  # Set height of each rail
        on_change=on_workspace_change,  # When the rail is clicked
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.LIBRARY_BOOKS_OUTLINED, selected_icon=ft.Icons.LIBRARY_BOOKS_ROUNDED, #icons
                label="Content", padding=10,
            ),
        ],
    )
    r1 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINE_ROUNDED, selected_icon=ft.Icons.PEOPLE_ROUNDED,
                label="Characters", padding=6,
            ),
        ],
    )
    r2 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELINE_ROUNDED, selected_icon=ft.Icons.TIMELINE_OUTLINED,
                label="Plot & Timeline", padding=6,
            ),
        ],
    )
    r3 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.PUBLIC_OUTLINED, selected_icon=ft.Icons.PUBLIC,
                label="World Building", padding=6,
            ),
        ],
    )
    r4 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DRAW_OUTLINED, selected_icon=ft.Icons.DRAW,
                label="Drawing Board", padding=6,
            ),
        ],
    )
    r5 = ft.NavigationRail(
        height=70,
        on_change=on_workspace_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED, selected_icon=ft.Icon(ft.Icons.STICKY_NOTE_2),
                label="Notes", padding=6,
            ),
        ],
    )

    # List our controls so we can save re-orders
    rail_controls = [r0, r1, r2, r3, r4, r5]

    def handle_reorder(e: ft.OnReorderEvent):
        print(f"Reordered from {e.old_index} to {e.new_index}")

        item = rail_controls.pop(e.old_index)
        rail_controls.insert(e.new_index, item)
        # Update the ReorderableListView's controls
        all_workspaces_rail.controls = rail_controls
        page.update()

    all_workspaces_rail = ft.Column(
        spacing=0, 
        alignment=ft.alignment.center,
        controls=rail_controls
    )

    # Called by clicking button on bottom left of rail. Only available when expanded
    # Set sthe rail to reordeable or not 
    def make_rail_reorderable(e):
        
        nonlocal is_reorderable, all_workspaces_rail, is_collapsed

        if is_collapsed:
            return
        else:
            is_reorderable = not is_reorderable

            if is_reorderable:
                print("true called")
                all_workspaces_rail = ft.ReorderableListView(
                    on_reorder=handle_reorder,
                    controls=rail_controls,
                )
            else:
                print("false called")
                all_workspaces_rail = ft.Column(
                    spacing=0, 
                    alignment=ft.alignment.center,
                    controls=rail_controls
                )

            all_workspaces_rail_container.content.controls[0] = all_workspaces_rail
            page.update()

    # Called by clicking button on bottom right of rail
    # Collapses or expands the rail
    def collapse_rail(e):
        print("collapse called")
        nonlocal is_collapsed, is_reorderable, r0, r1, r2, r3, r4, r5

        if is_reorderable:
            make_rail_reorderable(e)

        is_collapsed = not is_collapsed

        if is_collapsed:
            r0.destinations[0].label = None
            r1.destinations[0].label = None
            r2.destinations[0].label = None
            r3.destinations[0].label = None
            r4.destinations[0].label = None
            r5.destinations[0].label = None
            all_workspaces_rail_container.width = 50
            print("awrc width: ", all_workspaces_rail_container.width)
            all_workspaces_rail_container.content.controls = [
                all_workspaces_rail,
                ft.Container(expand=True, width=50),
                ft.IconButton(
                        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
                        on_click=collapse_rail,
                    ),
            ]
        else:
            r0.destinations[0].label = "Content"
            r1.destinations[0].label = "Characters"
            r2.destinations[0].label = "Plot & Timeline"
            r3.destinations[0].label = "World Building"
            r4.destinations[0].label = "Drawing Board"
            r5.destinations[0].label = "Notes"
            all_workspaces_rail_container.width = 130
            all_workspaces_rail_container.content.controls = [
                all_workspaces_rail,
                ft.Container(expand=True),
                ft.Row(spacing=0, controls=[
                    ft.IconButton( 
                        icon=ft.Icons.REORDER_ROUNDED, 
                        on_click=make_rail_reorderable,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                        on_click=collapse_rail,
                    ),
                ]),
            ]

            #check is reorderable or not before collapsing

        
        page.update()

    
    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        width=130,
        padding=ft.padding.only(bottom=10),
        content=ft.Column(
            alignment=ft.alignment.center,
            controls=[
                all_workspaces_rail,
                ft.Container(expand=True),
                ft.Row(spacing=0, controls=[
                    ft.IconButton( 
                        icon=ft.Icons.REORDER_ROUNDED,
                        on_click=make_rail_reorderable,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
                        on_click=collapse_rail,
                    ),
                ]),
                
            ]
        ),
    )


    return all_workspaces_rail_container