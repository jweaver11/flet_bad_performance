import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data

# Class for branches (essentiall sub-timelines) on a timeline. 
# These branches can be connected to each other, and the parent timeline, and its child objects,
# Where as a timeline is independent from other timelines completely
class Branch(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,        # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "branch",                     # Tag to identify what type of object this is
                'start_date': str,                  # Start and end date of the branch, for timeline view
                'end_date': str,                    # Start and end date of the branch, for timeline view
                'color': "secondary",                       # Color of the branch in the timeline
                'plot_points_are_expanded': True,   # If the plotpoints section is expanded
                'arcs_are_expanded': True,          # If the arcs section is expanded
                'time_skips_are_expanded': True,    # If the timeskips section is expanded
                'plot_points': dict,                # Dict of plot points in this branch
                'arcs': dict,                       # Dict of arcs in this branch
                'time_skips': dict,                 # Dict of time skips in this branch
            },
        )


        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}

        self.load_plot_points() 
        self.load_arcs()
        self.load_time_skips()

    

    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(title=key, data=data)
        
    
    # Called in the constructor 
    def load_arcs(self):
        ''' Loads arcs from data into self.arcs  '''
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            from models.mini_widgets.plotline.arc import Arc
            self.arcs[key] = Arc(title=key, data=data)
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''

        for key, data in self.data['time_skips'].items():
            from models.mini_widgets.plotline.time_skip import Time_Skip
            self.time_skips[key] = Time_Skip(title=key, data=data)

        return self.time_skips
    
    def on_hover(self, e: ft.HoverEvent):
        print(e)