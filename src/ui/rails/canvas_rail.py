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

        # UI elements ---------------------------------------------
        # Buttons at the top of the rail
        self.top_row_buttons = [
            ft.IconButton(
                tooltip="New Vertical Canvas",
                icon=ft.Icons.COMPARE_ARROWS_OUTLINED,
                rotate=ft.Rotate(math.pi/2),  # 90 degrees counter-clockwise
                on_click=self.new_canvas_clicked
            ),
            
            ft.IconButton(
                tooltip="New Horizontal canvas",
                icon=ft.Icons.COMPARE_ARROWS_OUTLINED,
                on_click=self.new_canvas_clicked
            ),
            ft.IconButton(
                icon=ft.Icons.FILE_UPLOAD_OUTLINED,
                tooltip="Upload Canvas",
                on_click=lambda e: print("Upload Canvas clicked")
            )
        ]

        # Color picker for changing brush color
        color_only = self.story.data.get('paint_settings', {}).get('color', "#000000").split(",", 1)[0]     # Set color without opacity for the color picker
        self.color_picker = ColorPicker(color=color_only)   # Set our color pickers color

        # Button to open the diolog to pick brush color
        self.color_picker_button = ft.IconButton(
            icon=ft.Icons.COLOR_LENS_OUTLINED,
            icon_color=self.story.data.get('paint_settings', {}).get('color', ft.Colors.PRIMARY),
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

   
    # Called when color picker button is clicked to change color
    def color_picker_clicked(self, e):
        ''' Opens a dialog to pick new hex brush color.'''

        # Called when the apply button is selected. Applies to color change to data and UI
        def _apply_color_change(e):

            # Our new selected color
            selected_color = self.color_picker.color
           
            # Our story data needs the opacity, but color picker can't have it
            opacity = self.story.data.get('canvas_data', {}).get('color', "1.0").split(",", 1)[1].strip()
            color_with_opacity = f"{selected_color},{opacity}"
            
            self.story.change_data(**{'paint_settings': {'color': color_with_opacity}})

            self.color_picker_button.icon_color = selected_color
            self.p.close(alert_dialog)
            self.p.update()

        # Alert dialog for picking color
        alert_dialog = ft.AlertDialog(
            title=ft.Text("Select Brush Color", weight=ft.FontWeight.BOLD),
            content=self.color_picker,
            actions=[
                ft.TextButton("CANCEL", on_click=lambda e: self.p.close(alert_dialog), style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("APPLY", on_click=_apply_color_change),
            ],
        )

        # Open the dialog
        self.p.open(alert_dialog)

    # Called when we change the opacity on our slider
    def opacity_changed(self, e):
        ''' Handles when the opacity slider is changed. Updates our story data. '''

        new_opacity = float(e.control.value)/100

        print("New Opacity:", new_opacity)

        # Get our current color without opacity
        current_color = self.story.data.get('paint_settings', {}).get('color', "#000000").split(",", 1)[0].strip()
        color_with_opacity = f"{current_color},{new_opacity}"

        print("Color with Opacity:", color_with_opacity)

        self.story.change_data(**{'paint_settings': {'color': color_with_opacity}})

    

    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self):

        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=self.top_row_buttons
        )


        opacity_value = float(self.story.data.get('paint_settings', {}).get('color', "1.0").split(",", 1)[1].strip()) * 100
        opacity = ft.Slider(
            min=0, max=100, expand=True,
            divisions=100, value=opacity_value,
            label="Opacity: {value}%",
            on_change_end=self.opacity_changed
        )
        
        
        # Type of brush?
        # Brush settings - color, width, anti alias, blend modes, blur image?, gradient
                 

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