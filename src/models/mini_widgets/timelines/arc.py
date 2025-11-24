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
                'color': "secondary",                         # Color of the arc in the timeline
                'dropdown_is_expanded': True,               # If the arc dropdown is expanded on the rail
                'plot_points_are_expanded': True,           # If the plotpoints section is expanded
                'arcs_are_expanded': True,                  # If the arcs section is expanded
                'size': size,                               # Size of the arc on the timeline. Can be Small, Medium, Large, or X-Large
                'size_int': size_int,                       # S=4, M=3, L=2, XL=1.5
                'arc_height': pin_height / size_int,       # Height of the arc on the timeline calculated dynamically from pin location and size
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

        # Set our alignment values
        self.x_alignment_start = ft.Alignment(self.data.get('x_alignment_start'), 0)
        self.x_alignment_end = ft.Alignment(self.data.get('x_alignment_end', 0), 0)



        # UI elements
        self.timeline_control: ft.Stack = None      # Stack that holds our timeline arc and slider
        self.timeline_arc: ft.Container = None     # Container with rounded border to draw our arc on the timeline
        self.gd: ft.GestureDetector = None          # Gesture detector to handle clicks and hovers on the timeline_arc.
        self.slider: ft.RangeSlider = None          # Slider to drag our start and end points for the arc on the timeline

        # Build the gesture detector for our timeline arc. It doesn't need to be rebuilt, so we just do it once in constructor
        self.gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            expand=True,
            #on_enter=self.show_slider,
            on_tap=self.show_slider,
            on_exit=self.hide_slider,
        )   

        # State variables
        self.is_dragging: bool = False              # If we are currently dragging our arc slider
      

        # Loads our mini widget
        self.reload_mini_widget()



    # Called when hovering over our plot point to show the slider
    def show_slider(self, e=None):
        ''' Shows our slider and hides our timeline_point. Makes sure all other sliders are hidden '''
        return

        # Check all other plot points
        for arc in self.owner.arcs.values():

            # If they are dragging, we don't wanna also start dragging ours, so return out
            if arc.is_dragging and arc != self:
                return
            
            # Also check if they have a slider visible. This matter for very close together plot points. Make sure only one is ready to drag at a time
            elif arc.slider.visible and arc != self:
                return
            
        
        # If we didn't return out, show our slider and hide our timeline point
        self.slider.visible = True
        self.timeline_arc.visible = False
        
        # Apply it to the UI
        self.p.update()


    # Called when we stop dragging our slider thumb, or when we drag too high or low from slider
    def hide_slider(self, e=None):
        ''' Hides our slider and puts our dot back on the timeline. Saves our new position to the file '''
        return
    
        # Hide slider
        self.slider.visible = False
        #self.timeline_arc.visible = True      # Set our point to visible again
        self.is_dragging = False                # No longer dragging

        # Update our alignment based on our correct data. This is updated when dragging, so no need to set it here
        self.x_alignment = ft.Alignment(self.data.get('x_alignment', 0), 0)

        # Save new x_alignment to file
        self.save_dict()
        
        # Must reload our plot point to apply the change to ourself, then reload the parent widget to apply the change to the page
        #self.reload_mini_widget()
        #self.owner.reload_widget()

    # Called to determine if we want to hide our slider
    def may_hide_slider(self, e=None):
        ''' Checks our dragging state. If we are dragging, don't hide the slider '''

        # Check if we're dragging
        if self.is_dragging:
            return
        
        # If we're not dragging, hide the slider
        else:
            return
    
            # Hide slider
            self.slider.visible = False
            self.timeline_arc.visible = True      # Set our point to visible again
            self.is_dragging = False

            # Since no data changed, just update the page to apply changes
            self.p.update()
            

    # Called when mouse clicks the thumb on the slider to start drag, or just clicks it
    def start_dragging(self, e=None):
        ''' Sets our state to dragging so may_hide_slider knows not to hide us. Also makes sure we're visible if clicking'''
        self.is_dragging = True
        self.toggle_visibility(value=True)

    # Called whenever we need to rebuild our slider, such as on construction or when our x position changes
    def reload_slider(self):

        # Give us a ratio for integers for our left and right expand values to catch hover off of our plot pont
        ratio = (self.data.get('x_alignment', 0) + 1) / 2     # Convert -1 -> 1 to 0 -> 1
    
        # Set the left and right ratio
        left_ratio = int(ratio * 1000)
        right_ratio = 1000 - left_ratio

        # state used during dragging
        self.slider = ft.Column(
            spacing=0,
            visible=True,                                      # Start hidden until we hover over plot point
            controls=[
                ft.GestureDetector(on_enter=self.hide_slider, expand=True, content=ft.Container(bgcolor=ft.Colors.with_opacity(.3, "yellow"))),    # Invisible container to hide slider when going too far up
                ft.Stack(
                    alignment=ft.Alignment(0,0),
                    controls=[
                    ft.GestureDetector(                                             # GD so we can detect right clicks on our slider
                        on_secondary_tap=lambda e: print("Right click on slider"),
                        content=ft.RangeSlider(
                            min=-100, max=100,                                  # Min and max values on each end of slider
                            start_value=self.data.get('x_alignment_start', 0) * 100,        # Where we start on the slider
                            end_value=self.data.get('x_alignment_end', 0) * 100,            # Where we end on the slider
                            divisions=200,                                      # Number of spots on the slider
                            active_color=self.data.get('color', "secondary"),                 # Get rid of the background colors
                            inactive_color=ft.Colors.TRANSPARENT,               # Get rid of the background colors
                            overlay_color=ft.Colors.TRANSPARENT,    # Color of plot point when hovering over it or dragging    
                            #on_change=lambda e: self.change_x_position(e),      # Update our data with new x position as we drag
                            #on_change_end=self.hide_slider,                     # Save the new position, but don't write it yet                      
                            #on_change_start=self.start_dragging,                # Make sure we're visible
                            #on_blur=self.hide_slider                            # Hide the slider if we click away from it
                        ),
                    ),
                    # Sitting overtop the slider, is a row with expand based on our proportions
                    ft.Row(
                        spacing=0,
                        expand=True,
                        height=100,
                        controls=[
                            #ft.GestureDetector(         # Catch our hovers to the left of the thumb
                                #on_hover=self.may_hide_slider,
                                #expand=left_ratio,
                                #content=ft.Container(expand=True),
                                #content=ft.Container(expand=True, bgcolor=ft.Colors.with_opacity(.3, "red"))
                            #),
                            ft.Column(
                                width=50,
                                spacing=0,
                                controls=[
                                    # Catch above and below the thumb
                                    ft.GestureDetector(expand=True, on_hover=self.may_hide_slider, hover_interval=100),

                                    # Reserve safe space for the thumb
                                    ft.Container(       # Safe area
                                        ignore_interactions=True,
                                        shape=ft.BoxShape.CIRCLE,
                                        width=50, height=50, 
                                    ),
                                    ft.GestureDetector(expand=True, on_hover=self.may_hide_slider, hover_interval=100),
                                ]
                            ),
                            #ft.GestureDetector(         # Catch our hovers to the right of the thumb
                                #on_hover=self.may_hide_slider,
                                #expand=right_ratio,
                                #content=ft.Container(expand=True),
                                #content=ft.Container(expand=True, bgcolor=ft.Colors.with_opacity(.3, "red"))
                            #),
                        ]
                    )
                ]),
                ft.GestureDetector(on_enter=self.hide_slider, expand=True, content=ft.Container(bgcolor=ft.Colors.with_opacity(.3, "yellow"))),    # Invisible container to hide slider when going too far down
        ])

    # Called from reload mini widget to update our timeline control
    def reload_timeline_control(self):
        ''' Reloads our arc drawing on the timeline based on current/updated data, including page size '''

        # Reload our slider
        self.reload_slider()

        # Make sure our alignment are correct
        self.x_alignment_start = ft.Alignment(self.data.get('x_alignment_start', -.2), 0)
        self.x_alignment_end = ft.Alignment(self.data.get('x_alignment_end', .2), 0)


        # Give us a ratio for integers for our left and right expand values to catch hover off of our plot pont
        left_ratio = (self.data.get('x_alignment_start', 0) + 1) / 2     # Convert -1 -> 1 to 0 -> 1
        right_ratio = (1 - self.data.get('x_alignment_end', 0)) / 2     # Convert -1 -> 1 to 0 -> 1
    
        # Set the left and right ratio
        left_ratio = int(left_ratio * 1000)
        right_ratio = int(right_ratio * 1000)

        mid_ratio = 1000 - right_ratio - left_ratio

        spacing_left = ft.Container(
            expand=left_ratio, 
            #bgcolor=ft.Colors.with_opacity(0.3, "red")
        )
        spacing_right = ft.Container(
            expand=right_ratio, 
            #bgcolor=ft.Colors.with_opacity(0.3, "red")
        )
        

        self.timeline_arc = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.3, "yellow"),    # Testing
            offset=ft.Offset(0, -0.5) if self.data['branch_direction'] == "top" else ft.Offset(0, .5),          # Moves it up or down slightly to center on timeline
            expand=mid_ratio,
            height=200,
            padding=ft.Padding(0,0,0,0),

            #height=None/proportions of width
            border=ft.border.all(2, self.data.get('color', "primary")),
            
            #border=ft.border.only(
                #top=ft.BorderSide(2, self.data.get('color', "primary")),
                #left=ft.BorderSide(2, self.data.get('color', "primary")),
                #right=ft.BorderSide(2, self.data.get('color', "primary")),
                #bottom=ft.BorderSide(0, ft.Colors.TRANSPARENT),
            #),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border_radius=ft.BorderRadius(
                top_left=1000,      
                top_right=1000,     
                bottom_left=0,   
                bottom_right=0
            ),
            content=self.gd,        # Set the content to our gesture detector so we can handle clicks and hovers
        )

        # Row for our spacing containers, and rebuilt timeline_arc
        row = ft.Row(
            expand=True,
            visible=False,
            spacing=0,
            controls=[
                spacing_left,
                self.timeline_arc,
                spacing_right,
            ]
        )
    

        self.timeline_control = ft.Stack(
            expand=True,            # Make sure it fills the whole timeline width
            controls=[
                ft.Container(expand=True, ignore_interactions=True),        # Make sure our stack is always expanded to full size
                row,
                self.slider,                                                # Our slider that appears when we hover over the plot point
            ]
        ) 




    # Called to reload our mini widget content
    def reload_mini_widget(self):

        # Reload our timeline control and all associated components 
        self.reload_timeline_control()


        

        
        # Build the information display of this mini widget
        self.content_control = ft.TextField(
            #on_submit=self.change_arc_height,
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
