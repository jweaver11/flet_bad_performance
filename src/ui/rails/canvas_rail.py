""" WIP """

import flet as ft
from models.views.story import Story
from ui.rails.rail import Rail
from styles.menu_option_style import Menu_Option_Style
import math


# Class for our Canvas Board rail
class Canvas_Rail(Rail):

    def __init__(self, page: ft.Page, story: Story):

        # Initialize the parent Rail class first
        super().__init__(
            page=page,
            story=story,
            directory_path=story.data.get('content_directory_path', ""),
        )

        # UI elements
        self.top_row_buttons = [
            ft.IconButton(
                tooltip="New Vertical Canvas",
                icon=ft.Icons.COMPARE_ARROWS_OUTLINED,
                rotate=ft.Rotate(math.pi/2),  # 90 degrees counter-clockwise
                on_click=self.new_canvas_clicked
            ),
            
            ft.IconButton(
                tooltip="New Horizontal canvas",
                #icon=ft.Icons.BRUSH_OUTLINED,
                icon=ft.Icons.COMPARE_ARROWS_OUTLINED,
                #rotate=ft.Rotate(0.70),  # 90 degrees clockwise
                on_click=self.new_canvas_clicked
            ),
            ft.IconButton(
                icon=ft.Icons.FILE_UPLOAD_OUTLINED,
                tooltip="Upload Canvas",
            )
        ]

        # Reload the rail on start
        self.reload_rail()

    # Called when new character button or menu option is clicked
    def new_canvas_clicked(self, e):
        ''' Handles setting our textfield for new character creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Canvas Title"
        self.new_item_textfield.data = "canvas"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()   

    

    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self):

        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=self.top_row_buttons
        )

        opacity = ft.Slider(
            min=0, max=100,
            divisions=10, value=self.story.data.get('canvas_data', {}).get('opacity', 100),
            label="Opacity: {value}%",
            on_change_end=lambda e: self.story.change_data(**{'canvas_data': {'opacity': int(e.control.value)}})
        )
        
                 

        # Build the content of our rail
        content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            controls=[
                opacity
            ]
        )

        # Build rail here
        # Open/Upload Upload
        # TODO: RAIL Has brushes, tools, colors, etc.
        # Rail shows our brush/drawing design options, not a view of all drawings

        

        # Type of brush?
        # Brush settings - color, width, anti alias, blen modes, blur image?, gradient


        content.controls.append(self.new_item_textfield)


        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                header,
                ft.Divider(),
                content
                # Add more controls here as needed
            ]
        )

        # Apply the update
        self.p.update()