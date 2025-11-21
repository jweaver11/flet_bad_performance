import flet as ft
from models.mini_widget import Mini_Widget
from models.widget import Widget
from handlers.verify_data import verify_data
from models.widgets.timeline import Timeline


# Plotpoint mini widget object that appear on timelines and arcs
class Plot_Point(Mini_Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, key: str, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,        
            father=father,      # In this case, father is always a timeline or another arc
            page=page,          
            key=key,  
            data=data,    
        ) 
        

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "plot_point",            # Tag to identify what type of object this is
                'description': str,
                'events': list,                 # Numbered list of events that occur at this plot point
                'x_alignment': float,           # Float between -1 and 1 on x axis of timeline. 0 is center
                'is_major': bool,               # If this plot point is a major event
                'date': str,                    # Date of the plot point
                'time': str,                    # Time of the plot point
                'color': "secondary",           # Color of the plot point on the timeline
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        )

        # Set our x alignment to position on our timeline. -1 is left, 0 is center, 1 is right. Default 0
        self.x_alignment = ft.Alignment(self.data.get('x_alignment', 0), 0)

        # state used during dragging
        self.slider = ft.Column(
            spacing=0,
            controls=[
                ft.Container(on_hover=self.hide_slider, expand=True, bgcolor=ft.Colors.TRANSPARENT),    # Invisible container to hide slider when going too far up
                ft.GestureDetector(                                             # GD so we can detect right clicks on our slider
                    on_secondary_tap=lambda e: print("Right click on slider"),
                    content=ft.Slider(
                        min=-100, max=100,                                  # Min and max values on each end of slider
                        adaptive=True,                                      # Make sure it looks good on all devices
                        value=self.data.get('x_alignment', 0) * 100,        # Where we start on the slider
                        divisions=200,                                      # Number of spots on the slider
                        interaction=ft.SliderInteraction.SLIDE_THUMB,       # Make sure you can only drag the plot point, and not click the slider to move it
                        active_color=ft.Colors.TRANSPARENT,                 # Get rid of the background colors
                        inactive_color=ft.Colors.TRANSPARENT,               # Get rid of the background colors
                        thumb_color=self.data.get('color', "secondary"),    # Color of our actual dot on the slider
                        overlay_color=ft.Colors.with_opacity(.5, self.data.get('color', "secondary")),    # Color of plot point when hovering over it or dragging      
                        on_change=lambda e: self.change_x_position(e),      # Update our data with new x position as we drag
                        on_change_end=self.hide_slider,                     # Save the new position, but don't write it yet                      
                        on_change_start=self.timeline_control_click,        # Show the slider when we click on the plot point
                        on_blur=self.hide_slider
                    ),
                ),
                ft.Container(on_hover=self.hide_slider, expand=True, bgcolor=ft.Colors.TRANSPARENT),    # Invisible container to hide slider when going too far down
        ])
 
        # Gesture detector for our plot point on the timeline, so we can hover over it to show the slider
        self.gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            expand=False,   
            content=ft.Container(
                padding=ft.Padding(20,0,20,0),                  # Gives us necessary padding so we look pretty on our timeline
                expand=False, ignore_interactions=True,         # Make sure this container doesn't mess with our gesture detector interactions
                content=ft.CircleAvatar(radius=8, bgcolor=self.data.get('color', "secondary"))      # Dot on the timeline
            ),      
            
            on_enter=self.timeline_control_click,               # Show the slider when we hover over our plot point
            on_secondary_tap=lambda e: print("Right click on plot point")
            #TODO: Make sure we can right click, including move. Long left click allows us to move
        )
            
        
        # Stack that holds our 
        self.timeline_control = ft.Stack(
            alignment=self.x_alignment,
            expand=True,            # Make sure it fills the whole timeline width
            controls=[
                ft.Container(expand=True, ignore_interactions=True),        # Make sure our stack is always expanded to the full width of the timeline
                self.gd,                                                    # Our plot point on the timeline
                self.slider                                                 # Our slider that appears when we hover over the plot point
            ]
        ) 


        self.reload_mini_widget()

    # Called at the end of dragging our point on the slider to update it
    def change_x_position(self, e):
        ''' Changes our x position on the slider, and saves it to our data dictionary, but not to our file yet '''

        # Grab our new position as a flot of whatever number division we're on (-100 -> 100)
        new_position = float(e.control.value)

        # Convert that float between -1 -> 1 for our alignment to work
        np = new_position / 100

        # Save the new position to data, but don't needlessly write to file until we stop dragging
        self.data['x_alignment'] = np
        
    # Called when hovering over our plot point to show the slider
    def show_slider(self, e=None):
        ''' Shows our slider and hides our gesture detector. Makes sure all other sliders are hidden '''
        
        # Set slider to visible and hide our plot point on the timeline
        if not self.slider.visible:
            self.slider.visible = True
            self.gd.visible = False
            
            # Apply it to the UI
            self.p.update()

        # If we're already visible, skip all the logic and just return
        else:
            return

    # Called when we stop dragging our plotpoint, or when we drag too hight or low from slider
    def hide_slider(self, e=None):
        ''' Hides our slider and puts our dot back on the timeline. Saves our new position to the file '''
        print("Hide slider called")
        # Hide slider
        self.slider.visible = False
        self.gd.visible = True

        # Update our alignment based on our correct data
        self.x_alignment = ft.Alignment(self.data.get('x_alignment', 0), 0)

        # Save new position to the file
        self.save_dict()
        
        # Must reload our plot point to apply the change to ourself, then reload the parent widget to apply the change to the page
        self.reload_mini_widget()
        self.owner.reload_widget()


    def timeline_control_click(self, e=None):
        ''' Called when we click on our plot point on the timeline. Shows our slider and hides the plot point '''
        self.show_slider()

        self.toggle_visibility(value=True)



    # Called when reloading changes to our plot point and in constructor
    def reload_mini_widget(self):
        ''' Rebuilds any parts of our UI and information that may have changed when we update our data '''

        #self.reload_timeline_control()
        self.timeline_control.alignment = self.x_alignment

        self.content_control = ft.TextField(
            hint_text="Change x position",
            on_submit=self.change_x_position,
            expand=True,
        )

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.delete_dict()
                ),
            ],
            expand=True,
        )

        self.p.update()