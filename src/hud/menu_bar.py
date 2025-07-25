''' Menu bar at the top of the page '''
import flet as ft
from handlers.render_widgets import stack, widget_row, pin_drag_targets


def create_menu_bar(page: ft.Page):
    
    # Handler logic for each menu item clicked
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!"))
        )
        page.update()

    def handle_file_open_click(e):
        page.route = "/welcome"
        page.update()


    # Handlers called automatically for submenu events
    def handle_submenu_open(e):
        print(f"{e.control.content.content.value}.on_open")

    def handle_submenu_close(e):
        print(f"{e.control.content.content.value}.on_close")

    def handle_submenu_hover(e):
        print(f"{e.control.content.content.value}.on_hover")



    # Create our menu bar with submenu items
    menubar = ft.MenuBar(
       # Format menubar
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.TRANSPARENT,
            shadow_color=ft.Colors.TRANSPARENT,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            # Parent submenu item with child items on hover
            ft.SubmenuButton(
                content=ft.Container(
                    content=ft.Text("File"),
                    alignment=ft.alignment.center
                ),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT},
                ),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("New"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save as"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_file_open_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Import"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_file_open_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Export"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_file_open_click,
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
                content=ft.Container(
                    content=ft.Text("Edit"),
                    alignment=ft.alignment.center
                ),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                ),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Copy"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Paste"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Container(
                    content=ft.Text("  Upload  "),
                    alignment=ft.alignment.center
                ),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                ),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Text-chapters"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Image (comics)"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Video (animations?)"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Projects (other stories)"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Characters"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Worldbuilding, etc"),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Container(
                    content=ft.Text(" View "),
                    alignment=ft.alignment.center
                ),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                ),
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Zoom In"),
                        leading=ft.Icon(ft.Icons.ZOOM_IN),
                        close_on_click=False,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Zoom Out"),
                        leading=ft.Icon(ft.Icons.ZOOM_OUT),
                        close_on_click=False,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT}
                        ),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
        ], 
    )

    # Create our container for the menu bar
    menubar_container = ft.Container(
        bgcolor=ft.Colors.GREY_900,     # Set background color
        border_radius=ft.border_radius.all(4),  # 4px radius on all corners

        content=ft.Row(
            spacing=None,
            controls=[
                menubar,    # Menubar on left
                ft.Container(expand=True),  # empty space in middle of menubar
                ft.TextButton("Feedback"),  # Feedback button
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icon(ft.Icons.SETTINGS)),   # Settings button
                ft.TextButton("Account Name", icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED),  # users account name
            ]))



    return menubar_container
