'''
Layout our widgets whenever there is more than 2
'''
import flet as ft


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

   