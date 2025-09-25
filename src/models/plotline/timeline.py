import json
import os

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Timeline:

    # Contsturctor. Accepts tile, file path, and optional data if plotline is beaing created from existing json file
    def __init__(self, title: str, directory_path: str, data: dict=None):

        self.title = title  # Set our title
        self.directory_path = directory_path  # Path to our plotline json file
        self.data = data    # Set our data. If new object, this will be None, otherwise its loaded data

        self.branches: dict = {}
        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}

        # If no data passed in (Newly created timeline), give it default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in
            self.save_dict()
        
        # Else if there is data (We loaded it), run the rest of our functions. More efficient than lazy loading
        else:

            self.load_plot_points()  # Load our plotpoints
            self.load_arcs()
            self.load_time_skips()

    # Called when saving changes in our timeline object to file
    def save_dict(self):
        ''' Saves our data dict to our json file '''

        file_path = os.path.join(self.directory_path, f"{self.title}.json")

        try:
            # Create the directory if it doesn't exist. Catches errors from users deleting folders
            os.makedirs(self.directory_path, exist_ok=True)
            
            # Save the data to the file (creates file if doesnt exist)
            with open(file_path, "w", encoding='utf-8') as f:   
                json.dump(self.data, f, indent=4)
        
        # Handle errors
        except Exception as e:
            print(f"Error saving object to {file_path}: {e}")
        

    # Called at the constructor if this is a new timeline that was not loaded
    def create_default_data(self) -> dict:
        ''' Returns a default dict data sctructure for a new timeline '''

        return {
            'title': self.title,
            'directory_path': self.directory_path,   # was timeline_file_path
            'tag': "timeline",

            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            'is_expanded': True,

            'plot_points_are_expanded': True,   # If the plotpoints section is expanded
            'arcs_are_expanded': True,         # If the arcs section is expanded
            'time_skips_are_expanded': True,    # If the timeskips section is expanded

            'start_date': "",    # Start and end date of this particular plotline
            'end_date': "",

            'color': "blue",

            # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
            # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
            'time_skips': {},    # 'timeskip_title': {timeskip object}
            
            # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
            'plot_points': {},      # 'plotpoint_title': {plotpoint object}

            # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
            'arcs': {},     # 'arc_title': {arc object}
        }
    
    # Called in the constructor if we loaded this timeline from a file.
    def load_plot_points(self) -> dict:
        ''' Loads plotpoints from data into self.plotpoints dictionary '''
        
        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, value in self.data['plot_points'].items():
            from models.plotline.plot_point import Plot_Point
            self.plot_points[key] = Plot_Point(**value)
        
        return self.plot_points
    
    def load_arcs(self) -> dict:
        ''' Loads arcs from data into self.arcs dictionary '''
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, value in self.data['arcs'].items():
            from models.plotline.arc import Arc
            self.arcs[key] = Arc(**value)
        
        return self.arcs
    
    def load_time_skips(self) -> dict:

        for key, value in self.data['time_skips'].items():
            from models.plotline.time_skip import Time_Skip
            self.time_skips[key] = Time_Skip(**value)

        return self.time_skips
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''

        from models.plotline.plot_point import Plot_Point

        self.plot_points[title] = Plot_Point(title=title)
        self.data['plot_points'][title] = self.plot_points[title].__dict__

        self.save_dict()

    def create_arc(self, title: str):
        ''' Creates a new arc inside of our timeline object, and updates the data to match '''

        from models.plotline.arc import Arc

        self.arcs[title] = Arc(title=title)
        self.data['arcs'][title] = self.arcs[title].__dict__

        self.save_dict()

    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''

        from models.plotline.time_skip import Time_Skip

        self.time_skips[title] = Time_Skip(title=title)
        self.data['time_skips'][title] = self.time_skips[title].__dict__

        self.save_dict()


    # Called when deleting a plotpoint
    def delete_plot_point(self, title: str):
        ''' Deletes a plotpoint from our timeline object, and updates the data to match '''
        
        if title in self.plot_points:
            del self.plot_points[title]
        
        if title in self.data['plot_points']:
            del self.data['plot_points'][title]
        
        self.save_dict()



        