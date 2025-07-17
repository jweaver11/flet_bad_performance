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
            print("object:\n", object) 
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "top"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("top pin accepted")

def left_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            print("object:\n", object) 
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "left"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("left pin accepted")

def main_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            print("object:\n", object) 
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "main"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("main pin accepted")


def right_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            print("object:\n", object) 
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "right"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    
    if src_id:
        draggable = e.page.get_control(src_id)
        if draggable:
            object = draggable.data
            print("object:\n", object) 
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Set our objects pin location to the correct new location
    object.pin_location = "bottom"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("bottom pin accepted")

# Drag target to catch draggable drops between the drag targets
def ib_drag_accept(e):
    e.control.content = ft.Row(height=minimum_pin_height)
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.update()
    print("ib drag target accepted")

# When a draggable is hovering over a target
def drag_will_accept(e):
    e.control.content = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
        height=minimum_pin_height
    )
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.controls.extend(pin_drag_targets)  # Add the drag targets to the stac
    stack.update()

# When a draggable leaves a target
def on_leave(e):
    #print("Left a pin drag target")
    e.control.content = ft.Row(height=300)
    e.control.update()
    stack.update()


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
        margin=ft.margin.only(top=10, left=20, right=20),
        top=0, left=200, right=200,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=left_pin_drag_target,
        width=200,
        margin=ft.margin.only(top=10, left=10, bottom=10,),
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
        margin=ft.margin.only(top=10, right=10, bottom=10,),
        right=0, top=0, bottom=0,
        border_radius=ft.border_radius.all(10),  
    ),
    ft.Container(
        content=bottom_pin_drag_target,
        height=200,
        bottom=0, left=200, right=200,
        margin=ft.margin.only(left=20, right=20, bottom=10),
        border_radius=ft.border_radius.all(10), 
    ),
]

# Master row that holds all our widgets
widget_row = ft.Row(
    spacing=10,
    expand=True,
    controls=[]
)

# Stack that holds our widget row, and the drag targets overtop them when it needs to
stack = ft.Stack(expand=True, controls=[widget_row])

# Pin our widgets in here for formatting
def render_widgets(page: ft.Page):
    print("render_widgets called")
    
    # We have our 5 pin locations that hold the containers, and the formatted controls that hold the pin locations
    # and formatting so it all looks nice. They also hold the draggable gesture detector dividers for resizing
    tpf = ft.Column(spacing=0, controls=[])  # Top pin formatting column
    lpf = ft.Row(spacing=0, controls=[])  # Left pin formatting row
    rpf = ft.Row(spacing=0, controls=[])  # Right pin formatting row
    bpf = ft.Column(spacing=0, controls=[])  # Bottom pin formatting column

    # Method called when our divider (inside a gesture detector) is dragged
    # Updates the size of our pin in the story object
    def move_top_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_y > 0 and story.top_pin.height < page.height/2) or (e.delta_y < 0 and story.top_pin.height > 200):
            story.top_pin.height += e.delta_y
        tpf.update()
    def move_left_pin_divider(e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and story.left_pin.width < page.width/2) or (e.delta_x < 0 and story.left_pin.width > 200):
            story.left_pin.width += e.delta_x
        lpf.update()

    # Change our cursor when we hover over a divider 
    def show_vertical_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        e.control.update()
    def show_horizontal_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    # Holds the divider that is draggable to resize the top pin
    top_pin_gesture_detector = ft.GestureDetector(
        content=ft.Divider(color=ft.Colors.PRIMARY, height=10),
        on_pan_update=move_top_pin_divider,
        on_hover=show_vertical_cursor,
    )
    # Holds the divider that is draggable to resize the top pin
    left_pin_gesture_detector = ft.GestureDetector(
        content=ft.VerticalDivider(color=ft.Colors.PRIMARY, width=10),
        on_pan_update=move_left_pin_divider,
        on_hover=show_horizontal_cursor,
    )


    arrange_widgets() # Only needs to run if main widget was empty catch occurs ^

    '''
    # Each obj is an extended flet container, meaning we just add it to our pin controls
    for obj in story.top_pin_obj:
        if obj.visible == True:
            top_pin.controls.append(obj)
    for obj in story.left_pin_obj:
        if obj.visible == True:
            left_pin.controls.append(obj)
    for obj in story.main_pin_obj:
            main_pin.controls.append(obj) 
    for obj in story.right_pin_obj:
        if obj.visible == True:
            right_pin.controls.append(obj)
    for obj in story.bottom_pin_obj:
        if obj.visible == True:
            bottom_pin.controls.append(obj)
    '''


    # Arrange our widgets into their pin locations
    arrange_widgets() # Only needs to run if main widget was empty catch occurs ^
    # Otherwise this is uneccessary
    
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


    # Format and render our widgets so they always look fancy on the page
    # If pin is empty, don't expand (hide it)
    if len(story.top_pin.controls) == 0:
        tpf.expand = False
    else:
        # format and add our top pin
        if story.top_pin.height < minimum_pin_height:
            story.top_pin.height = minimum_pin_height

        tpf.controls.append(ft.Container(height=10)) 
        tpf.controls.append(story.top_pin)  
        tpf.controls.append(top_pin_gesture_detector)

    if len(story.left_pin.controls) == 0:
        lpf.expand = False
    else:
        story.left_pin.width=minimum_pin_width

        lpf.controls.append(ft.Container(width=10))
        lpf.controls.append(story.left_pin)
        lpf.controls.append(left_pin_gesture_detector)

    
    if len(story.right_pin.controls) == 0:
        rpf.expand = False  
    else:
        story.right_pin.width=minimum_pin_width
        story.right_pin.controls.insert(0, ft.Container(width=10))
        story.right_pin.controls.append(ft.Container(width=10))
        rpf.controls.append(story.right_pin)
        rpf.controls.append(ft.Container(width=10))

    if len(story.main_pin.controls) == 0:
        story.main_pin.expand = False
    

    if len(story.bottom_pin.controls) == 0:
        bpf.expand = False
    else:
        # format and add our top pin
        story.bottom_pin.height=minimum_pin_height

        bpf.controls.append(story.bottom_pin)
        bpf.controls.append(ft.Container(height=10))    



    # Format our pins on the page
    widget_row.controls.clear()
    widget_row.controls = [
        lpf,    # formatted left pin
        ft.Column(
            expand=True, spacing=10, 
            controls=[
                tpf,    # formatted top pin
                story.main_pin,     # main work area with widgets
                bpf     # formatted bottom pin
        ]),
        rpf,    # formatted right pin
    ]

    page.update()


# Holding flet controls as our pins inside of story now, 