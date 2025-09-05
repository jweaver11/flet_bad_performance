import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget
from models.plotline import Plotline


# Class that holds our timeline object, that holds our plotlines
# Stories generally only have one plotline, unless we want multiple timelines, regression, multiverse, etc.
class Timeline(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, file_path: str, story: Story):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "timeline",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            file_path = file_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
        )

        self.plotlines = {}

        # Loads our notes data from file, or sets default data if no file exists. Also loads our plotlines
        self.load_from_dict(file_path)

        # Load our widget UI on start after we have loaded our data
        self.reload_widget()

        print(len(self.plotlines), self.story.title)

    # Called whenever there are changes in our data that need to be saved
    def save_dict(self):
        ''' Saves our data to our timeline json file. '''

        try:
            with open(self.data['file_path'], "w") as f:
                json.dump(self.data, f, indent=4)
            #print(f"Plotline saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving timeline to {self.file_path}: {e}")

    # Called at end of constructor
    def load_from_dict(self, file_path: str):
        ''' Loads our timeline data and plotlines data from our seperate plotlines files inside the plotlines directory '''

        # Sets the path to our file based on our title inside of the timeline directory
        timeline_file_path = os.path.join(file_path, "timeline.json")
        
        # This is default data if no file exists. If we are loading from an existing file, this is overwritten
        default_data = {
            'title': self.title,
            'file_path': timeline_file_path,

            'pin_location': "bottom",
            'visible': False,    # If the widget is visible. Flet has this parameter build in, so our objects all use it
            
            'story_start_date': None,  # Start and end date of the main story
            'story_end_date': None,

            'filters': {    # Filters we can apply to change the view of our plotline, while keeping the data intact
                'show_timeskips': True,
                'show_plot_points': True,
                'show_arcs': True,
            },
        }
        

        try:
            # Try to load existing settings from file
            if os.path.exists(timeline_file_path):
                self.file_path = timeline_file_path  # Set the path to the file
                #print(f"Loading character data from {self.path}")
                with open(timeline_file_path, "r") as f:
                    loaded_data = json.load(f)
                
                # Start with default data and update with loaded data
                self.data = {**default_data, **loaded_data}

                # Set specific attributes form our data
                self.title = self.data.get('title', self.title)  # live title = data title, default to current title if error
                self.visible = self.data.get('visible', True)   # live visible bool = data visible bool, default to true if error
                self.file_path = self.data.get('file_path', timeline_file_path)  # live file path = data file path, default to constructed path if error
                
            else:
               
                self.data = default_data    # Set our live object data to our default data
                
                self.save_dict()  # Create the file (or write to it) that saves our live object data

        # Our error for our try statement. Uses our default error if there is an error loading the file/doesn't exist
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Error loading timeline data: {e}")
            # Fall back to default data on error
            self.data = default_data



        # Load our plotlines from the plotlines directory
        plotlines_directory_path = os.path.join(os.path.dirname(timeline_file_path), "plotlines")
        
        try: 
            # Go through all the saved files in the plotlines
            if os.path.exists(plotlines_directory_path):
                for dirpath, dirnames, filenames in os.walk(plotlines_directory_path):
                    for filename in filenames:
                        
                        # All our objects are stored as JSON
                        if filename.endswith(".json"):
                            file_path = os.path.join(dirpath, filename)     # Pass in whatever our directory is (have not tested)
                            try:
                                # Read the JSON file
                                with open(file_path, "r") as f:
                                    plotline_data = json.load(f)
                                    print(plotline_data)
                                
                                # Extract the title from the data
                                plotline_title = plotline_data.get("title", filename.replace(".json", ""))

                                # Create Plotline object with the title, filepath, and data
                                from models.plotline import Plotline
                                plotline = Plotline(plotline_title, file_path, plotline_data)

                                self.plotlines[plotline_title] = plotline
                                #print(self.plotlines[plotline_title].title) 

                            # Handle errors if the path is wrong
                            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                                print(f"Error loading plotline from {filename}: {e}")    

             
                            
        # Handle errors if the path is wrong
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error loading any plotlines from {filename}: {e}")

        if len(self.plotlines) == 0:
            print("No plotlines found for this timeline, creatting one to get started")
            self.create_plotline("Main Plotline")
            print(self.plotlines)
                


    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        #MAKE THE TIMELINE DASHED, AND THE PLOTLINES SOLID. TIMESKIPS WILL SHOW UP THEN
        timeline = ft.Container(
            top=0,
            left=0,
            right=0,
            bottom=0,
            expand=True,
            content=ft.Divider(color=ft.Colors.RED),
        )

        top = ft.Container(
            #top=200,
            #left=200,
            content=ft.Text("hi from " + self.title),
        )

        # Body of the tab, which is the content of flet container
        body = ft.Container(
            expand=True,
            padding=6,
            #alignment=ft.alignment.center,
            #bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.ON_SECONDARY),
            content=ft.Stack(
                expand=True,
                controls=[
                #ft.Text("hi from " + self.title),
                timeline,
                top
            ])
        )

        # our tab.content is the body of our widget that we build above.
        self.tab.content=body   # We add this in combo with our 'tabs' later

        # Sets our actual 'tabs' portion of our widget, since 'tab' needs to nest inside of 'tabs' in order to work
        content = ft.Tabs(
            selected_index=0,
            animation_duration=0,
            #divider_color=ft.Colors.TRANSPARENT,
            padding=ft.padding.all(0),
            label_padding=ft.padding.all(0),
            mouse_cursor=ft.MouseCursor.BASIC,
            tabs=[self.tab]    # Gives our tab control here
        )
        
        # Content of our widget (ft.Container) is our created tabs content
        self.content = content



    def create_plotline(self, title: str):  # -> PLotline
        ''' Creates a new plotline object (branch), saves it to our live story object, and saves it to storage'''

        # Check for invalid names
        if title == "timeline":
            print("Cannot name plotline timeline")
            return
        
        # Check plotline name doesn't already exist
        for key, plotline in self.plotlines.items():
            if plotline.title == title:
                print("Plotline with that title already exists")
                return
        

        # Set file path for our plotline
        file_path = os.path.join(self.story.data['plotlines_directory_path'], f"{title}.json")

        # Set default data for our plotline
        data = {
            'title': title, # Save the title of our plotline
            'file_path': file_path,   # was timeline_file_path

            'visible': True,    # If the widget is visible. Flet has this parameter build in, so our objects all use it

            'start_date': None,    # Start and end date of this particular plotline
            'end_date': None,

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

        # Passes all checks, create our new plotline
        self.plotlines[title] = Plotline(title, file_path, data)

        return
        
        