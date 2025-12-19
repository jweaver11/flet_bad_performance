""" WIP """

import flet as ft
from models.views.story import Story
from ui.rails.rail import Rail
from styles.menu_option_style import Menu_Option_Style
import math
from flet_contrib.color_picker import ColorPicker
from models.app import app


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
                on_click=lambda e: print("Upload Canvas clicked")
            )
        ]

        self.color_picker = ColorPicker(color=self.story.data.get('canvas_data', {}).get('color', "#000000"))

        self.color_picker_button = ft.IconButton(
            icon=ft.Icons.COLOR_LENS_OUTLINED,
            icon_color=self.story.data.get('canvas_data', {}).get('color', ft.Colors.PRIMARY),
            tooltip="Color Picker", on_click=self.color_picker_clicked
        )
       

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

   

    def color_picker_clicked(self, e):

        def _apply_color_change(e):

            selected_color = self.color_picker.color
           
            print("Selected color: ", selected_color)
            self.story.change_data(**{'canvas_data': {'color': selected_color}})

            self.color_picker_button.icon_color = selected_color
            self.p.close(alert_dialog)
            self.p.update()

        alert_dialog = ft.AlertDialog(
            title=ft.Text("Select Brush Color", weight=ft.FontWeight.BOLD),
            content=self.color_picker,
            actions=[
                ft.TextButton("CANCEL", on_click=lambda e: self.p.close(alert_dialog), style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("APPLY", on_click=_apply_color_change),
            ],
        )

        self.p.open(alert_dialog)


    

    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self):

        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=self.top_row_buttons
        )

        opacity = ft.Slider(
            min=0, max=100, expand=True,
            divisions=100, value=self.story.data.get('canvas_data', {}).get('opacity', 100),
            label="Opacity: {value}%",
            on_change_end=lambda e: self.story.change_data(**{'canvas_data': {'opacity': int(e.control.value)}})
        )
        
        
        # Type of brush?
        # Brush settings - color, width, anti alias, blen modes, blur image?, gradient
                 

        # Build the content of our rail
        content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            controls=[
                self.color_picker_button,
                ft.Row([ft.Text("Opacity:", theme_style=ft.TextThemeStyle.LABEL_LARGE), opacity])
            ]
        )


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