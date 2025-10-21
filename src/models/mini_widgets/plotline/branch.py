import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data
#from models.mini_widgets.plotline.timeline import Timeline

# Class for branches (essentiall sub-timelines) on a timeline. 
# These branches can be connected to each other, and the parent timeline, and its child objects,
# Where as a timeline is independent from other timelines completely
class Branch(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], timeline, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,        # owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

        # The timeline this arc belongs to
        self.timeline = timeline  

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "branch",                     # Tag to identify what type of object this is
                'start_date': str,                  # Start and end date of the branch, for timeline view
                'end_date': str,                    # Start and end date of the branch, for timeline view
                'color': "secondary",                       # Color of the branch in the timeline
                'is_expanded': True,                  # If the branch dropdown is expanded on the rail
                'branches_are_expanded': True,      # If the branches section is expanded
                'plot_points_are_expanded': True,   # If the plotpoints section is expanded
                'arcs_are_expanded': True,          # If the arcs section is expanded
                'time_skips_are_expanded': True,    # If the timeskips section is expanded
                'branches': dict,                  # Dict of (sub) branches in this branch
                'plot_points': dict,                # Dict of plot points in this branch
                'arcs': dict,                       # Dict of arcs in this branch
                'time_skips': dict,                 # Dict of time skips in this branch
                'rail_dropdown_is_expanded': True,     
            },
        )

        # Declare dicts of our data types 
        self.branches: dict = {}    
        self.plot_points: dict = {} 
        self.arcs: dict = {}
        self.time_skips: dict = {}

        self.load_branches()      
        self.load_plot_points() 
        self.load_arcs()
        self.load_time_skips()

        self.reload_mini_widget()


    # Called in the constructor
    def load_branches(self):
        ''' Loads branches from data into self.branches  '''
        from models.mini_widgets.plotline.branch import Branch

        # Looks up our branches in our data, then passes in that data to create a live object
        for key, data in self.data['branches'].items():
            self.branches[key] = Branch(
                title=key, 
                owner=self.owner, 
                page=self.p, 
                dictionary_path=self.dictionary_path + ['branches', key],
                timeline=self.timeline,  # Branches can't own each other, only timelines can
                data=data
            )
            self.owner.mini_widgets.append(self.branches[key])  # Branches need to be in the owners mini widgets list to show up in the UI
    
    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(
                title=key, 
                owner=self.owner, 
                page=self.p, dictionary_path=self.dictionary_path + ['plot_points', key], 
                branch_line=self,
                data=data
            )
            self.owner.mini_widgets.append(self.plot_points[key])  # Plot points need to be in the owners mini widgets list to show up in the UI
        
    
    # Called in the constructor 
    def load_arcs(self):
        ''' Loads arcs from data into self.arcs  '''
        from models.mini_widgets.plotline.arc import Arc
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            self.arcs[key] = Arc(
                title=key, 
                owner=self.owner, 
                page=self.p, 
                dictionary_path=self.dictionary_path + ['arcs', key],
                branch_line=self,
                data=data
            )
            self.owner.mini_widgets.append(self.arcs[key])  # Arcs need to be in the owners mini widgets list to show up in the UI
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''
        from models.mini_widgets.plotline.time_skip import Time_Skip

        for key, data in self.data['time_skips'].items():
            self.time_skips[key] = Time_Skip(
                title=key, 
                owner=self.owner, 
                page=self.p, 
                dictionary_path=self.dictionary_path + ['time_skips', key],
                branch_line=self,
                data=data
            )
            self.owner.mini_widgets.append(self.time_skips[key])  # Time skips need to be in the owners mini widgets list to show up in the UI
    
    # Called when creating a new branch
    def create_branch(self, title: str):
        ''' Creates a new branch inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.branch import Branch

        # Add our new Branch mini widget object to our branches dict, and to our owners mini widgets
        self.branches[title] = Branch(
            title=title, 
            owner=self.owner, 
            page=self.p, 
            dictionary_path=self.dictionary_path + ['branches', title], 
            timeline=self.timeline,
            data=None
        )
        self.owner.mini_widgets.append(self.branches[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.reload_widget()
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        # Add our new Plot Point mini widget object to our plot_points dict, and to our owners mini widgets
        self.plot_points[title] = Plot_Point(
            title=title, 
            owner=self.owner, 
            page=self.p, 
            dictionary_path=self.dictionary_path + ['plot_points', title], 
            branch_line=self,
            data=None
        )
        self.owner.mini_widgets.append(self.plot_points[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.reload_widget()

    # Called when creating a new arc
    def create_arc(self, title: str):
        ''' Creates a new arc inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.arc import Arc

        # Add our new Arc mini widget object to our arcs dict, and to our owners mini widgets
        self.arcs[title] = Arc(
            title=title, 
            owner=self.owner, 
            page=self.p, 
            dictionary_path=self.dictionary_path + ['arcs', title], 
            branch_line=self,
            data=None
        )
        self.owner.mini_widgets.append(self.arcs[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.reload_widget()

    # Called when creating a new timeskip
    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.time_skip import Time_Skip

        # Add our new Time Skip mini widget object to our time_skips dict, and to our owners mini widgets
        self.time_skips[title] = Time_Skip(
            title=title, 
            owner=self.owner, 
            page=self.p, 
            dictionary_path=self.dictionary_path + ['time_skips', title], 
            branch_line=self,
            data=None
        )
        self.owner.mini_widgets.append(self.time_skips[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.reload_widget()


    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.owner.delete_mini_widget(self)
                ),
            ],
            expand=True,
        )

        self.p.update()