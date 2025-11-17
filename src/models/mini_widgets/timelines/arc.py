import flet as ft
from models.mini_widget import Mini_Widget
from models.widget import Widget
from handlers.verify_data import verify_data
import flet.canvas as cv
import math


# Class for arcs (essentially sub-timelines that are connected) on a timeline. 
# Arcs split off from the main timeline and can merge back in later. Exp: Characters going on different journeys that rejoin later
class Arc(Mini_Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, key: str, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,                    # Top most timeline this arc belongs too
            father=father,                  # Immediate parent timeline or arc that thisarc belongs too
            page=page,          
            key=key,  
            data=data,         
        ) 

        # Type of arcs?? timeskips, normal, etc??

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "arc",                               # Tag to identify what type of object this is
                'is_timeskip': bool,                        # If this arc is a time skip (skips ahead in time on the timeline)   
                'branch_direction': "top",                  # Direction the arc branches off (top or bottom) from the timeline
                'start_date': str,                          # Start and end date of the branch, for timeline view
                'end_date': str,                            # Start and end date of the branch, for timeline view
                'start_position': int,                      # Start position on the timeline
                'end_position': int,                        # End position on the timeline 
                'color': "primary",                         # Color of the arc in the timeline
                'dropdown_is_expanded': True,               # If the arc dropdown is expanded on the rail
                'plot_points_are_expanded': True,           # If the plotpoints section is expanded
                'arcs_are_expanded': True,                  # If the arcs section is expanded
                'height': 200,                            # Height of the arc on the timeline
                
                'plot_points': dict,                        # Dict of plot points in this branch
                'plot_points_dropdown_color': "primary",    # Color of the plot points dropdown in the rail
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

        self.timeline_control = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda e: print(f"Arc {self.title} tapped"),
            width=self.data['end_position'] - self.data['start_position'],
            left=self.data['start_position'],                                       # X position on the timeline
        )    

        # Loads our three mini widgets into their dicts   
        self.load_plot_points() 

        self.reload_mini_widget()

    
    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.mini_widgets.timelines.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(
                title=key, 
                owner=self.owner, 
                father=self,
                page=self.p, 
                key="plot_points", 
                data=data
            )
            self.owner.mini_widgets.append(self.plot_points[key])  # Plot points need to be in the owners mini widgets list to show up in the UI
        
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.timelines.plot_point import Plot_Point

        # Add our new Plot Point mini widget object to our plot_points dict, and to our owners mini widgets
        self.plot_points[title.capitalize()] = Plot_Point(
            title=title.capitalize(), 
            owner=self.owner, 
            father=self,
            page=self.p, 
            key="plot_points", 
            data=None
        )
        self.owner.mini_widgets.append(self.plot_points[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.story.active_rail.content.reload_rail()
        self.owner.reload_widget()

    # Called when creating a new timeskip
    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.timelines.time_skip import Time_Skip

        # Add our new Time Skip mini widget object to our time_skips dict, and to our owners mini widgets
        self.arcs[title.capitalize()] = Time_Skip(
            title=title.capitalize(), 
            owner=self.owner, 
            father=self,
            page=self.p, 
            key="time_skips", 
            data=None
        )
        self.owner.mini_widgets.append(self.arcs[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.story.active_rail.content.reload_rail()
        self.owner.reload_widget()

    # Called to reload our mini widget content
    def reload_mini_widget(self):

        # Declare how we will draw our arc on the timeline
        arc_start = 0
        arc_sweep = math.pi

        # If we are above the timeline, draw arc downwards. Defaults to drawing upwards
        if self.data.get("branch_direction") == "top":
            arc_start = math.pi              
            arc_sweep = math.pi     

        #self.timeline_control.height = self.arc_height
        self.timeline_control.content = cv.Canvas(
            width=self.data['end_position'] - self.data['start_position'],
            height=self.data.get("height", 200),
            content=ft.Stack(
                controls=[
                    ft.Container(bgcolor=ft.Colors.with_opacity(0.4, "red")),
                    ft.Text(self.title, color=self.data['color'])
                ]
            ),
            shapes=[
                cv.Arc(
                    x=0,
                    y=0,
                    width=self.data['end_position'] - self.data['start_position'],
                    height=self.data.get("height", 200),
                    start_angle=arc_start,
                    sweep_angle=arc_sweep,
                    paint=ft.Paint(
                        color=self.data['color'],
                        stroke_width=3,
                        style=ft.PaintingStyle.STROKE
                    )
                )
            ],
        
        )


        
        # Needs to show the owner
        # Distinct plot arc vs character arc??

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