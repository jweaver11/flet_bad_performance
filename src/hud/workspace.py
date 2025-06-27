'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.layout_widgets import stack, widget_row, drag_targets


# Function to return our container for our widgets
def create_workspace(page: ft.Page, story):    

    def bg_on_will_accept(e):
        print("Entered BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.controls.extend(drag_targets)  # Add the drag targets to the stack
        stack.update()
        page.update()

    def bg_on_accept(e):
        print("Accepted into BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()

    def bg_on_leave(e):
        print("Left BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()

    bg_drag_target = ft.DragTarget( # Needed to catch drags outside of pins, or program breaks
        group="widgets", 
        content=ft.Container(expand=True, bgcolor=ft.Colors.BLUE_700), 
        on_will_accept=bg_on_will_accept,
        on_accept=bg_on_accept,
        on_leave=bg_on_leave,  # Use lambda to pass page to the
    )

    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        margin=ft.margin.all(10),
        #bgcolor=ft.Colors.RED,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        #bgcolor=ft.Colors.GREY_800,
        content=stack
    )

    # Stack for adding drag target behind container to catch draggable widget errors
    s = ft.Stack(expand=True, controls=[
        bg_drag_target, 
        workspace_container]
    )
    
    page.update()
    

    return s