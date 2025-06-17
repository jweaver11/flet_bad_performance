import flet as ft

# Other widgets use this function as the 'parent' to return same formatting, with dif bodies
def new_widget(title, body):
    

    cont = ft.Container(
        expand=True,
        padding=6,
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        bgcolor=ft.Colors.GREY_900,
        visible=True,
        content=ft.Column([
            ft.Draggable(group="top_row", content=ft.Row(     # Title of the widget
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[ft.TextButton(title)]
            )),
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column(body) 
            )
        ]) 
    )


    # return our formatted container
    return cont