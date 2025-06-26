'''
Layout our widgets whenever there is more than 2
'''
import flet as ft

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

def drag_will_accept(e):
    e.control.content = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
        height=default_pin_height
    )
    e.control.update()

def on_leave(e):
    e.control.content = ft.Row(height=300)
    e.control.update()


# set minimumm fallbacks for our pins
#min_pin_height = 30
#min_pin_width = 30
default_pin_height = 200
default_pin_width = 200

min_drag_target_height = 200

top_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=top_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
left_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=left_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
main_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=main_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
right_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=right_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
bottom_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(height=200), 
    on_accept=bottom_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)


drag_targets = [
    ft.Container(
            content=top_pin_drag_target,
            height=200,
            margin=ft.margin.only(top=10, left=20, right=20),
            top=0, left=200, right=200,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=left_pin_drag_target,
            width=200,
            margin=ft.margin.only(top=10, left=10, bottom=10,),
            left=0, top=0, bottom=0,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=main_pin_drag_target,
            margin=ft.margin.only(top=20, left=20, right=20, bottom=20,),
            top=200, left=200, right=200, bottom=200,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=right_pin_drag_target,
            width=200,
            margin=ft.margin.only(top=10, right=10, bottom=10,),
            right=0, top=0, bottom=0,
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),  # Temporary for visibility
        ),
        ft.Container(
            content=bottom_pin_drag_target,
            height=200,
            bottom=0, left=200, right=200,
            margin=ft.margin.only(left=20, right=20, bottom=10),
            border_radius=ft.border_radius.all(10),  # 10px radius on all corners
            #bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        )
]


# Master row that holds all our drag targets and pins for our stack inside of workspaces
# Needs to exist here to be dynamically updated, while the pins need to be created
# when the layout is run.
widget_row = ft.Row(
    spacing=10,
    expand=True,
    controls=[]
)

default_pin_height = 200
default_pin_width = 200
    
# autopin widgets when more than 2 are active so they look nicer
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

    # Set lists for pins based off widget list?

    
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
                        ft.Container(width=10)]
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

   