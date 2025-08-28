'''
UI styling for the main workspace area of appliction that holds our widgets (tabs)
Returns our container with our formatting areas inside the workspace area.
The stories 'mast_stack' holds our 'master_row', which contains our five pins: top, left, main, right, and bottom.
Overtop that, we append our drag targets when we start dragging a widget (tab). Thats why its a stack
'''

import flet as ft
from models.app import app
from models.story import Story

# Our workspace object that is stored in our story object
class Workspace(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):

        # Set our container properties for the workspace
        super().__init__(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_INVERSE_SURFACE),
        )

        # Creates our 5 pin locations for our widgets inside our workspace
        self.top_pin = ft.Row(spacing=0, controls=[])
        self.left_pin = ft.Column(spacing=0, controls=[])
        self.main_pin = ft.Row(expand=True, spacing=0, controls=[])
        self.right_pin = ft.Column(spacing=0, controls=[])
        self.bottom_pin = ft.Row(spacing=0, controls=[])

        # Our master row that holds all our widgets
        self.widgets = ft.Row(spacing=0, expand=True, controls=[])

        # Master stack that holds our widgets ^ row. We add our drag targets overtop our widgets, so we use a stack here
        # And our drag targets when we start dragging widgets.
        # We use global stack like this so there is always a drag target, even if a pin is empty
        self.master_stack = ft.Stack(expand=True, controls=[self.widgets])

        #self.reload_workspace(page, story)

    # Called when we need to reload our workspace content, especially after pin drags
    def reload_workspace(self, page: ft.Page, story: Story):
        ''' Reloads our workspace content by clearing and re-adding our 5 pin locations to the master row '''

        from handlers.arrange_widgets import arrange_widgets


        arrange_widgets(story)

        # Change our cursor when we hover over a resizer (divider). Either vertical or horizontal
        def show_vertical_cursor(e: ft.HoverEvent):
            e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
            e.control.update()
        def show_horizontal_cursor(e: ft.HoverEvent):
            e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
            e.control.update()

        def do_nothing(e: ft.HoverEvent):
            pass

        # Rendering adds dividers between each widget. So if we remove old ones here
        #story.top_pin.controls = [control for control in story.top_pin.controls if type(control) != ft.GestureDetector]
        #story.left_pin.controls = [control for control in story.left_pin.controls if type(control) != ft.GestureDetector]
        #story.right_pin.controls = [control for control in story.right_pin.controls if type(control) != ft.GestureDetector]
        #story.bottom_pin.controls = [control for control in story.bottom_pin.controls if type(control) != ft.GestureDetector]

        # Create gesture detector dividers and insert them between each visible control. Start with top pin
        #visible_top_controls = [control for control in story.top_pin.controls if getattr(control, 'visible', True)]
        #if len(visible_top_controls) > 1:
            # Work backwards to avoid index shifting issues when inserting
            # Find positions of visible controls in the original list and insert dividers between them
            #visible_indices = [i for i, control in enumerate(story.top_pin.controls) if getattr(control, 'visible', True)]
            #for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                #insert_position = visible_indices[i]
                #gd = ft.GestureDetector(
                    #content=ft.Container(
                        #width=10,
                        #bgcolor=ft.Colors.TRANSPARENT,
                        #padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                        #content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
                    #),
                    #on_hover=show_horizontal_cursor,
                    #on_hover= do_nothing,  # No hover effect for left pin
                    #on_pan_update=resize the left pin controls
                #)
                #story.top_pin.controls.insert(insert_position, gd)
        
        # left pin
        # First, get only visible controls to determine where dividers should go
        #visible_left_controls = [control for control in story.left_pin.controls if getattr(control, 'visible', True)]
        #if len(visible_left_controls) > 1:
            # Work backwards to avoid index shifting issues when inserting
            # Find positions of visible controls in the original list and insert dividers between them
            #visible_indices = [i for i, control in enumerate(story.left_pin.controls) if getattr(control, 'visible', True)]
            #for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                #insert_position = visible_indices[i]
                #gd = ft.GestureDetector(
                    #content=ft.Container(
                        #height=10,
                        #bgcolor=ft.Colors.TRANSPARENT,
                        #padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                    # content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
                    #),
                    #on_hover=show_vertical_cursor,
                    #on_hover= do_nothing,  # No hover effect for left pin
                    #on_pan_update=resize the left pin controls
                #)
                #story.left_pin.controls.insert(insert_position, gd)


        # right pin
        # First, get only visible controls to determine where dividers should go
        #visible_right_controls = [control for control in story.right_pin.controls if getattr(control, 'visible', True)]
        #if len(visible_right_controls) > 1:
            # Work backwards to avoid index shifting issues when inserting
            # Find positions of visible controls in the original list and insert dividers between them
            #visible_indices = [i for i, control in enumerate(story.right_pin.controls) if getattr(control, 'visible', True)]
            #for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                #insert_position = visible_indices[i]
                #gd = ft.GestureDetector(
                    #content=ft.Container(
                    # height=10,
                        #bgcolor=ft.Colors.TRANSPARENT,
                        #padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                    # content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
                    #),
                    #on_hover=show_vertical_cursor,
                    #on_hover= do_nothing,  # No hover effect for left pin
                #)
                #story.right_pin.controls.insert(insert_position, gd)

        # bottom pin
        # First, get only visible controls to determine where dividers should go
        #visible_bottom_controls = [control for control in story.bottom_pin.controls if getattr(control, 'visible', True)]
        #if len(visible_bottom_controls) > 1:
            # Work backwards to avoid index shifting issues when inserting
            # Find positions of visible controls in the original list and insert dividers between them
            #visible_indices = [i for i, control in enumerate(story.bottom_pin.controls) if getattr(control, 'visible', True)]
            #for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                #insert_position = visible_indices[i]
                #gd = ft.GestureDetector(
                    #content=ft.Container(
                        #width=10,
                        #bgcolor=ft.Colors.TRANSPARENT,
                        #padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                        #content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
                    #),
                    #on_hover=show_horizontal_cursor,
                    #on_hover= do_nothing,  # No hover effect for left pin
                #)
                #story.bottom_pin.controls.insert(insert_position, gd)


        # Main pin is rendered as a tab control, so we won't use dividers and will use different logic
        #visible_main_controls = [control for control in story.main_pin.controls if getattr(control, 'visible', True)]
        #if len(visible_main_controls) > 1:
            # Get the selected tab index from the story object, default to 0
            #selected_tab_index = getattr(story, 'selected_main_tab_index', 0)
            # Ensure the index is within bounds
            #if selected_tab_index >= len(visible_main_controls):
                #selected_tab_index = 0
                #story.selected_main_tab_index = 0
                
            # Temporary
            #formatted_main_pin = ft.Tabs(
                #selected_index=selected_tab_index,
                #animation_duration=0,
                #expand=True,  # Layout engine breaks Tabs inside of Columns if this expand is not set
                #divider_color=ft.Colors.TRANSPARENT,
                #padding=ft.padding.all(0),
                #label_padding=ft.padding.all(0),
                #mouse_cursor=ft.MouseCursor.BASIC,
                #tabs=[]    # Gives our tab control here   
            #)
            #for control in visible_main_controls:
                #formatted_main_pin.tabs.append(control.tab)
        #else:
            #formatted_main_pin = story.main_pin
        


        # Method called when our divider (inside a gesture detector) is dragged
        # Updates the size of our pin in the story object
        def move_top_pin_divider(e: ft.DragUpdateEvent):
            print("move top pin divider called")
            #if (e.delta_y > 0 and story.top_pin.height < page.height/2) or (e.delta_y < 0 and story.top_pin.height > 200):
                #story.top_pin.height += e.delta_y
                #top_pin_drag_target.content.height = story.top_pin.height  # Update the drag target height to match the pin height
            #formatted_top_pin.update()
            #story.widgets.update() # Update the main pin, as it is affected by all pins resizing
            #story.master_stack.update()
        #def save_top_pin_height(e: ft.DragEndEvent):
            print("save top pin height called")
            #app.active_story.data['top_pin_height'] = story.top_pin.height
            #app.active_story.save_dict()
            

        # The control that holds our divider, which we drag to resize the top pin
        top_pin_resizer = ft.GestureDetector(
            content=ft.Container(
                height=10,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
            ),
            on_pan_update=move_top_pin_divider,
            #on_pan_end=save_top_pin_height,
            on_hover=show_vertical_cursor,
        )

        # Left pin reisizer method and variable
        def move_left_pin_divider(e: ft.DragUpdateEvent):
            print("move left pin divider called")
            #if (e.delta_x > 0 and story.left_pin.width < page.width/2) or (e.delta_x < 0 and story.left_pin.width > 200):
                #story.left_pin.width += e.delta_x
            #formatted_left_pin.update()
            #story.widgets.update()
            #story.master_stack.update()
        def save_left_pin_width(e: ft.DragEndEvent):
            print("save left pin width called")
            #app.active_story.data['left_pin_width'] = story.left_pin.width
            #app.active_story.save_dict()
        left_pin_resizer = ft.GestureDetector(
            content=ft.Container(
                width=10,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
            ),
            on_pan_update=move_left_pin_divider,
            on_pan_end=save_left_pin_width,
            on_hover=show_horizontal_cursor,
        )
        
        # No resizer for main pin, as it is always expanded and takes up the rest of the space

        # Right pin resizer method and variable
        def move_right_pin_divider(e: ft.DragUpdateEvent):
            print("move right pin divider called")
            #if (e.delta_x < 0 and story.right_pin.width < page.width/2) or (e.delta_x > 0 and story.right_pin.width > 200):
                #story.right_pin.width -= e.delta_x
            #formatted_right_pin.update()
            #story.widgets.update()
            #story.master_stack.update()
        def save_right_pin_width(e: ft.DragEndEvent):
            print("save right pin width called")    
            #app.active_story.data['right_pin_width'] = story.right_pin.width
            #app.active_story.save_dict()
        right_pin_resizer = ft.GestureDetector(
            content=ft.Container(
                width=10,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
            ),
            on_pan_update=move_right_pin_divider,
            on_pan_end=save_right_pin_width,
            on_hover=show_horizontal_cursor,
        )

        # Bottom pin resizer method and variable
        def move_bottom_pin_divider(e: ft.DragUpdateEvent):
            print("move bottom pin divider called")
            #if (e.delta_y < 0 and story.bottom_pin.height < page.height/2) or (e.delta_y > 0 and story.bottom_pin.height > 200):
                #story.bottom_pin.height -= e.delta_y
            #formatted_bottom_pin.update()
            #story.widgets.update()
            #story.master_stack.update()
        def save_bottom_pin_height(e: ft.DragEndEvent):
            print("save bottom pin height called")
            #app.active_story.data['bottom_pin_height'] = story.bottom_pin.height
            #app.active_story.save_dict()
        bottom_pin_resizer = ft.GestureDetector(
            content=ft.Container(
                height=10,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
            ),
            on_pan_update=move_bottom_pin_divider,
            on_pan_end=save_bottom_pin_height,
            on_hover=show_vertical_cursor,
        )


        '''
        # Formatted pin locations that hold our pins, and our resizer gesture detectors.
        # Main pin is always expanded and has no resizer, so it doesnt need to be formatted
        formatted_top_pin = ft.Column(spacing=0, controls=[story.top_pin, top_pin_resizer])
        formatted_left_pin = ft.Row(spacing=0, controls=[story.left_pin, left_pin_resizer]) 
        formatted_right_pin = ft.Row(spacing=0, controls=[right_pin_resizer, story.right_pin])  # Right pin formatting row
        formatted_bottom_pin = ft.Column(spacing=0, controls=[bottom_pin_resizer, story.bottom_pin])  # Bottom pin formatting column

        # Check if our pins have any visible widgets or not, so if they should show up on screen
        # Check if top pin is empty. If yes, hide the formatted pin
        if len(story.top_pin.controls) == 0:
            formatted_top_pin.visible = False
        # If top pin not empty, make sure there is at least one visible widget
        elif all(obj.visible == False for obj in story.top_pin.controls[:]):
            formatted_top_pin.visible = False
        else:   # If not empty, check if any of the widgets are visible
            for obj in story.top_pin.controls:
                if obj.visible == True:     # If any widgets are visible, show our formatted pin
                    formatted_top_pin.visible = True
                    break   # No need to keep checking if at least one is visible
            # Makes sure our height is set correctly
            if story.top_pin.height < minimum_pin_height:
                story.top_pin.height = minimum_pin_height

        # Left pin
        if len(story.left_pin.controls) == 0:
            formatted_left_pin.visible = False
        elif all(obj.visible == False for obj in story.left_pin.controls[:]):
            formatted_left_pin.visible = False
        else:
            for obj in story.left_pin.controls:
                if obj.visible == True:
                    formatted_left_pin.visible = True
                    break
            if story.left_pin.width < minimum_pin_width:
                story.left_pin.width = minimum_pin_width

        # Right pin
        if len(story.right_pin.controls) == 0:
            formatted_right_pin.visible = False
        elif all(obj.visible == False for obj in story.right_pin.controls[:]):
            formatted_right_pin.visible = False
        else:
            for obj in story.right_pin.controls:
                if obj.visible == True:
                    formatted_right_pin.visible = True
                    break
            if story.right_pin.width < minimum_pin_width:
                story.right_pin.width = minimum_pin_width

        # Bottom pin
        if len(story.bottom_pin.controls) == 0:
            formatted_bottom_pin.visible = False
        elif all(obj.visible == False for obj in story.bottom_pin.controls[:]):
            formatted_bottom_pin.visible = False
        else:
            for obj in story.bottom_pin.controls:
                if obj.visible == True:
                    formatted_bottom_pin.visible = True
                    break
            if story.bottom_pin.height < minimum_pin_height:
                story.bottom_pin.height = minimum_pin_height

        # Format our pins on the page
        story.widgets.controls.clear()
        story.widgets.controls = [
            formatted_left_pin,    # formatted left pin
            ft.Column(
                expand=True, spacing=0, 
                controls=[
                    formatted_top_pin,    # formatted top pin
                    formatted_main_pin,     # main work area with widgets
                    formatted_bottom_pin,     # formatted bottom pin
            ]),
            formatted_right_pin,    # formatted right pin
        ]
        '''
        page.update()
        




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
            #content=story.master_stack,   
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
