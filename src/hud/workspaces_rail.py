''' The master navigation bar for the 'workspaces' on the left side of the screen'''
import flet as ft
from hud.active_rail import workspace_rails, default_rail, active_rail
from models.story import story
from handlers.layout_widgets import stack, widget_row, pin_drag_targets


def create_rails(page: ft.Page):

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

    # Our navigation rails as their own variable for manipulation
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
                icon=ft.Icons.BUILD_OUTLINED, selected_icon=ft.Icons.BUILD_ROUNDED,
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
 

    # Sets all wrkspaces rail as a reordable list view so
    # we can drag them and re-order them
    all_workspaces_rail = ft.ReorderableListView(
        on_reorder=handle_reorder,
        controls=rail_controls,
    )

    def add_workspace(e):
        print("Add Workspace Button clicked")

    
    # Container for all available workspaces. On left most side of page
    all_workspaces_rail_container = ft.Container(
        alignment=ft.alignment.center,  # Aligns content to the 
        width=150,
        padding=ft.padding.only(bottom=10),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centers items in column
            alignment=ft.alignment.center,
            controls=[
                all_workspaces_rail,
                ft.Container(expand=True),
                ft.TextButton(
                    icon=ft.Icons.ADD_CIRCLE_ROUNDED, 
                    text="Workspace", 
                    on_click=add_workspace,
                ),
                
            ]
        ),
    )

    # Accept functions for each pin location
    def drag_accept(e):
        e.control.update()
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        #print("workspaces rail drag target accepted")

    def drag_will_accept(e):
        #print("Entered workspaces rail drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stack
        stack.update()
        page.update()

    # When a draggable leaves a target
    def on_leave(e):
        #print("Left workspaces rail target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        page.update()


    dt = ft.DragTarget(
        group="widgets", 
        content=ft.Column(expand=True, width=150), 
        on_accept=drag_accept,
        on_will_accept=drag_will_accept,
        on_leave=on_leave,
    )

    s = ft.Stack(
        controls=[all_workspaces_rail_container, dt]
    )


    return s