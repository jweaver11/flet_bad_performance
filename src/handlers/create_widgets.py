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
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Draggable(
                        group="widgets", 
                        content=ft.TextButton(title)    # Title for the widget
                    )
                ]
            ),
            ft.Container(       # Body of the widget
                expand=True,
                content=ft.Column(body) 
            )
        ]) 
    )


    # return our formatted container
    return cont