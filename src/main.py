'''
The main file to run the application.
Initializes the app, settings, page data, and renders our UI onto the page
'''

import flet as ft
from models.app import app
from handlers.route_change import route_change
from models.views.loading import create_loading_view
import asyncio
from ui.workspaces_rail import Workspaces_Rail

# Main function
def main(page: ft.Page):

    

    def show_horizontal_cursor(e: ft.HoverEvent):
        ''' Changes the cursor to horizontal when hovering over the resizer '''

        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        e.control.update()

        # Called when resizing the active rail by dragging the resizer
    def move_active_rail_divider(e: ft.DragUpdateEvent):
        ''' Responsible for altering the width of the active rail '''

        cont.height = cont.height + int(e.local_delta.y)     
        cont2.height = cont2.height + int(e.local_delta.y)
        cont3.height = cont3.height + int(e.local_delta.y)
        cont4.height = cont4.height + int(e.local_delta.y)       
        page.update()   # Apply our changes to the rest of the page

    cont = ft.Container(width=250, height=250, border=ft.Border.all(1, ft.Colors.RED), bgcolor=ft.Colors.YELLOW)
    cont2 = ft.Container(expand=True, height=250, bgcolor="red")
    cont3 = ft.Container(expand=True, height=250, bgcolor="blue")
    cont4 = ft.Container(expand=True, height=250, bgcolor="green")

    page.add(
        
            ft.Row([cont, cont2, cont3, cont4]), 
            
            ft.GestureDetector(
                content=ft.Container(
                    height=10,   # Total width of the GD, so its easier to find with mouse
                    
                    # Thin vertical divider, which is what the app will actually drag
                    content=ft.Divider(thickness=2, height=2, color=ft.Colors.BLUE),     # Original
                    padding=ft.Padding.only(right=8),  # Push the 2px divider ^ to the right side
                ),
                on_hover=show_horizontal_cursor,    # Change our cursor to horizontal when hovering over the resizer
                on_pan_update=move_active_rail_divider, # Resize the active rail as app is dragging
                #on_pan_end=save_active_rail_width,  # Save the resize when app is done dragging
                drag_interval=10,
            ),
        
    )
    page.update()

    page.controls.clear()

    # Our loading view while we setup the app
    page.views.append(create_loading_view(page))
    page.update()


    # Set our route change function to be called on route changes
    page.on_route_change = route_change 
    
    # Load settings and previous story (if one exists)
    app.load_settings(page)             

    # Load our previous story if one was active. If not, it will give us our home view
    asyncio.create_task(app.load_previous_story(page)) 


# Runs the app
if __name__ == "__main__":
    ft.run(main)
