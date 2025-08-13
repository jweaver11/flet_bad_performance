'''
Render our widgets on the screen based on their pins.
This also handles logic for dragging widgets into different pins and relocating them.
'''
import flet as ft
from models.user import user
import json
from handlers.arrange_widgets import arrange_widgets

story = user.active_story # Get our story object from the user

# When a draggable starts dragging, we add our drag targets to the master stack
def show_pin_drag_targets(e):
    
    # Only add drag targets if they're not already in the stack
    if pin_drag_targets not in story.master_stack.controls:
        story.master_stack.controls.extend(pin_drag_targets)
        story.master_stack.update()
    else:
        print("drag targets already in master stack. This is an error")

# Called whenever a drag target accepts a draggable
# Removes our drag targets from the stack, otherwise they sit overtop our widgets and break the program
def remove_drag_targets():
    print("remove drag_targets called")
    # Remove all our drag targets when a drag is complete
    for target in pin_drag_targets:
        if target in story.master_stack.controls:
            story.master_stack.controls.remove(target)
    story.master_stack.update()

# Called when a draggable hovers over a drag target before dropping
# Makes the drag target visible to notify users they can drop here
def on_hover_pin_drag_target(e):
    # e.control = whichever drag target is calling this method
    e.control.content.opacity = .5
    e.control.content.update()
    print("Hovered over a drag target")
    
# Called when a draggable leaves a drag target
# Makes the drag target invisible again
def on_leave_pin(e):
    e.control.content.opacity = 0
    e.control.content.update()
    print("Left a drag target")


# Accepting drags for our five pin locations
def top_pin_drag_accept(e):
    # Reset our container to be invisible again
    e.control.content.opacity = 0
    e.control.content.update()

    remove_drag_targets()  # Remove our drag targets from the stack, since we have completed our drag

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
    object.pin_location = "top"
    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    
    print("top pin accepted")

# Left drag accept
def left_pin_drag_accept(e):
    e.control.content.opacity = 0
    e.control.content.update()

    remove_drag_targets() 

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

    object.pin_location = "left"
    arrange_widgets()       
    render_widgets(e.page)  
    
    print("left pin accepted")

# Main drag accept
def main_pin_drag_accept(e):
    e.control.content.opacity = 0
    e.control.content.update()
    
    remove_drag_targets() 

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

    object.pin_location = "main"
    arrange_widgets()       
    render_widgets(e.page)  
    
    print("main pin accepted")

# Right drag accept
def right_pin_drag_accept(e):
    e.control.content.opacity = 0
    e.control.content.update()
    
    remove_drag_targets() 

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

    object.pin_location = "right"
    arrange_widgets()       
    render_widgets(e.page)  
    
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    e.control.content.opacity = 0
    e.control.content.update()
    
    remove_drag_targets() 

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

    object.pin_location = "bottom"
    arrange_widgets()       
    render_widgets(e.page)  
    
    print("bottom pin accepted")



# set minimumm fallbacks for our pins, and our drag targets
minimum_pin_height = 200
minimum_pin_width = 230

# Pin drag targets
top_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Container(expand=True, height=minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0), 
    on_accept=top_pin_drag_accept, on_will_accept=on_hover_pin_drag_target, on_leave=on_leave_pin,
)
left_pin_drag_target = ft.DragTarget(
    group="widgets",
    content=ft.Container(expand=True, height=minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0), 
    on_accept=left_pin_drag_accept, on_will_accept=on_hover_pin_drag_target, on_leave=on_leave_pin,
)
main_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Container(expand=True, height=minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0), 
    on_accept=main_pin_drag_accept, on_will_accept=on_hover_pin_drag_target, on_leave=on_leave_pin,
)
right_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Container(expand=True, height=minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0), 
    on_accept=right_pin_drag_accept, on_will_accept=on_hover_pin_drag_target, on_leave=on_leave_pin,
)
bottom_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Container(expand=True, height=minimum_pin_height, bgcolor=ft.Colors.WHITE, opacity=0),
    on_accept=bottom_pin_drag_accept, on_will_accept=on_hover_pin_drag_target, on_leave=on_leave_pin,
)

# List of Controls (Containers) that hold our drag targets we just created
# Must be in containers in order to position them inside the stack
# Surrounding drag target is on the bottom
pin_drag_targets = [
    ft.Container(
        content=top_pin_drag_target,
        height=200,
        top=0, left=200, right=200, 
    ),
    ft.Container(
        content=left_pin_drag_target,
        width=200,
        left=0, top=0, bottom=0,
    ),
    ft.Container(
        content=main_pin_drag_target,
        top=200, left=200, right=200, bottom=200, 
    ),
    ft.Container(
        content=right_pin_drag_target,
        width=200,
        right=0, top=0, bottom=0, 
    ),
    ft.Container(
        content=bottom_pin_drag_target,
        height=200,
        bottom=0, left=200, right=200,
    ),
]
print("render_widgets called")


# Pin our widgets in here for formatting
def render_widgets(page: ft.Page):

    # Runs our arrange widgets function to make sure all widgets are in correct locations
    arrange_widgets()

    # Change our cursor when we hover over a resizer (divieder). Either vertical or horizontal
    def show_vertical_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        e.control.update()
    def show_horizontal_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Method called when our divider (inside a gesture detector) is dragged
    # Updates the size of our pin in the story object
    def move_top_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_y > 0 and story.top_pin.height < page.height/2) or (e.delta_y < 0 and story.top_pin.height > 200):
            story.top_pin.height += e.delta_y
        formatted_top_pin.update()
        story.widgets.update() # Update the main pin, as it is affected by all pins resizing
        story.master_stack.update()

    # The control that holds our divider, which we drag to resize the top pin
    top_pin_resizer = ft.GestureDetector(
        content=ft.Divider(thickness=1, height=10, opacity=.7, color=ft.Colors.PRIMARY),
        on_pan_update=move_top_pin_divider,
        on_hover=show_vertical_cursor,
    )

    # Left pin reisizer method and variable
    def move_left_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and story.left_pin.width < page.width/2) or (e.delta_x < 0 and story.left_pin.width > 200):
            story.left_pin.width += e.delta_x
        formatted_left_pin.update()
        story.widgets.update()
        story.master_stack.update()
    left_pin_resizer = ft.GestureDetector(
        content=ft.VerticalDivider(thickness=1, width=10, opacity=.7, color=ft.Colors.PRIMARY),  # Makes it invisible
        on_pan_update=move_left_pin_divider,
        on_hover=show_horizontal_cursor,
    )
    
    # No resizer for main pin, as it is always expanded and takes up the rest of the space

    # Right pin resizer method and variable
    def move_right_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_x < 0 and story.right_pin.width < page.width/2) or (e.delta_x > 0 and story.right_pin.width > 200):
            story.right_pin.width -= e.delta_x
        formatted_right_pin.update()
        story.widgets.update()
        story.master_stack.update()
    right_pin_resizer = ft.GestureDetector(
        content=ft.VerticalDivider(thickness=1, width=10, opacity=.7, color=ft.Colors.PRIMARY),  # color=ft.Colors.TRANSPARENT
        on_pan_update=move_right_pin_divider,
        on_hover=show_horizontal_cursor,
    )

    # Bottom pin resizer method and variable
    def move_bottom_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_y < 0 and story.bottom_pin.height < page.height/2) or (e.delta_y > 0 and story.bottom_pin.height > 200):
            story.bottom_pin.height -= e.delta_y
        formatted_bottom_pin.update()
        story.widgets.update()
        story.master_stack.update()
    bottom_pin_resizer = ft.GestureDetector(
        content=ft.Divider(thickness=1, height=10, opacity=.7, color=ft.Colors.PRIMARY),
        on_pan_update=move_bottom_pin_divider,
        on_hover=show_vertical_cursor,
    )

    
    # Formatted pin locations that hold our drag targets, and our resizer gesture detectors.
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
                story.main_pin,     # main work area with widgets
                formatted_bottom_pin     # formatted bottom pin
        ]),
        formatted_right_pin,    # formatted right pin
    ]
    page.update()


# Add stack so drag targets are same size as pin??