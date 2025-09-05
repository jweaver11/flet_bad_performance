import json
import os

# Live objects that are stored in our timeline object
class Plotline:

    def __init__(self, title: str, file_path: str, data: dict = None):

        self.title = title  # Set our title

        self.file_path = file_path  # Path to our plotline json file

        self.data = data if data is not None else {}    # Set our data

        self.save_dict()


     # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves our data to our plotline json file. '''

        # If no data is passed in (creating new plotline), set default data
        if self.data is None:

            self.data = {
                'title': self.title,
                'file_path': str,   # was timeline_file_path

                'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it

                'plotline_begin_date': None,    # Start and end date of this particular plotline
                'plotline_end_date': None,

                # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
                # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
                'timeskips': {      
                    'title': "timeskip_title", 
                    'start_date': None, 
                    'end_date': None
                },

                # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
                'plot_points': {
                    'title': "Event Title",
                    'description': "Event Description",
                    'date': None,   # These are 'points' on the timeline, so they just get a date, not a start/end range
                    'time': None,   # time during that day
                    'involved_characters': [],
                    'related_locations': [],
                    'related_items': [],
                    #...
                },

                # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
                'arcs': {
                    'arc_title': "Arc Title",
                    'arc_description': "Arc Description",
                    'start_date': None,
                    'end_date': None,
                    'involved_characters': [],
                },
            }
            
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=4)
            #print(f"Plotline saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving plotline to {self.file_path}: {e}")

        