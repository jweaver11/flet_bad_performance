'''
Layout our widgets whenever there is more than 2
'''
import flet as ft

def top_pin_drag_accept(e):
    print("top pin accepted")
def left_pin_drag_accept(e):
    print("left pin accepted")
def main_work_area_drag_accept(e):
    print("main work area drag accepted")
def right_pin_drag_accept(e):
    print("right pin accepted")
def bottom_pin_drag_accept(e):
    print("bottom pin accepted")


top_drag_target = ft.DragTarget(content=ft.Row())
left_drag_target = ft.DragTarget(content=ft.Row())
main_drag_target = ft.DragTarget(content=ft.Row())
right_drag_target = ft.DragTarget(content=ft.Row())
bottom_drag_target = ft.DragTarget(content=ft.Row())



# Row or column with a list of controls that we can add/subtract from
top_pin = ft.Row(spacing=10, controls=[])
left_pin = ft.Column(spacing=10, controls=[])
main_work_area = ft.Row(expand=True, spacing=10, controls=[])
right_pin = ft.Column(spacing=10, controls=[])
bottom_pin = ft.Row(spacing=10, controls=[])


# set minimumm fallbacks for our pins
#min_pin_height = 30
#min_pin_width = 30
default_pin_height = 200
default_pin_width = 200


# clears the controls so we can start fresh
def clear_all_controls():
    # Clear our controls
    top_pin.controls.clear()
    left_pin.controls.clear()
    main_work_area.controls.clear()
    right_pin.controls.clear()
    bottom_pin.controls.clear()

    # format so they shrink when empty
    top_pin.expand=False
    left_pin.expand=False
    right_pin.expand=False
    bottom_pin.expand=False
    top_pin.height=False
    left_pin.width=False
    right_pin.width=False
    bottom_pin.height=False

    return print("all controls cleared")
    
    
# autopin widgets when more than 2 are active so they look nicer
def layout_widgets(widgets):

    if len(widgets) <= 0:   # If no widgets active, give it a default later
        # Otherwise, run our layout
        clear_all_controls()
        return print("No active widgets")
    if len(widgets) >= 24:  # max num widgets
        return print("Max num widgets reached")
    
    # Otherwise, run our layout
    clear_all_controls()

    
    # Render all widgets in same place, list up to 24 long. 
    # Fill in 'empty' slots with blank entries, but list is always 24 long
    # Make this a switch
    for i in range(len(widgets)):  # run through each widget and figure out where to put it.
        
        if i < 2:    # First 2 go in the main work area
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
                expand=True, 
                spacing=0, 
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
                expand=True, 
                spacing=0, 
                controls=[
                    ft.Container(width=10),
                    ft.Column(expand=True, spacing=0, controls=[
                        ft.Container(height=10),
                        widgets[i],
                        ft.Container(height=10)
                        ]), 
                    ]
            ))
    print("layout widgets done")

   