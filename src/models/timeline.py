import json
import os
import flet as ft
from models.story import Story

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Timeline(ft.GestureDetector):

    # Contsturctor. Accepts tile, file path, and optional data if plotline is beaing created from existing json file
    def __init__(self, title: str, directory_path: str, page: ft.Page, story: Story, data: dict=None):

        # Initialize our flet control. Theres problems with the data if this is not done first
        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title  # Set our title
        self.directory_path = directory_path  # Path to our plotline json file
        self.p = page  # Page reference for convenience
        self.story = story  # Story object that contains this timeline
        self.data = data    # Set our data. If new object, this will be None, otherwise its loaded data


        # Create our live object dictionaries
        self.branches: dict = {}
        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}
        self.connections: dict = {} # Connect points, arcs, branch, etc.???

        # If no data passed in (Newly created timeline), give it default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in
            self.save_dict()
        
        # Load the rest of our data from the file
        self.load_branches()
        self.load_plot_points() 
        self.load_arcs()
        self.load_time_skips()

        # Builds/reloads our timeline UI
        self.reload_timeline()

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
            'rail_dropdown_is_expanded': True,

            'branches_are_expanded': True,      # If the branches section is expanded
            'plot_points_are_expanded': True,   # If the plotpoints section is expanded
            'arcs_are_expanded': True,         # If the arcs section is expanded
            'time_skips_are_expanded': True,    # If the timeskips section is expanded

            'start_date': "",    # Start and end date of this particular plotline
            'end_date': "",

            'color': "blue",

            'branches': {},   # Branches in the timeline used to seperate disconnected story events that could merge seperately

            'plot_points': {},      # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.

            'arcs': {},     # Arcs, like character arcs, wars, etc. Events that span more than a single point in time

            # Any skips or jumps in the timeline that we want to note. Good for flashbacks, previous events, etc.
            # Stuff that doesnt happen in the main story plotline, but we want to be able to flesh it out, like backstories
            'time_skips': {},    

            # Mark part of timeline as written/drawn
            
        }
    
    # Called in the constructor
    def load_branches(self):
        ''' Loads branches from data into self.branches  '''
        from models.mini_widgets.plotline.branch import Branch

        # Looks up our branches in our data, then passes in that data to create a live object
        for key, data in self.data['branches'].items():
            self.branches[key] = Branch(title=key, owner=self, page=self.p, data=data)
    
    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(title=key, owner=self, page=self.p, data=data)
        
    
    # Called in the constructor 
    def load_arcs(self):
        ''' Loads arcs from data into self.arcs  '''
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            from models.mini_widgets.plotline.arc import Arc
            self.arcs[key] = Arc(title=key, owner=self, page=self.p, data=data)
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''

        for key, data in self.data['time_skips'].items():
            from models.mini_widgets.plotline.time_skip import Time_Skip
            self.time_skips[key] = Time_Skip(title=key, owner=self, page=self.p, data=data)

        return self.time_skips
    
    def create_branch(self, title: str):
        ''' Creates a new branch inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.branch import Branch

        self.branches[title] = Branch(title=title, owner=self, page=self.p)
        self.data['branches'][title] = self.branches[title].data

        self.save_dict()
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        self.plot_points[title] = Plot_Point(title=title, owner=self, page=self.p)
        self.data['plot_points'][title] = self.plot_points[title].data

        self.save_dict()

        self.reload_timeline()
        self.story.plotline.reload_widget()

    # Called when creating a new arc
    def create_arc(self, title: str):
        ''' Creates a new arc inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.arc import Arc

        self.arcs[title] = Arc(title=title, owner=self, page=self.p)
        self.story.plotline.mini_widgets.append(self.arcs[title])

        self.data['arcs'][title] = self.arcs[title].data

        self.save_dict()

        self.reload_timeline()

        self.story.plotline.reload_widget()  # New arc needs to be added to mini widgets in the UI, so we reload the widget

    # Called when creating a new timeskip
    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''

        from models.mini_widgets.plotline.time_skip import Time_Skip

        self.time_skips[title] = Time_Skip(title=title, owner=self, page=self.p)
        self.data['time_skips'][title] = self.time_skips[title].data

        self.save_dict()

    # Called when deleting a plotpoint
    def delete_plot_point(self, title: str):
        ''' Deletes a plotpoint from our timeline object, and updates the data to match '''
        
        if title in self.plot_points:
            del self.plot_points[title]
        
        if title in self.data['plot_points']:
            del self.data['plot_points'][title]
        
        self.save_dict()

    # Called when deleting an arc
    def delete_arc(self, title: str):
        ''' Deletes an arc from our timeline object, and updates the data to match '''
        
        if title in self.arcs:
            del self.arcs[title]
        
        if title in self.data['arcs']:
            del self.data['arcs'][title]
        
        self.save_dict()

    # Called when deleting a timeskip
    def delete_time_skip(self, title: str):
        ''' Deletes a timeskip from our timeline object, and updates the data to match '''
        
        if title in self.time_skips:
            del self.time_skips[title]
        
        if title in self.data['time_skips']:
            del self.data['time_skips'][title]

        self.save_dict()

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_timeline(self):

        # We only show branches, arcc, plotpoints, and timeskips using their UI elements, not their mini widget

        # Content of our Timeline (Gesture detector)
        self.content = ft.Container(
            margin=ft.margin.only(left=20, right=20),
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    #ft.Text(plotline.title, color=ft.Colors.WHITE, size=16),
                    ft.Divider(color=ft.Colors.with_opacity(0.4, ft.Colors.BLUE), thickness=2),
                ],
            )
        )
    



        