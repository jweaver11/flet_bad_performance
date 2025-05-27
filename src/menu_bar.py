''' Menu bar at the top of the page '''
import flet as ft

def create_menu_bar(page: ft.Page):
    
    # Handler logic for each menu item clicked
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!"))
        )
        page.update()

    def handle_bugs_click(e):
        # Print to console
        print(f"{e.control.content.value}.on_click. Theyre under my skin")
        page.open(
            # Pop up on bottom of app and disappear quickly
            ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked! claw them out now"))
        )
        page.update()


    # Handlers called automatically for submenu events
    def handle_submenu_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_submenu_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_submenu_hover(e):
        print(f"{e.control.content.value}.on_hover")

    # Create our menu bar with submenu items
    menubar = ft.MenuBar(
       # Format menubar
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            # Parent submenu item with child items on hover
            ft.SubmenuButton(
                content=ft.Text("File"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("About"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Edit"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.Icons.ZOOM_IN),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.Icons.ZOOM_OUT),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    )
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Insert"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.Icons.ZOOM_IN),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.Icons.ZOOM_OUT),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    )
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("View"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.Icons.ZOOM_IN),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.Icons.ZOOM_OUT),
                                close_on_click=False,
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                                ),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    )
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Feedback"),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Bugs"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_bugs_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Feature Suggestions"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    )  
                ],
            ),
        ],
    )
    return menubar
