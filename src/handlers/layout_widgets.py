'''
Layout our widgets whenever there is more than 2
'''
import flet as ft
def top_pin_drag_accept(e):
    print("top pin accepted")
def left_pin_drag_accept(e):
    print("left pin accepted")
def right_pin_drag_accept(e):
    print("right pin accepted")
def bottom_pin_drag_accept(e):
    print("bottom pin accepted")

# AI stuff
top_pin = ft.DragTarget(group="widgets", on_accept=top_pin_drag_accept, content=ft.Container(height=50, bgcolor=ft.Colors.GREY_700))
left_pin = ft.DragTarget(group="widgets", on_accept=left_pin_drag_accept, content=ft.Container(width=50, bgcolor=ft.Colors.GREY_700))
right_pin = ft.DragTarget(group="widgets", on_accept=right_pin_drag_accept, content=ft.Container(width=50, bgcolor=ft.Colors.GREY_700))
bottom_pin = ft.DragTarget(group="widgets", on_accept=bottom_pin_drag_accept, content=ft.Container(height=50, bgcolor=ft.Colors.GREY_700))

# autopin widgets when more than 2 are active so they look nicer
def layout_widgets(widgets):
    if len(widgets) == 1:
        return widgets[0]
    elif len(widgets) == 2:
        return ft.Row([widgets[0], widgets[1]], expand=True)
    elif len(widgets) == 3:
        return ft.Column([
            ft.Row([widgets[0], widgets[1]], expand=True),
            widgets[2]
        ], expand=True)
    else:
        return print("no active widgets")
    # ... extend for more widgets