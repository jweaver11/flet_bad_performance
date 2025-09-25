'''
UI styling for the main workspace area of appliction that holds our widgets (tabs)
Returns our container with our formatting areas inside the workspace area.
The stories 'mast_stack' holds our 'master_row', which contains our five pins: top, left, main, right, and bottom.
Overtop that, we append our drag targets when we start dragging a widget (tab). Thats why its a stack
'''

import flet as ft
from models.app import app
from models.story import Story
import json

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

        self.p = page
        self.story = story

        self.minimum_pin_height = 200
        self.minimum_pin_width = 230

        # Creates our 5 pin locations for our widgets inside our workspace
        self.top_pin = ft.Row(spacing=0, height=story.data['top_pin_height'], controls=[])
        self.left_pin = ft.Column(spacing=0, width=story.data['left_pin_width'], controls=[])
        self.main_pin = ft.Row(expand=True, spacing=0, controls=[])
        self.right_pin = ft.Column(spacing=0, width=story.data['right_pin_width'], controls=[])
        self.bottom_pin = ft.Row(spacing=0, height=story.data['bottom_pin_height'], controls=[])

        # Add our settings to the main pin whenver a new story is loaded or created
        self.main_pin.controls.append(app.settings)

        # Our master row that holds all our widgets
        self.widgets = ft.Row(spacing=0, expand=True, controls=[])

        # Master stack that holds our widgets ^ row. We add our drag targets overtop our widgets, so we use a stack here
        # And our drag targets when we start dragging widgets.
        # We use global stack like this so there is always a drag target, even if a pin is empty
        self.master_stack = ft.Stack(expand=True, controls=[self.widgets])

        # Pin drag targets
        self.top_pin_drag_target = ft.DragTarget(
            group="widgets", 
            content=ft.Container(expand=True, bgcolor=ft.Colors.WHITE, opacity=0), 
            on_accept=self.top_pin_drag_accept, on_will_accept=self.on_hover_pin_drag_target, on_leave=self.on_stop_hover_drag_target,
        )
        self.left_pin_drag_target = ft.DragTarget(
            group="widgets",
            content=ft.Container(expand=True, width=self.minimum_pin_width, bgcolor=ft.Colors.WHITE, opacity=0), 
            on_accept=self.left_pin_drag_accept, on_will_accept=self.on_hover_pin_drag_target, on_leave=self.on_stop_hover_drag_target,
        )
        self.main_pin_drag_target = ft.DragTarget(
            group="widgets", 
            content=ft.Container(expand=True, height=self.minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0), 
            on_accept=self.main_pin_drag_accept, on_will_accept=self.on_hover_pin_drag_target, on_leave=self.on_stop_hover_drag_target,
        )
        self.right_pin_drag_target = ft.DragTarget(
            group="widgets", 
            content=ft.Container(expand=True, width=self.minimum_pin_width, bgcolor=ft.Colors.WHITE, opacity=0), 
            on_accept=self.right_pin_drag_accept, on_will_accept=self.on_hover_pin_drag_target, on_leave=self.on_stop_hover_drag_target,
        )
        self.bottom_pin_drag_target = ft.DragTarget(
            group="widgets", 
            content=ft.Container(expand=True, height=self.minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0),
            on_accept=self.bottom_pin_drag_accept, on_will_accept=self.on_hover_pin_drag_target, on_leave=self.on_stop_hover_drag_target,
        )

        self.pin_drag_targets = [
            ft.Container(
                expand=True,
                content=self.main_pin_drag_target,
                top=200, left=200, right=200, bottom=200, 
            ),
            ft.Container(
                content=self.top_pin_drag_target,
                height=200,
                top=0, left=0, right=0, 
            ),
            ft.Container(
                content=self.bottom_pin_drag_target,
                height=200,
                bottom=0, left=0, right=0,
            ),
            ft.Container(
                content=self.left_pin_drag_target,
                width=220,
                left=0, top=0, bottom=0,
            ),
            ft.Container(
                content=self.right_pin_drag_target,
                width=220,
                right=0, top=0, bottom=0, 
            ),
            
        ]


        # We call this in the story build_view, since it errors out here if the object is not fully built yet
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


        # Rendering adds dividers between each widget. So if we remove old ones here
        self.top_pin.controls = [control for control in self.top_pin.controls if type(control) != ft.GestureDetector]
        self.left_pin.controls = [control for control in self.left_pin.controls if type(control) != ft.GestureDetector]
        self.right_pin.controls = [control for control in self.right_pin.controls if type(control) != ft.GestureDetector]
        self.bottom_pin.controls = [control for control in self.bottom_pin.controls if type(control) != ft.GestureDetector]

        # Create gesture detector dividers and insert them between each visible control. Start with top pin
        visible_top_controls = [control for control in self.top_pin.controls if getattr(control, 'visible', True)]
        if len(visible_top_controls) > 1:
            # Work backwards to avoid index shifting issues when inserting
            # Find positions of visible controls in the original list and insert dividers between them
            visible_indices = [i for i, control in enumerate(self.top_pin.controls) if getattr(control, 'visible', True)]
            for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                insert_position = visible_indices[i]
                gd = ft.GestureDetector(
                    content=ft.Container(
                        width=10,
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                        content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
                    ),
                    on_hover=show_horizontal_cursor,
                    #on_pan_update=resize the left pin controls
                )
                self.top_pin.controls.insert(insert_position, gd)
        
        # Left pin
        visible_left_controls = [control for control in self.left_pin.controls if getattr(control, 'visible', True)]
        if len(visible_left_controls) > 1:
            
            visible_indices = [i for i, control in enumerate(self.left_pin.controls) if getattr(control, 'visible', True)]
            for i in range(len(visible_indices) - 1, 0, -1):
                insert_position = visible_indices[i]
                gd = ft.GestureDetector(
                    content=ft.Container(
                        height=10,
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                        content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
                    ),
                    on_hover=show_vertical_cursor,
                    #on_pan_update=resize the left pin controls
                )
                self.left_pin.controls.insert(insert_position, gd)


        # Right pin
        visible_right_controls = [control for control in self.right_pin.controls if getattr(control, 'visible', True)]
        if len(visible_right_controls) > 1:
            visible_indices = [i for i, control in enumerate(self.right_pin.controls) if getattr(control, 'visible', True)]
            for i in range(len(visible_indices) - 1, 0, -1):
                
                insert_position = visible_indices[i]
                gd = ft.GestureDetector(
                    content=ft.Container(
                        height=10,
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                        content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
                    ),
                    on_hover=show_vertical_cursor,
                    #on_hover=do_nothing,  # No hover effect for left pin
                )
                self.right_pin.controls.insert(insert_position, gd)

        # bottom pin
        visible_bottom_controls = [control for control in self.bottom_pin.controls if getattr(control, 'visible', True)]
        if len(visible_bottom_controls) > 1:
            visible_indices = [i for i, control in enumerate(self.bottom_pin.controls) if getattr(control, 'visible', True)]
            for i in range(len(visible_indices) - 1, 0, -1):
                # Insert divider after the (i-1)th visible control
                insert_position = visible_indices[i]
                gd = ft.GestureDetector(
                    content=ft.Container(
                        width=10,
                        bgcolor=ft.Colors.TRANSPARENT,
                        padding=ft.padding.only(left=8),  # Push the 2px divider to the right side
                        content=ft.VerticalDivider(thickness=2, width=2, color=ft.Colors.PRIMARY, opacity=.5)
                    ),
                    on_hover=show_horizontal_cursor,
                    #on_hover=do_nothing,  # No hover effect for left pin
                )
                self.bottom_pin.controls.insert(insert_position, gd)


        # Main pin is rendered as a tab control, so we won't use dividers and will use different logic
        visible_main_controls = [control for control in self.main_pin.controls if getattr(control, 'visible', True)]
        if len(visible_main_controls) > 1:
            # Get the selected tab index from the story object, default to 0
            selected_tab_index = getattr(story, 'selected_main_tab_index', 0)
            # Ensure the index is within bounds
            if selected_tab_index >= len(visible_main_controls):
                selected_tab_index = 0
                self.selected_main_tab_index = 0
                
            # Temporary
            formatted_main_pin = ft.Tabs(
                selected_index=selected_tab_index,
                animation_duration=0,
                expand=True,  # Layout engine breaks Tabs inside of Columns if this expand is not set
                divider_color=ft.Colors.TRANSPARENT,
                padding=ft.padding.all(0),
                label_padding=ft.padding.all(0),
                mouse_cursor=ft.MouseCursor.BASIC,
                tabs=[]    # Gives our tab control here   
            )
            for control in visible_main_controls:
                formatted_main_pin.tabs.append(control.tab)
        else:
            formatted_main_pin = self.main_pin
        


        # Method called when our divider (inside a gesture detector) is dragged
        # Updates the size of our pin in the story object
        def move_top_pin_divider(e: ft.DragUpdateEvent):
            #print("move top pin divider called")
            if (e.delta_y > 0 and self.top_pin.height < page.height/2) or (e.delta_y < 0 and self.top_pin.height > 200):
                self.top_pin.height += e.delta_y
                self.top_pin_drag_target.content.height = self.top_pin.height  # Update the drag target height to match the pin height
            formatted_top_pin.update()
            self.widgets.update() # Update the main pin, as it is affected by all pins resizing
            self.master_stack.update()
        def save_top_pin_height(e: ft.DragEndEvent):
            #print("save top pin height called")
            story.data['top_pin_height'] = self.top_pin.height
            story.save_dict()
            

        # The control that holds our divider, which we drag to resize the top pin
        top_pin_resizer = ft.GestureDetector(
            content=ft.Container(
                height=10,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.only(top=8),  # Push the 2px divider to the right side
                content=ft.Divider(thickness=2, height=2, color=ft.Colors.PRIMARY, opacity=.5)
            ),
            on_pan_update=move_top_pin_divider,
            on_pan_end=save_top_pin_height,
            on_hover=show_vertical_cursor,
        )

        # Left pin reisizer method and variable
        def move_left_pin_divider(e: ft.DragUpdateEvent):
            #print("move left pin divider called")
            if (e.delta_x > 0 and self.left_pin.width < page.width/2) or (e.delta_x < 0 and self.left_pin.width > 200):
                self.left_pin.width += e.delta_x
            formatted_left_pin.update()
            self.widgets.update()
            self.master_stack.update()
        def save_left_pin_width(e: ft.DragEndEvent):
            #print("save left pin width called")
            story.data['left_pin_width'] = self.left_pin.width
            story.save_dict()
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
            #print("move right pin divider called")
            if (e.delta_x < 0 and self.right_pin.width < page.width/2) or (e.delta_x > 0 and self.right_pin.width > 200):
                self.right_pin.width -= e.delta_x
            formatted_right_pin.update()
            self.widgets.update()
            self.master_stack.update()
        def save_right_pin_width(e: ft.DragEndEvent):
            print("save right pin width called")    
            story.data['right_pin_width'] = self.right_pin.width
            story.save_dict()
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
            #print("move bottom pin divider called")
            if (e.delta_y < 0 and self.bottom_pin.height < page.height/2) or (e.delta_y > 0 and self.bottom_pin.height > 200):
                self.bottom_pin.height -= e.delta_y
            formatted_bottom_pin.update()
            self.widgets.update()
            self.master_stack.update()
        def save_bottom_pin_height(e: ft.DragEndEvent):
            print("save bottom pin height called")
            story.data['bottom_pin_height'] = self.bottom_pin.height
            story.save_dict()
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


        
        # Formatted pin locations that hold our pins, and our resizer gesture detectors.
        # Main pin is always expanded and has no resizer, so it doesnt need to be formatted
        formatted_top_pin = ft.Column(spacing=0, controls=[self.top_pin, top_pin_resizer])
        formatted_left_pin = ft.Row(spacing=0, controls=[self.left_pin, left_pin_resizer]) 
        formatted_right_pin = ft.Row(spacing=0, controls=[right_pin_resizer, self.right_pin])  # Right pin formatting row
        formatted_bottom_pin = ft.Column(spacing=0, controls=[bottom_pin_resizer, self.bottom_pin])  # Bottom pin formatting column

        # Check if our pins have any visible widgets or not, so if they should show up on screen
        # Check if top pin is empty. If yes, hide the formatted pin
        if len(self.top_pin.controls) == 0:
            formatted_top_pin.visible = False
        # If top pin not empty, make sure there is at least one visible widget
        elif all(obj.visible == False for obj in self.top_pin.controls[:]):
            formatted_top_pin.visible = False
        else:   # If not empty, check if any of the widgets are visible
            for obj in self.top_pin.controls:
                if obj.visible == True:     # If any widgets are visible, show our formatted pin
                    formatted_top_pin.visible = True
                    break   # No need to keep checking if at least one is visible
            # Makes sure our height is set correctly
            if self.top_pin.height < self.minimum_pin_height:
                self.top_pin.height = self.minimum_pin_height

        # Left pin
        if len(self.left_pin.controls) == 0:
            formatted_left_pin.visible = False
        elif all(obj.visible == False for obj in self.left_pin.controls[:]):
            formatted_left_pin.visible = False
        else:
            for obj in self.left_pin.controls:
                if obj.visible == True:
                    formatted_left_pin.visible = True
                    break
            if self.left_pin.width < self.minimum_pin_width:
                self.left_pin.width = self.minimum_pin_width

        # Right pin
        if len(self.right_pin.controls) == 0:
            formatted_right_pin.visible = False
        elif all(obj.visible == False for obj in self.right_pin.controls[:]):
            formatted_right_pin.visible = False
        else:
            for obj in self.right_pin.controls:
                if obj.visible == True:
                    formatted_right_pin.visible = True
                    break
            if self.right_pin.width < self.minimum_pin_width:
                self.right_pin.width = self.minimum_pin_width

        # Bottom pin
        if len(self.bottom_pin.controls) == 0:
            formatted_bottom_pin.visible = False
        elif all(obj.visible == False for obj in self.bottom_pin.controls[:]):
            formatted_bottom_pin.visible = False
        else:
            for obj in self.bottom_pin.controls:
                if obj.visible == True:
                    formatted_bottom_pin.visible = True
                    break
            if self.bottom_pin.height < self.minimum_pin_height:
                self.bottom_pin.height = self.minimum_pin_height

        # Format our pins on the page
        self.widgets.controls.clear()
        self.widgets.controls = [
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

        # Set the master_stack as the content of this container
        self.content = self.master_stack
        
        page.update()

    # When a draggable starts dragging, we add our drag targets to the master stack
    def show_pin_drag_targets(self):
        #print("show_pin_drag_targets called")
        
        # Only add drag targets if they're not already in the stack
        if self.pin_drag_targets not in self.master_stack.controls:
            self.master_stack.controls.extend(self.pin_drag_targets)
            self.master_stack.update()
        else:
            print("drag targets already in master stack. This is an error")

        self.p.update()


    # Called whenever a drag target accepts a draggable
    # Removes our drag targets from the stack, otherwise they sit overtop our widgets and break the program
    def remove_drag_targets(self):
        #print("remove drag_targets called")
        # Remove all our drag targets when a drag is complete
        for target in self.pin_drag_targets:
            if target in self.master_stack.controls:
                self.master_stack.controls.remove(target)
        self.master_stack.update()

    # Called when a draggable hovers over a drag target before dropping
    # Makes the drag target visible to notify apps they can drop here
    def on_hover_pin_drag_target(self, e):
        # e.control = whichever drag target is calling this method
        e.control.content.opacity = .5
        e.control.content.update()
        #print("Hovered over a drag target")
        
    # Called when a draggable leaves a drag target
    # Makes the drag target invisible again
    def on_stop_hover_drag_target(self, e):
        e.control.content.opacity = 0
        e.control.content.update()
        #print("Left a drag target")


    # Accepting drags for our five pin locations
    def top_pin_drag_accept(self, e):
        # Reset our container to be invisible again
        e.control.content.opacity = 0
        e.control.content.update()

        self.remove_drag_targets()  # Remove our drag targets from the stack, since we have completed our drag

        # Grab our object from e.data, which is is a JSON string, so we have to parse it
        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            # Get the Draggable control by ID. our object is stored in its data
            draggable = e.page.get_control(src_id)
            if draggable:
                # Set object variable to our object
                object = draggable.data
                #print("object:\n", object) 
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")

        # Set our objects pin location to the correct new location, and then call our arrange_widgets function
        if hasattr(object, 'data') and object.data:
            object.data['pin_location'] = "top"  # Update our object's data dictionary as well
            object.save_dict()  # Save our object with its new pin location

        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets(self.story)       # Re-arrange our widgets held in the story object
        self.reload_workspace(self.p, self.story)  # Re-render the widgets to reflect the new pin location
        
        print("top pin accepted")

    # Left drag accept
    def left_pin_drag_accept(self, e):
        e.control.content.opacity = 0
        e.control.content.update()

        self.remove_drag_targets() 

        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")

        if hasattr(object, 'data') and object.data:
            object.data['pin_location'] = "left"
            object.save_dict()

        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets(self.story)       
        self.reload_workspace(self.p, self.story) 
        
        print("left pin accepted")

    # Main drag accept
    def main_pin_drag_accept(self, e):
        e.control.content.opacity = 0
        e.control.content.update()
        
        self.remove_drag_targets() 

        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")

        object.data['pin_location'] = "main"
        object.save_dict()
        
        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets(self.story)       
        self.reload_workspace(self.p, self.story) 
        
        print("main pin accepted")

    # Right drag accept
    def right_pin_drag_accept(self, e):
        e.control.content.opacity = 0
        e.control.content.update()
        
        self.remove_drag_targets() 

        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")

        object.data['pin_location'] = "right"
        object.save_dict()

        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets(self.story)       
        self.reload_workspace(self.p, self.story)  
        
        print("right pin accepted")

    def bottom_pin_drag_accept(self, e):
        e.control.content.opacity = 0
        e.control.content.update()
        
        self.remove_drag_targets() 

        event_data = json.loads(e.data)
        src_id = event_data.get("src_id")
        
        if src_id:
            draggable = e.page.get_control(src_id)
            if draggable:
                object = draggable.data
            else:
                print("Could not find control with src_id:", src_id)
        else:
            print("src_id not found in event data")

        object.data['pin_location'] = "bottom"
        object.save_dict()

        from handlers.arrange_widgets import arrange_widgets
        arrange_widgets(self.story)       
        self.reload_workspace(self.p, self.story)  
        
        print("bottom pin accepted")
        



# Called to create our workspace whenever there is NO active story or no stories at all
def create_workspace(page: ft.Page) -> ft.Container:   

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
                ft.TextButton("Cancel", on_click=close_dialog, style=ft.ButtonStyle(color=ft.Colors.ERROR)),
                ft.TextButton("Create", on_click=lambda e: submit_new_story(story_title_field)),
            ],
        )

        # Open our dialog in the overlay
        dlg.open = True
        page.overlay.append(dlg)
        page.update()


    
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
