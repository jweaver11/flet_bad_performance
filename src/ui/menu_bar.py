''' 
UI element for our Menu bar at the top of the page (file, edit, etc)
Holds our settings icon, feedback, and account name as well
'''

import flet as ft
from models.app import app
from models.story import Story
#from handlers.reload_workspace import remove_drag_targets
#from handlers.reload_workspace import reload_workspace

# Called by main on program start to create our menu bar
def create_menu_bar(page: ft.Page, story: Story=None) -> ft.Container:
    
    # Placeholder events for now
    def handle_menu_item_click(e):
        #print(f"{e.control.content.value}.on_click")
        page.open(
            ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!"))
        )
        page.update()

    def handle_submenu_open(e):
        #print(f"{e.control.content.content.value}.on_open")
        pass
    def handle_submenu_close(e):
        #print(f"{e.control.content.content.value}.on_close")
        pass
    def handle_submenu_hover(e):
        #print(f"{e.control.content.content.value}.on_hover")
        pass


    # Called when file -> new is clicked
    def handle_create_new_story_clicked(e):
        ''' Opens a dialog to create a new story. Checks story is unique or not '''
        #print("New Story Clicked")

        # Variable to track if the title is unique
        is_unique = True

        def submit_new_story(e):
            ''' Creates a new story with the given title '''

            # Import our variable if it is unique or nah
            nonlocal is_unique

            if isinstance(e, ft.TextField):
                #print("Received the text field. title is e.value")
                title = e.value
            else:
                #print("received the event, title is e.control.value")
                title = e.control.value

            print(title)

            for story in app.stories.values():
                if story.title == title:
                    is_unique = False
                    break

            # Check if the title is unique
            if is_unique:
                #print("title is unique, story being created: ", title)
                app.create_new_story(title, page, "default") # Needs the story object
                dlg.open = False
                page.update()
            else:
                #print("Title not unique, no story created")
                story_title_field.error_text = "Title must be unique"
                story_title_field.focus()   # refocus the text field since the title was not unique
                page.update()


        # Called everytime the user enters a new letter in the text box
        def textbox_value_changed(e):
            ''' Called when the text in the text box changes '''

            nonlocal is_unique

            # Checks if the title sitting in the text box is unique for submitting
            title = e.control.value
            for story in app.stories.values():
                if story.title == title:
                    e.control.error_text = "Title must be unique"
                    is_unique = False
                    page.update()
                    return
                else:
                    e.control.error_text = None
                    is_unique = True
                    page.update()

            
            #print(f"New story created with title: {title}")

        # Create a reference to the text field so we can access its value
        story_title_field = ft.TextField(
            label="Story Title",
            autofocus=True,
            on_submit=submit_new_story,
            on_change=textbox_value_changed,
        )
            
        # The dialog that will pop up whenever the new story button is clicked
        dlg = ft.AlertDialog(

            # Title of our dialog
            title=ft.Text("Create New Story"),

            # Main content is text box for user to input story title
            content=story_title_field,

            # Our two action buttons at the bottom of the dialog
            actions=[
                #ft.TextButton("Cancel", on_click=page.close(dlg), style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("Create", on_click=lambda e: submit_new_story(story_title_field)),
            ],
        )
        
        # Add cancel button. Sometimes adding it ^^ first breaks and idk y
        dlg.actions.insert(0, ft.TextButton("Cancel", on_click=lambda e: page.close(dlg), style=ft.ButtonStyle(color=ft.Colors.ERROR)))

        # Open our dialog in the overlay
        page.open(dlg)


    # Called when file -> open is clicked
    def handle_file_open_click(e):
        ''' Opens a dialog to open an existing story '''

        #print("Open Story Clicked")

        # list that holds our story title buttons, and string of our selected story title
        story_choices = []
        selected_story = None

        # Called when a new story text button is clicked
        def change_selected_story(e):
            ''' Changes our selected story variable '''

            nonlocal selected_story
            selected_story = e.control.text
            #print("Selected story: ", selected_story)

        # Returns a list of all story titles available to open
        def get_stories_list() -> list[ft.Control]:
            ''' Returns a list of all story titles available to open '''

            # Use something better than radio in future, but for now this works
            for story in app.stories.values():
                story_choices.append(
                    ft.TextButton(story.title, on_click=change_selected_story)
                )

            return story_choices


        # Called when the 'open' button is clicked in the bottom right of the dialog
        def open_selected_story(e):
            ''' Changes the route to the selected story '''

            #print("Open button clicked, selected story is: ", selected_story)

            if selected_story is not None:
                print("Opening story: ", selected_story)
                page.route = app.stories[selected_story].route
                page.close(dlg)
                page.update()
            else:
                print("No story selected")

            page.close(dlg)
            page.update()

        # Our alert dialog that pops up when file -> open is clicked
        dlg = ft.AlertDialog(
            title=ft.Text("What story would you like to open?"),
            alignment=ft.alignment.center,
            title_padding=ft.padding.all(25),
            content=ft.Column(expand=False, controls=get_stories_list()),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg), style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("Open", on_click=open_selected_story),
            ]
        )

        # Opens our dialog
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
                        on_click=handle_create_new_story_clicked,
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
    def settings_clicked(story: Story):
        ''' Toggles the visibility of the settings widget in the menubar '''
        print("Settings clicked")

        if app.settings.data['visible']:
            app.settings.toggle_visibility(story)
        else:
            app.settings.toggle_visibility(story)


        
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


                ft.IconButton(icon=ft.Icons.BUILD_ROUNDED, on_click=lambda e: story.workspace.remove_drag_targets(), tooltip="Click if broken"),
                ft.TextButton("Feedback"),  # Feedback button
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED, on_click=lambda e: settings_clicked(story)),   # Settings button
                ft.TextButton("Account Name", icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED),  # apps account name
            ]
        )
    )
