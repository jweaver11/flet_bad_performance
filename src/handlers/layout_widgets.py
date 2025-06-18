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

# Row or column with a list of controls that we can add/subtract from
top_pin_controls = ft.Row(expand=True, spacing=0, controls=[])
left_pin_controls = ft.Column(expand=True, spacing=0, controls=[])
main_work_area_controls = ft.Row(spacing=4, expand=True, controls=[])
right_pin_controls = ft.Column(expand=True, spacing=0, controls=[])
bottom_pin_controls = ft.Row(expand=True, spacing=0, controls=[])

# Use reorderable list?

# Pins for when we add more and more controls
# Can hold up to 4 widgets
top_pin = ft.DragTarget(group="widgets", on_accept=top_pin_drag_accept, content=ft.Container( 
    height=100,
    border=ft.border.all(color=ft.Colors.RED_900),
    content=top_pin_controls
))
# Can hold up to 6 widgets
left_pin = ft.DragTarget(group="widgets", on_accept=left_pin_drag_accept, content=ft.Container(
    width=100,
    border=ft.border.all(color=ft.Colors.RED_900),
    content=left_pin_controls
))
# Can hold up to 4 widgets. Puts them in grid
main_work_area = ft.Container(
    expand=True,
    content=ft.DragTarget(group="widgets", on_accept=main_work_area_drag_accept, content=main_work_area_controls
))
# Can hold up to 6 widgets
right_pin = ft.DragTarget(group="widgets", on_accept=right_pin_drag_accept, content=ft.Container(
    width=100,
    border=ft.border.all(color=ft.Colors.RED_900),
    content=right_pin_controls
))
# Can hold up to 4 widgets
bottom_pin = ft.DragTarget(group="widgets", on_accept=bottom_pin_drag_accept, content=ft.Container(
    height=100,
    border=ft.border.all(color=ft.Colors.RED_900),
    content=bottom_pin_controls
))

# clears the controls so we can start fresh
def clear_all_controls():
    top_pin_controls.controls.clear()
    left_pin_controls.controls.clear()
    main_work_area_controls.controls.clear()
    right_pin_controls.controls.clear()
    bottom_pin_controls.controls.clear()

    # placeholder for empty pins, so they can still be dragged into while taking up less space
    #top_bot_placeholder = ft.Container(width=2, height=10)
    #left_right_placeholder = ft.Container(width=10, height=2)
    
    #top_pin_controls.controls.append(top_bot_placeholder)
    #left_pin_controls.controls.append(left_right_placeholder)
    #right_pin_controls.controls.append(left_right_placeholder)
    #bottom_pin_controls.controls.append(top_bot_placeholder)
    


# autopin widgets when more than 2 are active so they look nicer
def layout_widgets(widgets):

    if len(widgets) <= 0:   # If no widgets active, give it a default later
        return print("No active widgets")
    if len(widgets) >= 24:  # max num widgets
        return  print("Max num widgets reached")
    
    # Otherwise, run our layout
    clear_all_controls()
    
    # Render all widgets in same place, list up to 24 long. 
    # Fill in 'empty' slots with blank entries, but list is always 24 long
    for i in range(len(widgets) + 1):  # run through each widget and figure out where to put it
        if i==1 or i==2 or i==3 or i==4:    # First four go in the main work area
            main_work_area_controls.controls.append(widgets[i-1])
        if i == 5:
            bottom_pin_controls.controls.append(widgets[i-1])
        if i == 6:
            right_pin_controls.controls.append(widgets[i-1])
        if i == 7:
            top_pin_controls.controls.append(widgets[i-1])
        if i == 8:
            left_pin_controls.controls.append(widgets[i-1])

    
    return print(" layout widgets ran")
   