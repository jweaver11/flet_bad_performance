import json
import os

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Timeline:

    # Contsturctor. Accepts tile, file path, and optional data if plotline is beaing created from existing json file
    def __init__(self, title: str, directory_path: str, data: dict = None):

        self.title = title  # Set our title

        self.directory_path = directory_path  # Path to our plotline json file

        self.data = data    # Set our data. If new object, this will be None, otherwise its loaded data

        self.plotpoints = {}

        self.save_dict()    # Saves our data. 


     # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves our data to our plotline json file. '''

        # Our data dict. If no data was passed in, we create default data
        if self.data is None:
            self.data = {
                'title': self.title,
                'directory_path': self.directory_path,   # was timeline_file_path
                'tag': "plotline",

                'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
                'is_expanded': True,

                'plotpoints_are_expanded': True,   # If the plotpoints section is expanded
                'arcs_are_expanded': True,         # If the arcs section is expanded
                'timeskips_are_expanded': True,    # If the timeskips section is expanded

                'start_date': "",    # Start and end date of this particular plotline
                'end_date': "",

                'color': "blue",

                # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
                # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
                'timeskips': {},    # 'timeskip_title': {timeskip object}
                
                # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
                'plot_points': {},      # 'plotpoint_title': {plotpoint object}

                # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
                'arcs': {},     # 'arc_title': {arc object}
            }

        # Open our file and save our data to it
        try:
            with open(self.directory_path, "w") as f:
                json.dump(self.data, f, indent=4)
            #print(f"Plotline saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving plotline to {self.directory_path}: {e}")


    def load_from_dict(self):

        # Path to our file
        plotline_file_path = os.path.join(self.directory_path, f"{self.title}.json")

        default_data = {
            'title': self.title,
            'directory_path': self.directory_path,   # was timeline_file_path
            'tag': "plotline",

            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            'is_expanded': True,

            'plotpoints_are_expanded': True,   # If the plotpoints section is expanded
            'arcs_are_expanded': True,         # If the arcs section is expanded
            'timeskips_are_expanded': True,    # If the timeskips section is expanded

            'start_date': "",    # Start and end date of this particular plotline
            'end_date': "",

            'color': "blue",

            # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
            # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
            'timeskips': {},    # 'timeskip_title': {timeskip object}
            
            # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
            'plot_points': {},      # 'plotpoint_title': {plotpoint object}

            # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
            'arcs': {},     # 'arc_title': {arc object}
        }
        

    def create_plotpoint(self, title: str):
        #from models.timeline.plotpoint import Plotpoint
        #self.plotpoints[title] = Timeline(title)
        pass


        