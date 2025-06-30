'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.layout_widgets import stack, widget_row, pin_drag_targets


# Function to return our container for our widgets
def create_workspace(page: ft.Page, story):    

    def on_will_accept(e):
        print("Entered BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stack
        stack.update()
        page.update()

    def on_accept(e):
        print("Accepted into BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        page.update()

    def on_leave(e):
        print("Left BG drag target")
        stack.controls.clear()
        stack.controls.append(widget_row)  # Re-add the widget row to the stack
        stack.update()
        page.update()


    bg_drag_target = ft.DragTarget( # Needed to catch drags outside of pins, or program breaks
        group="widgets", 
        content=ft.Container(expand=True, bgcolor=ft.Colors.BLUE),
        on_will_accept=on_will_accept,
        on_accept=on_accept,
        #on_leave=on_leave
    )


    # Stack for adding drag target behind container to catch draggable widget errors
    s = ft.Stack(expand=True, controls=[bg_drag_target, stack])
    
    page.update()

    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        margin=ft.margin.all(10),
        #bgcolor=ft.Colors.RED,
        padding=None,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        #bgcolor=ft.Colors.GREY_800,
        content=stack
    )
    

    return s