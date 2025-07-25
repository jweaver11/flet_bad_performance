'''
Layout our widgets whenever there is more than 2
'''
import flet as ft
from models.user import user
import json
from handlers.arrange_widgets import arrange_widgets

story = user.active_story # Get our story object from the user

# Accepting drags for our five pin locations
def top_pin_drag_accept(e):
    # e.data is a JSON string, so we have to parse it
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        # Get the Draggable control by ID. our object is stored in its data
        draggable = e.page.get_control(src_id)
        if draggable:
            # Set object variable to our object
            object = draggable.data
            #print("object:\n", object) 
        #else:
            #print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "top"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()

    # Properly reset the stack
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    master_stack.update()
    print("top pin accepted")

def left_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
        #else:
            #print("Could not find control with src_id:", src_id)
    else:
       print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "left"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()

    # Properly reset the stack
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    master_stack.update()
    print("left pin accepted")

def main_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
        #else:
            #print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "main"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    
    # Reset the drag target appearance but don't clear it completely
    e.control.content = ft.Row(height=minimum_pin_height)
    e.control.update()
    
    # Properly reset the stack
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    master_stack.update()
    
    print("main pin accepted")


def right_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
        #else:
            #print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "right"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()

    # Properly reset the stack
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    master_stack.update()
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            #print("object:\n", object) 
        #else:
            #print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "bottom"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()

    # Properly reset the stack
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    master_stack.update()
    print("bottom pin accepted")

# Drag target to catch draggable drops between the drag targets
def ib_drag_accept(e):
    e.control.content = ft.Row(height=minimum_pin_height)
    e.control.update()
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)  # Re-add the widget row to the stack
    master_stack.update()
    print("ib drag target accepted")

# When a draggable is hovering over a target
def drag_will_accept(e):
    e.control.content = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
        height=minimum_pin_height
    )
    e.control.update()
    
    # Clear the stack and rebuild it properly
    master_stack.controls.clear()
    master_stack.controls.append(master_widget_row)
    
    # Only add drag targets if they're not already in the stack
    for target in pin_drag_targets:
        if target not in master_stack.controls:
            master_stack.controls.append(target)
    
    master_stack.update()

# When a draggable leaves a target
def on_leave(e):
    #print("Left a pin drag target")
    e.control.content = ft.Row(height=300)
    e.control.update()
    master_stack.update()


# set minimumm fallbacks for our pins
#min_pin_height = 30
#min_pin_width = 30
minimum_pin_height = 200
minimum_pin_width = 200

# Our 5 pin area drag targets
in_between_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=ib_drag_accept,
    on_leave=on_leave,
)
# Pin drag targets
top_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=top_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
left_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=left_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
main_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=main_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
right_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=right_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)
bottom_pin_drag_target = ft.DragTarget(
    group="widgets", 
    content=ft.Row(), 
    on_accept=bottom_pin_drag_accept, on_will_accept=drag_will_accept, on_leave=on_leave,
)

def hide_pin_drag_targets():
    for target in pin_drag_targets:
        target.visible = False
        target.update()

# containers for our pin drag targets
pin_drag_targets = [    # Must be in flet containers in order to position them
    ft.Container(
        content=in_between_drag_target,
        expand=True,
        margin=ft.margin.all(10),
        border_radius=ft.border_radius.all(10),
        top=0, left=0, right=0, bottom=0,       # Position them in their container
    ),
    ft.Container(
        content=top_pin_drag_target,
        height=200,
        margin=ft.margin.only(left=20, right=20),
        top=0, left=200, right=200,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=left_pin_drag_target,
        width=200,
        left=0, top=0, bottom=0,
        border_radius=ft.border_radius.all(10), 
    ),
    ft.Container(
        content=main_pin_drag_target,
        margin=ft.margin.only(top=20, left=20, right=20, bottom=20,),
        top=200, left=200, right=200, bottom=200,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=right_pin_drag_target,
        width=200,
        right=0, top=0, bottom=0,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=bottom_pin_drag_target,
        height=200,
        bottom=0, left=200, right=200,
        margin=ft.margin.only(left=20, right=20),
        border_radius=ft.border_radius.all(10), 
    ),
]

# Master row that holds all our widgets
master_widget_row = ft.Row(
    spacing=0,
    expand=True,
    controls=[]
)

# Stack that holds our widget row, and the drag targets overtop them when it needs to
master_stack = ft.Stack(expand=True, controls=[master_widget_row])

# Pin our widgets in here for formatting
def render_widgets(page: ft.Page):
    print("render_widgets called")

    # Change our cursor when we hover over a divider. Either vertical or horizontal
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
        master_widget_row.update() # Update the main pin, as it is affected by all pins resizing
        master_stack.update()

    # Holds the divider that is draggable to resize the top pin
    top_pin_resizer = ft.GestureDetector(
        content=ft.Divider(color=ft.Colors.PRIMARY, height=10, thickness=10),
        on_pan_update=move_top_pin_divider,
        on_hover=show_vertical_cursor,
    )

    # Left pin reisizer
    def move_left_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and story.left_pin.width < page.width/2) or (e.delta_x < 0 and story.left_pin.width > 200):
            story.left_pin.width += e.delta_x
        formatted_left_pin.update()
        master_widget_row.update()
        master_stack.update()
    left_pin_resizer = ft.GestureDetector(
        content=ft.VerticalDivider(thickness=10, width=10, color=ft.Colors.PRIMARY),  # color=ft.Colors.TRANSPARENT
        on_pan_update=move_left_pin_divider,
        on_hover=show_horizontal_cursor,
    )

    # Right pin resizer
    def move_right_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_x < 0 and story.right_pin.width < page.width/2) or (e.delta_x > 0 and story.right_pin.width > 200):
            story.right_pin.width -= e.delta_x
        formatted_right_pin.update()
        master_widget_row.update()
        master_stack.update()
    right_pin_resizer = ft.GestureDetector(
        content=ft.VerticalDivider(thickness=10, width=10, color=ft.Colors.PRIMARY),  # color=ft.Colors.TRANSPARENT
        on_pan_update=move_right_pin_divider,
        on_hover=show_horizontal_cursor,
    )
    # Bottom pin resizer
    def move_bottom_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_y < 0 and story.bottom_pin.height < page.height/2) or (e.delta_y > 0 and story.bottom_pin.height > 200):
            story.bottom_pin.height -= e.delta_y
        formatted_bottom_pin.update()
        master_widget_row.update()
        master_stack.update()
    bottom_pin_resizer = ft.GestureDetector(
        content=ft.Divider(color=ft.Colors.PRIMARY, height=10, thickness=10),
        on_pan_update=move_bottom_pin_divider,
        on_hover=show_vertical_cursor,
    )

    
    # Formatted pin locations that also hold our resizer gesture detecctors
    # Main pin is always expanded and has no resizer, so it doesnt need to be formatted
    formatted_top_pin = ft.Column(spacing=0, controls=[story.top_pin, top_pin_resizer])
    formatted_left_pin = ft.Row(spacing=0, controls=[story.left_pin, left_pin_resizer]) 
    formatted_right_pin = ft.Row(spacing=0, controls=[right_pin_resizer, story.right_pin])  # Right pin formatting row
    formatted_bottom_pin = ft.Column(spacing=0, controls=[bottom_pin_resizer, story.bottom_pin])  # Bottom pin formatting column


    
    '''
    print(f"story.top_pin_obj length:  {len(story.top_pin_obj)}")
    print(f"visible widgets:    {len(top_pin.controls)} \n")
    print(f"story.left_pin_obj length:  {len(story.left_pin_obj)}")
    print(f"visible widgets:    {len(left_pin.controls)} \n")
    print(f"story.main_pin_obj length:  {len(story.main_pin_obj)}")
    print(f"visible widgets:    {len(main_pin.controls)} \n")
    print(f"story.right_pin_obj length:  {len(story.right_pin_obj)}")
    print(f"visible widgets:    {len(right_pin.controls)} \n")
    print(f"story.bottom_pin_obj length:  {len(story.bottom_pin_obj)}")
    print(f"visible widgets:    {len(bottom_pin.controls)} \n")
    '''

    # Check if we have any widgets in top pin. If not, we hide the formatted top pin
    # If there are widgets, check if any are visible. If yes, show the formatted pin and break the loop
    if len(story.top_pin.controls) == 0:
        formatted_top_pin.visible = False
    else:
        for obj in story.top_pin.controls:
            if obj.visible == True:
                formatted_top_pin.visible = True
                break
        # format and add our top pin
        if story.top_pin.height < minimum_pin_height:
            story.top_pin.height = minimum_pin_height

    if len(story.left_pin.controls) == 0:
        formatted_left_pin.visible = False
    else:
        for obj in story.left_pin.controls:
            if obj.visible == True:
                formatted_left_pin.visible = True
                break
        if story.left_pin.width < minimum_pin_width:
            story.left_pin.width = minimum_pin_width

    if len(story.right_pin.controls) == 0:
        formatted_right_pin.visible = False
    else:
        for obj in story.right_pin.controls:
            if obj.visible == True:
                formatted_right_pin.visible = True
                break
        if story.right_pin.width < minimum_pin_width:
            story.right_pin.width = minimum_pin_width

    if len(story.bottom_pin.controls) == 0:
        formatted_bottom_pin.visible = False
    else:
        for obj in story.bottom_pin.controls:
            if obj.visible == True:
                formatted_bottom_pin.visible = True
                break
        if story.bottom_pin.height < minimum_pin_height:
            story.bottom_pin.height = minimum_pin_height



    # Format our pins on the page
    master_widget_row.controls.clear()
    master_widget_row.controls = [
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
    arrange_widgets()


# Fix formatting, get rest of drag targets working
# Add stack so drag targets are same size as pin??