import flet as ft


# Class for branches (essentiall sub-timelines) on a timeline. 
# These branches can be connected to each other, and the parent timeline, and its child objects,
# Where as a timeline is independent from other timeilnes completely
class Branch(ft.GestureDetector):

    def __init__(self, title: str, data: dict=None):

        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title  # Required, has no default
        self.data = data    # Optional, if none given, will be created with default values

        # Gives us default data if none was passed in
        if self.data is None:
            self.data = self.create_default_data()


        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}

        self.load_plot_points() 
        self.load_arcs()
        self.load_time_skips()


    def create_default_data(self):

        return {
            'title': self.title,
            'start_date': "",
            'end_date': "",

            'color': "yellow",

            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it

            'plot_points_are_expanded': True,   # If the plotpoints section is expanded
            'arcs_are_expanded': True,         # If the arcs section is expanded
            'time_skips_are_expanded': True,    # If the timeskips section is expanded

            # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
            'plot_points': {},      # 'plotpoint_title': {plotpoint object}

            # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
            'arcs': {},     # 'arc_title': {arc object}

            # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
            # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
            'time_skips': {},    # 'timeskip_title': {timeskip object}
        }
    

    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.plotline.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(title=key, data=data)
        
    
    # Called in the constructor 
    def load_arcs(self):
        ''' Loads arcs from data into self.arcs  '''
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            from models.plotline.arc import Arc
            self.arcs[key] = Arc(title=key, data=data)
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''

        for key, data in self.data['time_skips'].items():
            from models.plotline.time_skip import Time_Skip
            self.time_skips[key] = Time_Skip(title=key, data=data)

        return self.time_skips
    
    def on_hover(self, e: ft.HoverEvent):
        print(e)