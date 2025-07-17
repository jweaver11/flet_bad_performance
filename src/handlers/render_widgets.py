'''
Layout our widgets whenever there is more than 2
'''
import flet as ft
from models.user import user
import json
from handlers.arrange_widgets import arrange_widgets

story = user.stories['empty_story']  # Get our story object from the user

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

    # Set our pin location inside the object to the correct new location
    object.pin_location = "top"

    arrange_widgets()       # Re-arrange our widgets held in the story object
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row()
    e.control.update()
    print("top pin accepted")

def left_pin_drag_accept(e):
    # e.data is a JSON string, so we have to parse it
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    print("src_id:", src_id)
    if src_id:
        # Get the Draggable control by ID
        obj = e.page.get_control(src_id)
        if obj:
            print("Draggable's data:", obj.data)
            # Now you can use src_control.data["tag"], etc.
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Our 'obj' needs the data parameter to access inside of here now
    # Check our pin location, and set it to correct pin
    pl = obj.data.pin_location
    if pl == "top" or pl == "main" or pl == "right" or pl == "bottom":
        obj.data.pin_location = "left"

    arrange_widgets()
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("left pin accepted")

def main_pin_drag_accept(e):
    # e.data is a JSON string, so we have to parse it
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    print("src_id:", src_id)
    if src_id:
        # Get the Draggable control by ID
        obj = e.page.get_control(src_id)
        if obj:
            print("Draggable's data:", obj.data)
            # Now you can use src_control.data["tag"], etc.
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    pl = obj.data.pin_location
    if pl == "top" or pl == "left" or pl == "right" or pl == "bottom":
        obj.data.pin_location = "main"

    arrange_widgets()
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("main pin accepted")


def right_pin_drag_accept(e):
    # e.data is a JSON string, so we have to parse it
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    print("src_id:", src_id)
    if src_id:
        # Get the Draggable control by ID
        obj = e.page.get_control(src_id)
        if obj:
            print("Draggable's data:", obj.data)
            # Now you can use src_control.data["tag"], etc.
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Our 'obj' needs the data parameter to access inside of here now
    # Check our pin location, and set it to correct pin
    pl = obj.data.pin_location
    if pl == "top" or pl == "left" or pl == "main" or pl == "bottom":
        obj.data.pin_location = "right"

    arrange_widgets()
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    # e.data is a JSON string, so we have to parse it
    event_data = json.loads(e.data)
    src_id = event_data.get("src_id")
    print("src_id:", src_id)
    if src_id:
        # Get the Draggable control by ID
        obj = e.page.get_control(src_id)
        if obj:
            print("Draggable's data:", obj.data)
            # Now you can use src_control.data["tag"], etc.
        else:
            print("Could not find control with src_id:", src_id)
    else:
        print("src_id not found in event data")

    # Our 'obj' needs the data parameter to access inside of here now
    pl = obj.data.pin_location
    if pl == "top" or pl == "left" or pl == "main" or pl == "right":
        obj.data.pin_location = "bottom"

    arrange_widgets()
    render_widgets(e.page)  # Re-render the widgets to reflect the new pin location
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("bottom pin accepted")

# Drag target to catch draggable drops between the drag targets
def ib_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.update()
    print("ib drag target accepted")

# When a draggable is hovering over a target
def drag_will_accept(e):
    e.control.content = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), 
        height=default_pin_height
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
default_pin_height = 200
default_pin_width = 200

#min_drag_target_height = 200
min_drag_target_width = 200

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
    top_pin = ft.Row(spacing=10, controls=[], height=0)
    tpf = ft.Column(spacing=0, controls=[], height=0)  # Top pin formatting column
    left_pin = ft.Column(spacing=10, controls=[])
    lpf = ft.Row(spacing=0, controls=[])  # Left pin formatting row
    main_pin = ft.Row(expand=True, spacing=10, controls=[])   # no formatting needed
    right_pin = ft.Column(spacing=10, controls=[])
    rpf = ft.Row(spacing=0, controls=[])  # Right pin formatting row
    bottom_pin = ft.Row(spacing=10, controls=[])
    bpf = ft.Column(spacing=0, controls=[])  # Bottom pin formatting column


    def move_horizontal_divider(e: ft.DragUpdateEvent):
        print("e.delta_y: ", e.delta_y)
        
        # Initialize height if it's None
        if tpf.height is None:
            tpf.height = default_pin_height  # or some default value
        
        print("tpc.height: ", tpf.height)

        if (e.delta_y > 0 and top_pin.height < 300) or (e.delta_y < 0 and top_pin.height > 100):
            top_pin.height += e.delta_y
        top_pin.update()
        tpf.update()
        main_pin.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_UP_DOWN
        e.control.update()

    hgd = ft.GestureDetector(
        content=ft.Divider(color=ft.Colors.PRIMARY, height=2),
        on_pan_update=move_horizontal_divider,
        on_hover=show_draggable_cursor,
    )

    vgd = ft.GestureDetector()


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
    if len(top_pin.controls) == 0:
        tpf.expand = False
    else:
        # format and add our top pin
        top_pin.height=default_pin_height
        tpf.height = default_pin_height + 50

        tpf.controls.append(ft.Container(height=10)) 
        tpf.controls.append(top_pin)  
        tpf.controls.append(hgd)

    if len(left_pin.controls) == 0:
        lpf.expand = False
    else:
        left_pin.width=default_pin_width
        left_pin.controls.insert(0, ft.Container(width=10))  # Add spacing to left pin
        left_pin.controls.append(ft.Container(width=10))  # Add spacing to left pin
        lpf.controls.append(ft.Container(width=10))
        lpf.controls.append(left_pin)

    if len(main_pin.controls) == 0:
        main_pin.controls.append(ft.Container(expand=True))

    if len(right_pin.controls) == 0:
        rpf.expand = False  
    else:
        right_pin.width=default_pin_width
        right_pin.controls.insert(0, ft.Container(width=10))
        right_pin.controls.append(ft.Container(width=10))
        rpf.controls.append(right_pin)
        rpf.controls.append(ft.Container(width=10))

    if len(main_pin.controls) == 0:
        main_pin.expand = False
    

    if len(bottom_pin.controls) == 0:
        bpf.expand = False
    else:
        # format and add our top pin
        bottom_pin.height=default_pin_height

        bpf.controls.append(bottom_pin)
        bpf.controls.append(ft.Container(height=10))    



    # Format our pins on the page
    widget_row.controls.clear()
    widget_row.controls = [
        lpf,    # formatted left pin
        ft.Column(
            expand=True, spacing=10, 
            controls=[
                tpf,    # formatted top pin
                main_pin,     # main work area with widgets
                bpf     # formatted bottom pin
        ]),
        rpf,    # formatted right pin
    ]

    page.update()
