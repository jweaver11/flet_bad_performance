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


        # TODO:
        # Type of arcs?? timeskips, normal, character arcs

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
            on_tap=self.toggle_slider_visibility,
            on_enter=self.on_start_hover,
            on_exit=self.on_stop_hover,
            content=ft.Column(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text(self.title)])]),
        )   

        # State variables
        self.is_dragging: bool = False              # If we are currently dragging our arc slider
      

        # Loads our mini widget
        self.reload_mini_widget()


    # Called when we hover over our arc on the timeline
    def on_start_hover(self, e: ft.HoverEvent):
        ''' Focuses the arc control '''

        # Change its border opacity and update the page
        self.timeline_arc.border = ft.border.all(2, self.data.get('color', "secondary"))
        self.p.update()

    # Called when we stop hovering over our arc on the timeline
    def on_stop_hover(self, e: ft.HoverEvent):
        ''' Changes the arc control to unfocused '''

        self.timeline_arc.border = ft.border.all(2, ft.Colors.with_opacity(.7, self.data.get('color', "secondary")))
        self.p.update()

        
    # Called when hovering over our plot point to show the slider
    def toggle_slider_visibility(self, e=None):
        ''' Shows our slider and hides our timeline_point. Makes sure all other sliders are hidden '''

        # Check all other plot points
        for arc in self.owner.arcs.values():

            # If they are dragging, we don't wanna also start dragging ours, so return out
            if arc.is_dragging and arc != self:
                return
            
            # Also check if they have a slider visible. This matter for very close together plot points. Make sure only one is ready to drag at a time
            elif arc.slider.visible and arc != self:
                return
            
        
        # If we didn't return out, show our slider and hide our timeline point
        self.visible = not self.visible
        self.data['visible'] = self.visible
        self.slider.visible = self.visible

        self.save_dict()
        
        # Apply it to the UI
        self.p.update()
            

    # Called at the end of dragging our point on the slider to update it
    def change_x_positions(self, e: ft.DragUpdateEvent):
        ''' Changes our x position on the slider, and saves it to our data dictionary, but not to our file yet '''

        self.is_dragging = True                 # We are actively dragging

        # Grab our new positions as floats of whatever number division we're on (-100 -> 100)
        new_start_position = float(e.control.start_value)
        new_end_position = float(e.control.end_value)

        # Convert that float between -1 -> 1 for our alignment to work
        nsp = new_start_position / 100
        nep = new_end_position / 100

        # Save the new position to data, but don't needlessly write to file until we stop dragging
        self.data['x_alignment_start'] = nsp
        self.data['x_alignment_end'] = nep

        self.is_dragging = True


    # Called when we finish dragging our slider thumb to save our new position
    def finished_dragging(self, e):
        ''' Saves our new x positions to the file and updates alignment. Then applies the UI changes '''

        # Update our state
        self.is_dragging = False                # No longer dragging

        # Make sure our alignment are correct
        self.x_alignment_start = ft.Alignment(self.data.get('x_alignment_start', -.2), 0)
        self.x_alignment_end = ft.Alignment(self.data.get('x_alignment_end', .2), 0)

        # Save our new positions to file
        self.save_dict()

        # Apply the UI changes
        self.reload_mini_widget()
        self.owner.reload_widget()

    # Called whenever we need to rebuild our slider, such as on construction or when our x position changes
    def reload_slider(self):

        # Rebuild our slider
        self.slider = ft.Column(
            spacing=0,
            visible=self.visible,                                      # Start hidden until we hover over plot point
            controls=[
                ft.Stack(
                    alignment=ft.Alignment(0,0),
                    expand=True,
                    controls=[
                        ft.Container(expand=True, ignore_interactions=True),        # Make sure our stack is always expanded to full size
                        ft.GestureDetector(                                             # GD so we can detect right clicks on our slider
                            on_secondary_tap=lambda e: print("Right click on slider"),
                            height=100,
                            content=ft.RangeSlider(
                                min=-100, max=100,                                  # Min and max values on each end of slider
                                start_value=self.data.get('x_alignment_start', 0) * 100,        # Where we start on the slider
                                end_value=self.data.get('x_alignment_end', 0) * 100,            # Where we end on the slider
                                divisions=200,                                      # Number of spots on the slider
                                active_color=self.data.get('color', "secondary"),                 # Get rid of the background colors
                                tooltip="",
                                inactive_color=ft.Colors.TRANSPARENT,               # Get rid of the background colors
                                overlay_color=ft.Colors.with_opacity(.5, self.data.get('color', "secondary")),    # Color of plot point when hovering over it or dragging    
                                on_change=self.change_x_positions,       # Update our data with new x position as we drag
                                on_change_end=self.finished_dragging,                     # Save the new position, but don't write it yet                      
                            ),
                        ),
                    ]
                ),
                
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
            ignore_interactions=True,
            #bgcolor=ft.Colors.with_opacity(0.3, "red")
        )
        spacing_right = ft.Container(
            expand=right_ratio, 
            ignore_interactions=True,
            #bgcolor=ft.Colors.with_opacity(0.3, "red")
        )

        

        self.timeline_arc = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.2, "yellow"),    # Testing
            offset=ft.Offset(0, -0.5) if self.data['branch_direction'] == "top" else ft.Offset(0, .5),          # Moves it up or down slightly to center on timeline
            expand=mid_ratio,
            height=200,
            padding=ft.Padding(2,2,2,2),

            #height=None/proportions of width
            border=ft.border.all(2, ft.Colors.with_opacity(.7, self.data.get('color', "secondary"))),
            
            #border=ft.border.only(
                #top=ft.BorderSide(0, ft.Colors.TRANSPARENT),
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
            spacing=0,
            controls=[
                ft.Container(width=24),
                spacing_left,
                self.timeline_arc,
                spacing_right,
                ft.Container(width=24),
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
