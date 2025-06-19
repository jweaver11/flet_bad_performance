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
top_pin_widgets = ft.Row(expand=True, spacing=0, controls=[])
left_pin_widgets = ft.Column(expand=True, spacing=0, controls=[])
main_work_area_widgets = ft.Row(expand=True, spacing=4, controls=[])
right_pin_widgets = ft.Column(expand=True, spacing=0, controls=[])
bottom_pin_widgets = ft.Row(expand=True, spacing=0, controls=[])


# set minimumm fallbacks for our pins
min_pin_height = 30
min_pin_width = 30
max_pin_width = 300
#default?


# Pins for when we add more and more controls
# Can hold up to 4 widgets
top_pin = ft.Container(
    content=ft.DragTarget(group="widgets", on_accept=top_pin_drag_accept, content=top_pin_widgets
))
# Can hold up to 6 widgets
left_pin = ft.Container(
    content=ft.DragTarget(group="widgets", on_accept=left_pin_drag_accept, content=left_pin_widgets
))

# Can hold up to 2 widgets. Go side by side
main_work_area = ft.Container(
    expand=True,
    content=ft.DragTarget(
        group="widgets", 
        on_accept=main_work_area_drag_accept,
        content=main_work_area_widgets, 
))


# Can hold up to 6 widgets
right_pin = ft.Container(
    #bgcolor = dark postboard color?
    content=ft.DragTarget(group="widgets", on_accept=right_pin_drag_accept, content=right_pin_widgets
))

bottom_pin = ft.Container(
    content=ft.DragTarget(group="widgets", on_accept=bottom_pin_drag_accept, content=bottom_pin_widgets
))



# clears the controls so we can start fresh
def clear_all_controls():
    # Clear our controls
    top_pin_widgets.controls.clear()
    left_pin_widgets.controls.clear()
    main_work_area_widgets.controls.clear()
    right_pin_widgets.controls.clear()
    bottom_pin_widgets.controls.clear()


    top_pin.expand=False
    top_pin.height=min_pin_height

    left_pin.expand=False
    left_pin.width=min_pin_width

    right_pin.expand=False
    right_pin.width=min_pin_width

    bottom_pin.expand=False
    bottom_pin.height=min_pin_height




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
        # Otherwise, run our layout
        clear_all_controls()
        return print("No active widgets")
    if len(widgets) >= 24:  # max num widgets
        return print("Max num widgets reached")
    
    # Otherwise, run our layout
    clear_all_controls()
    
    # Render all widgets in same place, list up to 24 long. 
    # Fill in 'empty' slots with blank entries, but list is always 24 long
    for i in range(len(widgets) + 1):  # run through each widget and figure out where to put it
        
        if i == 1 or i == 2:    # First 2 go in the main work area
            main_work_area_widgets.controls.append(widgets[i-1])

        if i == 3:
            bottom_pin.expand=True
            bottom_pin.height=False
            bottom_pin_widgets.controls.append(widgets[i-1])
        if i == 4:
            #right_pin.expand=True
            right_pin.width=max_pin_width
            right_pin_widgets.controls.append(widgets[i-1])
        if i == 5:
            top_pin.expand=True
            top_pin.height=False
            top_pin_widgets.controls.append(widgets[i-1])
        if i == 6:
            left_pin.expand=True
            left_pin.width=False
            left_pin_widgets.controls.append(widgets[i-1])

   