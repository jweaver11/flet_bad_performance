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
            icon=ft.Icons.COLOR_LENS_OUTLINED, tooltip="The color of your brush strokes.",
            icon_color=self.story.data.get('paint_settings', {}).get('color', ft.Colors.PRIMARY),
            on_click=self._color_picker_clicked
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
    def _color_picker_clicked(self, e):
        ''' Opens a dialog to pick new hex brush color.'''

        # Called when the apply button is selected. Applies to color change to data and UI
        def _apply_color_change(e):

            # Our new selected color
            selected_color = self.color_picker.color
           
            # Our story data needs the opacity, but color picker can't have it
            opacity = self.story.data.get('paint_settings', {}).get('color', "1.0").split(",", 1)[1].strip()
            color_with_opacity = f"{selected_color},{opacity}"
            
            self.story.data['paint_settings']['color'] = color_with_opacity
            self.story.save_dict()

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



    # Called on startup and when we have changes to the rail that have to be reloaded 
    def reload_rail(self):
        ''' Reloads the canvas rail with updated data and UI elements. '''

        # Called when changing paint width
        def _paint_width_changed(e):
            new_width = int(e.control.value)
            # Change the data directly
            self.story.data['paint_settings']['stroke_width'] = new_width
            self.story.save_dict()

        # Called when changing paint opacity
        def _paint_opacity_changed(e):
            new_opacity = float(e.control.value)/100

            # Get our current color without opacity
            current_color = self.story.data.get('paint_settings', {}).get('color', "#000000").split(",", 1)[0].strip()
            color_with_opacity = f"{current_color},{new_opacity}"

            # Change the data directly
            self.story.data['paint_settings']['color'] = color_with_opacity
            self.story.save_dict()

        # Called when changing paint style
        def _paint_style_changed(e):
            new_style = e.control.text.lower()      # New style
            self.story.data['paint_settings']['stroke_dash_pattern'] = None   # Clear any dash pattern when changing style
            if new_style == "stroke":       # Change the icon
                e.control.parent.content = ft.Icon(ft.Icons.BRUSH_OUTLINED)
            elif new_style == "fill":
                e.control.parent.content = ft.Icon(ft.Icons.FORMAT_COLOR_FILL_OUTLINED)
            else:
                # Dashed line is not a style, so we just add stroke_dash pattern data and return
                e.control.parent.content = ft.Icon(ft.Icons.LINE_STYLE_OUTLINED)
                self.story.data['paint_settings']['stroke_dash_pattern'] = [self.story.data['paint_settings']['stroke_width'], self.story.data['paint_settings']['stroke_width']]   # Default dash pattern
                self.story.save_dict()
                self.p.update()
                return
            self.story.data['paint_settings']['style'] = new_style      # Update the data
            self.story.save_dict()
            self.p.update()     # Update the page

        # Called when changing paint anti-aliasing
        def _paint_anti_alias_changed(e):
            new_anti_alias = e.control.value
            self.story.data['paint_settings']['anti_alias'] = new_anti_alias
            self.story.save_dict()

        def _paint_stroke_cap_changed(e):
            new_stroke_cap = e.control.text.lower()
            if new_stroke_cap == "butt":
                e.control.parent.content = ft.Icon(ft.Icons.CROP_SQUARE_OUTLINED)
            elif new_stroke_cap == "round":
                e.control.parent.content = ft.Icon(ft.Icons.CIRCLE_OUTLINED)
            else:
                e.control.parent.content = ft.Icon(ft.Icons.SQUARE_OUTLINED)
            self.story.data['paint_settings']['stroke_cap'] = new_stroke_cap
            self.story.save_dict()
            self.p.update()

        def _paint_stroke_join_changed(e):
            new_stroke_join = e.control.text.lower()
            # Update icon based on stroke join type if desired
            if new_stroke_join == "miter":
                e.control.parent.content = ft.Icon(ft.Icons.CROP_SQUARE_OUTLINED)
            elif new_stroke_join == "round":
                e.control.parent.content = ft.Icon(ft.Icons.CIRCLE_OUTLINED)
            else:
                e.control.parent.content = ft.Icon(ft.Icons.SQUARE_OUTLINED)
            self.story.data['paint_settings']['stroke_join'] = new_stroke_join
            self.story.save_dict()
            self.p.update()

        # Our header at the top of the rail
        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=self.top_row_buttons
        )

        # Opacity slider
        opacity_value = float(self.story.data.get('paint_settings', {}).get('color', "1.0").split(",", 1)[1].strip()) * 100
        paint_opacity = ft.Slider(
            min=0, max=100,  tooltip="The opacity of your brush strokes.",
            divisions=100, value=opacity_value, expand=True,
            label="Opacity: {value}%",
            on_change_end=_paint_opacity_changed
        )

        # Width/Size of brush
        paint_width = ft.Slider(
            min=1, max=50,  tooltip="The size of your brush strokes.", expand=True,
            divisions=49, value=self.story.data.get('paint_settings', {}).get('stroke_width', 5),
            label="Brush Size: {value}px",
            on_change_end=_paint_width_changed
        )

        # Paint style (fill or stroke)
        paint_style = ft.PopupMenuButton(
            content=ft.Icon(ft.Icons.BRUSH_OUTLINED) if self.story.data.get('paint_settings', {}).get('style', 'stroke') == 'stroke' else ft.Icon(ft.Icons.FORMAT_COLOR_FILL_OUTLINED),
            tooltip="The style of paint for your brush strokes.",
            menu_padding=ft.padding.all(0),
            items=[
                ft.PopupMenuItem(text="Stroke", icon=ft.Icons.BRUSH_OUTLINED, on_click=_paint_style_changed),
                ft.PopupMenuItem(text="Dashed Stroke", icon=ft.Icons.LINE_STYLE_OUTLINED, on_click=_paint_style_changed),
                ft.PopupMenuItem(text="Fill", icon=ft.Icons.FORMAT_COLOR_FILL_OUTLINED, on_click=_paint_style_changed),
            ]
        )

        # If we use anti aliasing or not
        paint_anti_alias = ft.Checkbox(
            label="Anti-Aliasing", on_change=_paint_anti_alias_changed,
            label_position=ft.LabelPosition.LEFT,
            value=self.story.data.get('paint_settings', {}).get('anti_alias', True)
        )

        # Stroke cap shape
        if self.story.data.get('paint_settings', {}).get('stroke_cap', 'butt') == 'round':
            paint_stroke_icon = ft.Icon(ft.Icons.CIRCLE_OUTLINED)
        elif self.story.data.get('paint_settings', {}).get('stroke_cap', 'butt') == 'square':
            paint_stroke_icon = ft.Icon(ft.Icons.SQUARE_OUTLINED)
        else:
            paint_stroke_icon = ft.Icon(ft.Icons.CROP_SQUARE_OUTLINED)
        paint_stroke_cap = ft.PopupMenuButton(
            content=paint_stroke_icon,
            tooltip="The shape that your brush strokes will have at the end of each line segment.",
            menu_padding=ft.padding.all(0),
            items=[
                ft.PopupMenuItem(text="Butt", on_click=_paint_stroke_cap_changed, icon=ft.Icons.CROP_SQUARE_OUTLINED, tooltip="Flat cut ends"),
                ft.PopupMenuItem(text="Round", on_click=_paint_stroke_cap_changed, icon=ft.Icons.CIRCLE_OUTLINED, tooltip="Rounded ends"),
                ft.PopupMenuItem(text="Square", on_click=_paint_stroke_cap_changed, icon=ft.Icons.SQUARE_OUTLINED, tooltip="Sharp cut ends"),
            ]
        )

        if self.story.data.get('paint_settings', {}).get('stroke_join', 'miter') == 'round':
            stroke_cap_icon = ft.Icon(ft.Icons.CIRCLE_OUTLINED)
        elif self.story.data.get('paint_settings', {}).get('stroke_join', 'miter') == 'bevel':
            stroke_cap_icon = ft.Icon(ft.Icons.SQUARE_OUTLINED)
        else:
            stroke_cap_icon = ft.Icon(ft.Icons.CROP_SQUARE_OUTLINED)
        paint_stroke_join = ft.PopupMenuButton(
            content=stroke_cap_icon,
            tooltip="The shape that your brush strokes will have at the join of two line segments.",
            menu_padding=ft.padding.all(0),
            items=[
                ft.PopupMenuItem(text="Miter", icon=ft.Icons.CROP_SQUARE_OUTLINED, on_click=_paint_stroke_join_changed, tooltip="Sharp corners"),
                ft.PopupMenuItem(text="Round", icon=ft.Icons.CIRCLE_OUTLINED, on_click=_paint_stroke_join_changed, tooltip="Rounded corners"),
                ft.PopupMenuItem(text="Bevel", icon=ft.Icons.SQUARE_OUTLINED, on_click=_paint_stroke_join_changed, tooltip="Flat cut corners"),
            ]
        )




        # Build the content of our rail
        content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row([ft.Text("Brush Settings: ", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.color_picker_button, paint_style], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                ft.Row([ft.Text("Size", theme_style=ft.TextThemeStyle.LABEL_LARGE), paint_width]),
                ft.Row([ft.Text("Opacity", theme_style=ft.TextThemeStyle.LABEL_LARGE), paint_opacity]),
                ft.Row([ft.Text("Stroke Cap Shape", theme_style=ft.TextThemeStyle.LABEL_LARGE), paint_stroke_cap]),
                ft.Row([ft.Text("Stroke Join Shape", theme_style=ft.TextThemeStyle.LABEL_LARGE), paint_stroke_join]),

                # gradient
                # stroke dash pattern
                
                ft.Divider(),
                ft.Row([ft.Text("Effects: ", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([paint_anti_alias]),

                # blend mode
                # blur image

            ]
        )
        ft.Paint()

        #blend_mode: BlendMode | None = None,
        #blur_image: float | int | Tuple[float | int, float | int] | Blur | None = None,
        #gradient: PaintGradient | None = None,
        #stroke_cap: StrokeCap | None = None,
        #stroke_join: StrokeJoin | None = None,
        #stroke_miter_limit: float | None = None,
        #stroke_width: float | None = None,
        #stroke_dash_pattern: List[float] | None = None,
        #style: PaintingStyle | None = None


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