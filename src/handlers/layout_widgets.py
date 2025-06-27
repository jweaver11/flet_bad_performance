'''
Layout our widgets whenever there is more than 2
'''
import flet as ft


# Accept functions for each pin location
def ib_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.update()
    print("ib drag target accepted")

def ib_drag_will_accept(e):
    print("Entered ib drag target")
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stack
    stack.update()

def top_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("top pin accepted")

def left_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("left pin accepted")

def main_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("main pin accepted")

def right_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("bottom pin accepted")

# When a draggable is hovering over a target
def drag_will_accept(e):
    e.control.content = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
        height=default_pin_height
    )
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stac
    stack.update()

# When a draggable leaves a target
def on_leave(e):
    print("Left a pin drag target")
    e.control.content = ft.Row(height=300)
    e.control.update()
    stack.update()


# set minimumm fallbacks for our pins
#min_pin_height = 30
#min_pin_width = 30
default_pin_height = 200
default_pin_width = 200

min_drag_target_height = 200
min_drag_target_width = 200

# Our 5 pin area drag targets
in_between_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=ib_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)

# Pin drag targets
top_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=top_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
left_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=left_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
main_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=main_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
right_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=right_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
bottom_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=bottom_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)

# containers for our pin drag targets
pin_drag_targets = [    # Must be in flet containers in order to position them
    ft.Container(
        content=in_between_drag_target,
        expand=True,
        margin=ft.margin.all(10),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        top=0, left=0, right=0, bottom=0,
        #bgcolor=ft.Colors.RED,  # Default color for the in-between container
    ),
    ft.Container(
        content=top_pin_drag_target,
        height=200,
        margin=ft.margin.only(top=10, left=20, right=20),
        top=0, left=200, right=200,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=left_pin_drag_target,
        width=200,
        margin=ft.margin.only(top=10, left=10, bottom=10,),
        left=0, top=0, bottom=0,
        border_radius=ft.border_radius.all(10), 
    ),
    ft.Container(
        content=main_pin_drag_target,
        margin=ft.margin.only(top=20, left=20, right=20, bottom=20,),
        top=200, left=200, right=200, bottom=200,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=right_pin_drag_target,
        width=200,
        margin=ft.margin.only(top=10, right=10, bottom=10,),
        right=0, top=0, bottom=0,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=bottom_pin_drag_target,
        height=200,
        bottom=0, left=200, right=200,
        margin=ft.margin.only(left=20, right=20, bottom=10),
        border_radius=ft.border_radius.all(10), 
    ),
]

widget_row = ft.Row(
    spacing=10,
    expand=True,
    controls=[]
)
    
stack = ft.Stack(expand=True, controls=[widget_row])

# Pin our widgets in here for formatting
def layout_widgets(visible_widgets):
    widgets = visible_widgets

    if len(widgets) <= 0:   # If no widgets active, give it a default later
        # Otherwise, run our layout
        return print("No active widgets")
    if len(widgets) >= 24:  # max num widgets
        return print("Max num widgets reached")
    
    
    top_pin = ft.Row(spacing=10, controls=[])
    left_pin = ft.Column(spacing=10, controls=[])
    main_work_area = ft.Row(expand=True, spacing=10, controls=[])
    right_pin = ft.Column(spacing=10, controls=[])
    bottom_pin = ft.Row(spacing=10, controls=[])

    
    # Render all widgets in same place, list up to 24 long. 
    # Fill in 'empty' slots with blank entries, but list is always 24 long
    # Make this a switch
    for i in range(len(widgets)):  # run through each widget and figure out where to put it.

        if widgets[i] is not None:  # If the widget is not visible, skip it

            if i <= 1:    # First 2 go in the main work area
                main_work_area.controls.append(widgets[i])

            elif i == 2: 
                bottom_pin.height=default_pin_height
                bottom_pin.controls.append(
                    ft.Column(      # Adds column to keep formatting on bottom
                        expand=True, 
                        spacing=0, 
                        controls=[widgets[i], ft.Container(height=10)])
                )
            elif i == 3:
                right_pin.width=default_pin_width
                right_pin.controls.append(ft.Row(      # Adds column to keep formatting on bottom
                    expand=True, spacing=0, 
                    controls=[
                        ft.Column(expand=True, spacing=0, controls=[
                            ft.Container(height=10),
                            widgets[i],
                            ft.Container(height=10)
                            ]), 
                        ft.Column(width=10)]
                ))
            elif i == 4:
                top_pin.height=default_pin_height
                top_pin.controls.append(
                    ft.Column(      # Adds column to keep formatting on bottom
                        expand=True, 
                        spacing=0, 
                        controls=[ft.Container(height=10), widgets[i]])
                )
            elif i == 5:
                left_pin.width=default_pin_width
                left_pin.controls.append(ft.Row(      # Adds column to keep formatting on bottom
                    expand=True, spacing=0, 
                    controls=[
                        ft.Container(width=10),
                        ft.Column(expand=True, spacing=0, controls=[
                            ft.Container(height=10),
                            widgets[i],
                            ft.Container(height=10)
                            ]), 
                        ]
                ))
                        

    # Format our content
    widget_row.controls.clear()
    widget_row.controls = [
        left_pin,
        ft.Column(expand=True, spacing=10, controls=[top_pin, main_work_area, bottom_pin]),
        right_pin,
    ]


    print("layout widgets done")

   