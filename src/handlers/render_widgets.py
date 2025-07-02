'''
Layout our widgets whenever there is more than 2
'''
import flet as ft
from models.story import story
from handlers.create_widget import create_widget


# Accept functions for each pin location
def ib_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    stack.controls.clear()
    stack.controls.append(widget_row)  # Re-add the widget row to the stack
    stack.update()
    print("ib drag target accepted")

def top_pin_drag_accept(e):
    #e.control.content = ft.Row(height=default_pin_height)
    print(e.control.content)
    for widget in story.widgets:
        if widget.title == e.data:
            story.top_pin_widgets.append(widget.control)


    
    e.control.update()
    print("top pin accepted")

def left_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("left pin accepted")

def main_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("main pin accepted")

def right_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("right pin accepted")

def bottom_pin_drag_accept(e):
    e.control.content = ft.Row(height=default_pin_height)
    e.control.update()
    print("bottom pin accepted")

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

min_drag_target_height = 200
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
    on_accept=bottom_pin_drag_accept,
    on_will_accept=drag_will_accept,
    on_leave=on_leave,
)

# containers for our pin drag targets
pin_drag_targets = [    # Must be in flet containers in order to position them
    ft.Container(
        content=in_between_drag_target,
        expand=True,
        margin=ft.margin.all(10),
        border_radius=ft.border_radius.all(10),  # 10px radius on all corners
        top=0, left=0, right=0, bottom=0,
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

widget_row = ft.Row(
    spacing=10,
    expand=True,
    controls=[]
)
    
stack = ft.Stack(expand=True, controls=[widget_row])

# Pin our widgets in here for formatting
def render_widgets(page: ft.Page):
    
    # Render our pin areas for flet
    top_pin = ft.Row(spacing=10, controls=[])
    tpf = ft.Column(spacing=0, controls=[])  # Top pin formatting column
    left_pin = ft.Column(spacing=10, controls=[])
    lpf = ft.Row(spacing=0, controls=[])  # Left pin formatting row
    main_pin = ft.Row(expand=True, spacing=10, controls=[])   # no formatting needed
    right_pin = ft.Column(spacing=10, controls=[])
    rpf = ft.Row(spacing=0, controls=[])  # Right pin formatting row
    bottom_pin = ft.Row(spacing=10, controls=[])
    bpf = ft.Column(spacing=0, controls=[])  # Bottom pin formatting column

    # Check if objects in pins are visible, add them to render if they are
    for obj in story.main_pin_obj:
        if obj.visible == True:
            main_pin.controls.append(create_widget(obj.title, page, obj.tag, widget_row, pin_drag_targets, stack)) 

    for obj in story.bottom_pin_obj:
        if obj.visible == True:
            bottom_pin.controls.append(create_widget(obj.title, page, obj.tag, widget_row, pin_drag_targets, stack))
    
   
    print(f"top pin widgets length: {len(story.top_pin_obj)}")
    print(f"tp visible widgets len: {len(top_pin.controls)}")

    print(f"Left pin widgets length: {len(story.left_pin_obj)}")
    print(f"lp visible widgets len: {len(left_pin.controls)}")

    print(f"main pin widgets length: {len(story.main_pin_obj)}")
    print(f"mp visible widgets len: {len(main_pin.controls)}")

    print(f"right pin widgets length: {len(story.right_pin_obj)}")
    print(f"rp visible widgets len: {len(right_pin.controls)}")

    print(f"num of objects instory.bottom_pin_obj {len(story.bottom_pin_obj)}")
    print(f"bp visible widgets len: {len(bottom_pin.controls)}")
    

    # Catch if no widgets in main pin. Must have at least 1 if there is at least 1 visible widget
    if len(main_pin.controls) == 0:
        print("main pin is empty, catching error")
        print("Stole widget from bottom_pin.controls")
        main_pin.controls.append(bottom_pin.controls[0])
        bottom_pin.controls.remove(bottom_pin.controls[0])  # Remove the first widget from the bottom pin

    # If pin is empty, don't expand (hide it)
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


    print("layout widgets done")

   
'''
    if len(story.main_pin_widgets) >= 1:
        for widget in story.main_pin_widgets:
            main_pin.controls.append(widget)  # Add the control to the main work area

        # Format and load our top widgets
        if len(story.top_pin_widgets) > 0:
            top_pin.height=default_pin_height
            top_pin.controls.extend(story.top_pin_widgets)  # Add any widgets that were in the top pin list

            # format and add our top pin
            tpf.controls.append(ft.Container(height=10))
            tpf.controls.append(top_pin)

        # Format and load our left pin widgets
        if len(story.left_pin_widgets) > 0:
            left_pin.width=default_pin_width
            left_pin.controls.append(ft.Container(height=0))
            left_pin.controls.extend(story.left_pin_widgets)
            left_pin.controls.append(ft.Container(height=0))

            lpf.controls.append(ft.Container(width=10))
            lpf.controls.append(left_pin)


        # Format and load our left pin widgets
        if len(story.right_pin_widgets) > 0:
            right_pin.width=default_pin_width
            right_pin.controls.append(ft.Container(height=0))
            for widget in story.right_pin_widgets:
                if widget.visible:
                    right_pin.controls.append(widget)
            
            right_pin.controls.append(ft.Container(height=0))

            rpf.controls.append(right_pin)
            rpf.controls.append(ft.Container(width=10))

        # Format and load our top widgets
        if len(story.bottom_pin_widgets) > 0:
            bottom_pin.height=default_pin_height
            for widget in story.bottom_pin_widgets:
                if widget.visible:
                    bottom_pin.controls.append(widget)

            # format and add our top pin
            bpf.controls.append(bottom_pin)
            bpf.controls.append(ft.Container(height=10))
                         
        '''