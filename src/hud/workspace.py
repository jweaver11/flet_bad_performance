'''
Just the formatting for our 'widgets' workspace area.
Returns our container with our formatting areas inside the workspace area.
Formatted areas are: top pin, left pin, main work area, right pin, and bottom pin
'''

import flet as ft
from handlers.layout_widgets import widget_row


def drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("top pin accepted")

def drag_will_accept(e):
    e.control.content = ft.Container(bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), height=default_pin_height)
    e.control.update()

def on_leave(e):
    e.control.content = ft.Row(height=300)
    e.control.update()

def left_pin_drag_accept(e):
    print("left pin accepted")
def main_work_area_drag_accept(e):
    print("main work area drag accepted")
def right_pin_drag_accept(e):
    print("right pin accepted")
def bottom_pin_drag_accept(e):
    print("bottom pin accepted")


# set minimumm fallbacks for our pins
#min_pin_height = 30
#min_pin_width = 30
default_pin_height = 200
default_pin_width = 200

top_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
left_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
main_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
right_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
bottom_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)

stack = ft.Stack(
    expand=True, 
    controls=[widget_row]
)

drag_targets = [
    ft.Container(
            content=top_pin_drag_target,
            height=200,
            top=0,
            left=200,
            right=200,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=left_pin_drag_target,
            width=200,
            left=0, top=0, bottom=0,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=main_pin_drag_target,
            top=200, left=200, right=200, bottom=200,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=right_pin_drag_target,
            width=200,
            right=0,
            top=0,
            bottom=0,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            height=200,
            bottom=0,
            left=200,
            right=200,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            content=bottom_pin_drag_target,
        )
]


# Function to return our container for our widgets
def create_workspace(page: ft.Page, story):     

    # These will be the draggable parts
    


    #stack.controls.extend(drag_targets)  # Add the drag targets to the stack

    # Container for 1 or more widgets open on the workspace area right side of screen
    workspace_container = ft.Container(
        expand=True,
        #margin=ft.margin.only(top=0, left=0, right=6, bottom=6),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        #bgcolor=ft.Colors.GREY_800,
        content=stack
    )
    
    page.update()
    

    return workspace_container