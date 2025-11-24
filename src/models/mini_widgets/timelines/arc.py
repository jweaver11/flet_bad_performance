import flet as ft
from models.mini_widget import Mini_Widget
from models.widget import Widget
from handlers.verify_data import verify_data
import flet.canvas as cv
import math
from models.app import app

# Class for arcs (essentially sub-timelines that are connected) on a timeline. 
# Arcs split off from the main timeline and can merge back in later. Exp: Characters going on different journeys that rejoin later
class Arc(Mini_Widget):

    # Constructor.
    def __init__(
        self, 
        title: str, 
        owner: Widget, 
        father, 
        page: ft.Page, 
        key: str, 
        size: str = None,
        data: dict = None
    ):
        
        
        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,                    # Top most timeline this arc belongs too
            father=father,                  # Immediate parent timeline or arc that thisarc belongs too
            page=page,          
            key=key,  
            data=data,         
        ) 


        # Set pin location to calculate sizes
        pin_location = self.owner.data.get("pin_location", "main")

        # Check if a size was passed in, otherwise default to medium
        if size is None:
            size = "medium"

        # Set our size calculation int based on size string
        if size == "small":
            size_int = 4
        elif size == "medium":
            size_int = 3
        elif size == "large":
            size_int = 2
        elif size == "x-large":
            size_int = 1.5
        else:
            size_int = 3  
            
        # Determine our 'timelines height' based on the pin its in.
        if pin_location == "top":
            pin_height = self.owner.story.data['top_pin_height']
        elif pin_location == "bottom":
            pin_height = self.owner.story.data['bottom_pin_height']

        # Main, left, and right all take up the whole workspace, so we can use the page there
        else:
            #pin_height = self.owner.p.height
            pin_height = app.settings.data.get("page_height", self.owner.p.height)

        # TODO:
        # Type of arcs?? timeskips, normal, character arcs
        # Arcs have 4 sizes: small, medium, large, x-large This determines their height.
        # height = page height / by: S=4, M=3, L=2, XL=1.5

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "arc",                               # Tag to identify what type of object this is
                'is_timeskip': bool,                        # If this arc is a time skip (skips ahead in time on the timeline)   
                'branch_direction': "top",                  # Direction the arc branches off (top or bottom) from the timeline
                'start_date': str,                          # Start and end date of the branch, for timeline view
                'end_date': str,                            # Start and end date of the branch, for timeline view
                'x_alignment_start': -.2,                   # Start position on the timeline
                'x_alignment_end': .2,                      # End position on the timeline 
                'color': "primary",                         # Color of the arc in the timeline
                'dropdown_is_expanded': True,               # If the arc dropdown is expanded on the rail
                'plot_points_are_expanded': True,           # If the plotpoints section is expanded
                'arcs_are_expanded': True,                  # If the arcs section is expanded
                'size': size,                               # Size of the arc on the timeline. Can be Small, Medium, Large, or X-Large
                'size_int': size_int,                       # S=4, M=3, L=2, XL=1.5
                'arch_height': pin_height / size_int,       # Height of the arc on the timeline calculated dynamically from pin location and size
                'is_focused': bool,                         # If this arc is currently focused/selected. True when mini widget visible, or mouse hovering over arc
                

                'connections': dict,                        # Connect points, arcs, branch, etc.???
                'rail_dropdown_is_expanded': True,          # If the rail dropdown is expanded  
                'content': str,
                'description': str,
                'summary': str,
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        )

        # Declare dicts of our data types  
        self.arcs: dict = {}
        self.plot_points: dict = {} 

        self.x_alignment = ft.Alignment((self.data.get('x_alignment_start') + self.data.get('x_alignment_end')) / 2, 0)

        # The container we position on our timeline holding our arc drawing, and the gesture detector with logic for it
        self.timeline_control = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.3, "yellow"),    # Testing
            offset=ft.Offset(0, -0.5) if self.data['branch_direction'] == "top" else ft.Offset(0, .5),          # Moves it up or down slightly to center on timeline
            width=200,
            #expand=True,
            height=200,
            padding=ft.Padding(0,0,0,0),
            #height=None/proportions of width
            border=ft.border.all(2, self.data.get('color', "primary")),
            border_radius=ft.BorderRadius(
                top_left=1000,      
                top_right=1000,     
                bottom_left=0,   
                bottom_right=0
            ),
        )    

        self.left_connector = ft.GestureDetector(
            content=ft.Icon(ft.Icons.FIBER_MANUAL_RECORD),
            mouse_cursor=ft.MouseCursor.CLICK,
            #alignment=ft.Alignment(-1,-1),
            on_hover=lambda e: print("hovered over left connector")
        )
        self.right_connector = ft.Container(
            alignment=ft.Alignment(1,-1),
            padding=ft.Padding(0,0,0,0),
            content=ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.CLICK,
                content=ft.IconButton(ft.Icons.FIBER_MANUAL_RECORD),
                #content=ft.Container(shape=ft.BoxShape.CIRCLE, width=16, height=16, bgcolor=ft.Colors.BLUE),
                on_hover=lambda e: print("hovered over right connector")
            )
        )

        # Gesture detector to handle clicks and hovers on the arc. 
        self.gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda e: print(f"Arc {self.title} tapped"),
            #expand=True,
            #on_hover=self.on_hovers,
            on_enter=lambda e: self.on_start_hover(e),
            on_exit=self.on_stop_hover,
            content=ft.Stack(
                expand=True, controls=[
                ft.Container(ignore_interactions=True, expand=True),
                self.left_connector,
                self.right_connector,
            ])
        )   

      

        # Loads our mini widget
        self.reload_mini_widget()


    # Called when hovering over the arc on the timeline
    def on_hovers(self, e):
        # Grab x position on the timeline
        
        self.data['is_focused'] = True
        self.reload_mini_widget()

    # Called when hovering over the arc on the timeline
    def on_start_hover(self, e=None):
        
        self.timeline_control.border = ft.border.all(2, self.data.get('color', "primary"))
        self.p.update()
        

    def on_stop_hover(self, e=None):
        self.timeline_control.border = ft.border.all(2, ft.Colors.with_opacity(.7, self.data.get('color', "primary")))
        self.p.update()
        

    def change_arc_height(self, e):
        ''' Changes the arc height based on new size string passed in '''

        new_size = e.control.value.lower()
        
        # Set our size calculation int based on size string
        if new_size == "small":
            size_int = 4
        elif new_size == "medium":
            size_int = 3
        elif new_size == "large":
            size_int = 2
        elif new_size == "x-large":
            size_int = 1.5
        else:
            size_int = 3  

        # Update our data values
        self.data['size'] = new_size
        self.data['size_int'] = size_int
        self.save_dict()

        # Reload our timeline control to apply changes
        self.reload_mini_widget()

        # Update the UI
        self.p.update()

    # Called from reload mini widget to update our timeline control
    def reload_timeline_control(self):
        ''' Reloads our arc drawing on the timeline based on current/updated data, including page size '''
        self.timeline_control.content = self.gd
            


    # Called to reload our mini widget content
    def reload_mini_widget(self):

        self.reload_timeline_control()

        self.content_control = ft.TextField(
            on_submit=self.change_arc_height,
            hint_text="Arc Size (Small, Medium, Large, X-Large)",
        )

        
        # Reload the mini widget content
        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.delete_dict() # Pass in whatever branch it is (just self for now)
                ),
            ],
            expand=True,
        )

        self.p.update()
