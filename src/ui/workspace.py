'''
UI styling for the main workspace area of appliction that holds our widgets (tabs)
Returns our container with our formatting areas inside the workspace area.
The stories 'mast_stack' holds our 'master_row', which contains our five pins: top, left, main, right, and bottom.
Overtop that, we append our drag targets when we start dragging a widget (tab). Thats why its a stack
'''

import flet as ft
from models.app import app
from models.story import Story

# Function to return our container for our widgets
def create_workspace(page: ft.Page, story: Story=None) -> ft.Container:   

    # Called when giant new story button is clicked
    def create_new_story_button_clicked(e):
        ''' Opens a dialog to create a new story. Checks story is unique or not '''
        #print("New Story Clicked")

        # Variable to track if the title is unique
        is_unique = True

        # Called by clicking off the dialog or cancel button
        def close_dialog(e):
            ''' Closes the dialog '''
            dlg.open = False
            page.update()

        def submit_new_story(e):
            ''' Creates a new story with the given title '''

            # Import our variable if it is unique or nah
            nonlocal is_unique

            if isinstance(e, ft.TextField):
                print("Received the text field. title is e.value")
                title = e.value
            else:
                print("received the event, title is e.control.value")
                title = e.control.value

            print(title)

            for story in app.stories.values():
                if story.title == title:
                    is_unique = False
                    break

            # Check if the title is unique
            if is_unique:
                #print("title is unique, story being created: ", title)
                app.create_new_story(title, page) # Needs the story object
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
                ft.TextButton("Cancel", on_click=close_dialog, style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("Create", on_click=lambda e: submit_new_story(story_title_field)),
            ],
        )

        # Open our dialog in the overlay
        dlg.open = True
        page.overlay.append(dlg)
        page.update()


    # When we passed a story through, we show its master stack
    if story is not None:
        # Container for 1 or more widgets open on the workspace area right side of screen
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
            content=story.master_stack,   
        )
    
    # Otherwise, there is no active story, so we show a big button to create a new story
    else:
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
            content=ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                text="No Active Story\nClick to Create New Story",
                on_click=create_new_story_button_clicked,
                width=200,
                height=100,
                shape=ft.RoundedRectangleBorder(radius=10),  
            ),
        )
