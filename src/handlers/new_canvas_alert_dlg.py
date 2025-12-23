''' Used to open the overlay for creating a new canvas '''

import flet as ft
from models.views.story import Story


def new_canvas_alert_dlg(page: ft.Page, story: Story, directory_path: str=None) -> ft.AlertDialog:
    ''' Creates a new alert dialog for the canvas '''

    def _text_field_changed(e):
        ''' Handles when the text field is changed '''
        # Set our nonlocal variables
        nonlocal canvas_data, create_button

        # Grab out data (key) and pass in the value to our data dict
        data = e.control.data
        canvas_data[data] = e.control.value

        # Reset error text
        e.control.error_text = None

        if e.control.value == "":
            value = int()
            
        else:
            value = int(e.control.value)

        if value == 0:
            e.control.error_text = f"{data.capitalize()} cannot be 0"
            create_button.disabled = True
            page.update()
            return

            

        # Enable the button if both height and width have been set
        if canvas_data.get('width') is not None and canvas_data.get('height') is not None:
            if int(canvas_data.get('width')) > 0 and int(canvas_data.get('height')) > 0:    # Make sure no 0 values
                create_button.disabled = False
                page.update()
        page.update()
            
            
            

    def _title_text_field_changed(e):
        title = e.control.value

        if title != "":
            e.control.error_text = None
            create_button.disabled = False
            page.update()
        else:
            e.control.error_text = "Title cannot be empty"
            create_button.disabled = True
            page.update()

        # Check here for title taken
        

    def _new_option_selected(e):

        # Set our data for when creating the canvas
        nonlocal canvas_data
        data = e.control.data

        canvas_data.update(data)

        create_button.disabled = False
        page.update()

    def _create_button_clicked(e):
        ''' Handles creating a new canvas when create is clicked '''
        nonlocal canvas_data

        title = title_textfield.value if title_textfield.value != "" else f"Canvas {len(story.canvases) + 1}"

        story.create_canvas(
            title=title,
            directory_path=directory_path,
            data=canvas_data
        )

        # Build the canvas here
        page.close(alert_dialog)
        page.update()

    canvas_data = {'width': None, 'height': None, 'aspect_ratio': None}       # Data we will pass set to pass in whenever a different option is selected
    create_button = ft.TextButton(text="CREATE", on_click=_create_button_clicked, disabled=True)  # Button to create the canvas
    width_textfield = ft.TextField(
        label="Width", data="width", width=140, dense=True,  input_filter=ft.NumbersOnlyInputFilter(), 
        max_length=4, on_change=_text_field_changed
    )
    height_textfield = ft.TextField(
        label="Height", data="height", width=140, dense=True, input_filter=ft.NumbersOnlyInputFilter(), 
        max_length=4, on_change=_text_field_changed
    )  
    title_textfield = ft.TextField(
        label="Title", data="title", width=300, autofocus=True, on_change=_title_text_field_changed, capitalization=ft.TextCapitalization.WORDS # Add check for other widgets with same names
    )
    

    alert_dialog = ft.AlertDialog(
        title=ft.Text("Build Your Canvas", weight=ft.FontWeight.BOLD),
        
        actions=[
            ft.TextButton("CANCEL", on_click=lambda e: page.close(alert_dialog), style=ft.ButtonStyle(color=ft.Colors.ERROR)),
            create_button
        ],
        content=ft.Row(
            #alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
            spacing=20,
            controls=[
                title_textfield,
                ft.Divider(),
                ft.Container(
                    content=ft.Text("Blank", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=120, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=120
                ),
                width_textfield,
                height_textfield,
                ft.Divider(color=ft.Colors.TRANSPARENT),
                
                ft.Text("Horizontal", weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.LABEL_LARGE, text_align=ft.TextAlign.RIGHT, width=88),
                
                ft.Container(
                    content=ft.Text("4k (3840x2160)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=90, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=160
                ),
                ft.Container(
                    content=ft.Text("2k (2560x1440)",text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=90, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=160
                ),
                ft.Container(
                    content=ft.Text("HD (1920x1080)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=90, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=160
                ),
                ft.Container(
                    content=ft.Text("Banner (1500x500)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=53, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=160
                ),
                ft.Divider(color=ft.Colors.TRANSPARENT),
               
            
                ft.Text("Vertical", weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.LABEL_LARGE, text_align=ft.TextAlign.RIGHT, width=88),
                
                ft.Container(
                    content=ft.Text("4k (2160x3840)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected, 
                    height=160, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=90,
                ),
                ft.Container(
                    content=ft.Text("2k (1440x2560)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=160, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=90
                ),
                ft.Container(
                    content=ft.Text("HD (1080x1920)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected, 
                    height=160, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=90
                ),
                ft.Container(
                    content=ft.Text("Banner (500x1500)", text_align=ft.TextAlign.CENTER), padding=ft.padding.all(5), border_radius=4,
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT), on_click=_new_option_selected,
                    height=160, alignment=ft.alignment.top_center, bgcolor=ft.Colors.SURFACE, width=90
                ),
                ft.Divider(color=ft.Colors.TRANSPARENT),


                ft.Text("Aspect Ratio", weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.LABEL_LARGE, text_align=ft.TextAlign.RIGHT, width=88),
            ], 
            
        )
    )

    # aspect ratios: 1:1, 4:3, 16:9, 3:2, 2:1, 1:2, 9:16, 3:4

    return alert_dialog