''' 
UI element for our Menu bar at the top of the page (file, edit, etc)
Holds our settings icon, feedback, and account name as well
'''

import flet as ft
from constants import data_paths
from models.app import app
from handlers.reload_workspace import remove_drag_targets
from handlers.reload_workspace import reload_workspace

# Called by main on program start to create our menu bar
def create_menu_bar(page: ft.Page) -> ft.Container:
    
    # Placeholder events for now
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!"))
        )
        page.update()

    def handle_submenu_open(e):
        print(f"{e.control.content.content.value}.on_open")
    def handle_submenu_close(e):
        print(f"{e.control.content.content.value}.on_close")
    def handle_submenu_hover(e):
        print(f"{e.control.content.content.value}.on_hover")

    # Called when file->new is clicked
    def new_clicked(e):
        ''' Placeholder for new story click event '''
        print("New Story Clicked")

        def submit_new_story(title: str):
            ''' Creates a new story with the given title '''
            app.create_new_story(title)
            #app.active_story = new_story
            print(f"New story created with title: {title}")
            dlg.open = False
            reload_workspace(page)
            page.update()


        dlg = ft.AlertDialog(
            title=ft.Text("Create New Story"),
            content=ft.Text("This will create a new story with default settings. Continue?"),
            actions=[
                #ft.TextButton("Cancel", on_click=lambda e: page.dialog.close()),
                ft.TextButton("OK", on_click=lambda e: submit_new_story("new_story")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )

        dlg.open = True
        page.overlay.append(dlg)
        page.update()

        


        title = "new_story"
        new_story = app.create_new_story(title)

        app.active_story = new_story

    def handle_file_open_click(e):
        ''' Placeholder for open story click event '''
        print("Open Story Clicked")

        def get_story_list() -> list[ft.Control]:
            ''' Returns a list of all story titles available to open '''

            list = []

            for story in app.stories:
                list.append(ft.Text(story))

            return list

        dlg = ft.AlertDialog(
            title=ft.Text("What story would you like to open?"),
            alignment=ft.alignment.center,
            on_dismiss=lambda e: print("Dialog dismissed!"),
            title_padding=ft.padding.all(25),
            content=ft.Column(expand=False, controls=get_story_list()),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.TextButton("Open", on_click=lambda e: page.close(dlg)),
            ]
        )

        page.open(dlg)

        


    # Styling used by lots of menu bar items
    menubar_style = ft.ButtonStyle(
        bgcolor={ft.ControlState.HOVERED: ft.Colors.TRANSPARENT},
    )

    # Create our menu bar with submenu items
    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(     # Styling our menubar
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.TRANSPARENT,
            shadow_color=ft.Colors.TRANSPARENT,
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[  # The controls shown in our menu bar from left to right
            ft.SubmenuButton(   # Button that opens a subment
                content=ft.Container(
                    content=ft.Text("File", weight=ft.FontWeight.BOLD),     # Content of subment button
                    alignment=ft.alignment.center
                ),
                style=menubar_style,    # styleing for the button
                on_open=handle_submenu_open,    # Handle when a submenu is opened
                on_close=handle_submenu_close,  # Handle when a submenu is closed
                on_hover=handle_submenu_hover,  # Handle when a submenu is hovered
                controls=[      # The options shown inside of our button
                    ft.MenuItemButton(
                        content=ft.Text("New", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.ADD_CIRCLE_ROUNDED,),
                        style=menubar_style,
                        on_click=new_clicked,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=menubar_style,
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save as", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.SAVE),
                        style=menubar_style,
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=menubar_style,
                        on_click=handle_file_open_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Import", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=menubar_style,
                        on_click=handle_file_open_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Export", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=menubar_style,
                        on_click=handle_file_open_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        style=menubar_style,
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Container(
                    content=ft.Text("Edit", weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center
                ),
                style=menubar_style,
                on_open=handle_submenu_open,
                on_close=handle_submenu_close,
                on_hover=handle_submenu_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Copy", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=menubar_style,
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Paste", weight=ft.FontWeight.BOLD),
                        leading=ft.Icon(ft.Icons.INFO),
                        style=menubar_style,
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
        ], 
    )

    # Called when the settings icon on the right side of the menubar is clicked
    def settings_clicked(e):
        ''' Toggles the visibility of the settings widget in the menubar '''

        app.settings.change_visibility()
        if app.settings.data['visible']:
            app.settings.show_widget()
        else:
            app.settings.hide_widget()

        reload_workspace(page)  # Re-render the page to show/hide settings

    def view1(e):
        print("View 1")
        
        from handlers.route_change import route_change

        route_change(page, app.stories['default_story'])
        

    def view2(e):
        print("View 2")
        from handlers.route_change import route_change

        route_change(page, app.stories['test_story_1'])
        
    # Return our formatted menubar
    return ft.Container(
        border=ft.border.only(bottom=ft.BorderSide(width=1, color=ft.Colors.OUTLINE_VARIANT)),
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.ON_INVERSE_SURFACE),

        content=ft.Row(
            spacing=None,
            controls=[
                menubar,    # Menubar on left
                ft.Container(expand=True),  # empty space in middle of menubar
                # Fix broken widgets button

                ft.IconButton(icon=ft.Icons.BUNGALOW, on_click=view1),
                ft.IconButton(icon=ft.Icons.BUNGALOW, on_click=view2),


                ft.IconButton(icon=ft.Icons.BUILD_ROUNDED, on_click=lambda e: remove_drag_targets(), tooltip="Click if broken"),
                ft.TextButton("Feedback"),  # Feedback button
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, on_click=settings_clicked),   # Settings button
                ft.TextButton("Account Name", icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED),  # apps account name
            ]
        )
    )
