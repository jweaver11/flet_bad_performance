'''
Our timeline object that stores plot points, branches, arcs, and time skips.
These objects is displayed in the plotline widget, and store our mini widgets branches, plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from models.widget import Widget
from models.mini_widget import MiniWidget
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Timeline(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 


        # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'rail_dropdown_is_expanded': bool,
                'branches_are_expanded': bool,      # If the branches section is expanded
                'plot_points_are_expanded': bool,   # If the plotpoints section is expanded
                'arcs_are_expanded': bool,         # If the arcs section is expanded
                'time_skips_are_expanded': bool,    # If the timeskips section is expanded
                'start_date': str,    # Start and end date of this particular plotline
                'end_date': str,
                'color': str,
                'branches': dict,   # Branches in the timeline used to seperate disconnected story events that could merge seperately
                'plot_points': dict,      # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
                'arcs': dict,     # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
                'time_skips': dict,  
            },
            tag="timeline"
        )


        # Check if we loaded our mini widget or created a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # If not loaded, set default values. No new data here, just giving values to existing fields
        if not loaded:
            self.data.update({
                'directory_path': self.owner.directory_path,   
                'visible': True,   
                'rail_dropdown_is_expanded': True,
                'branches_are_expanded': True,     
                'plot_points_are_expanded': True,   
                'arcs_are_expanded': True,       
                'time_skips_are_expanded': True,    
                'color': "blue",
            })
            self.save_dict()


        # Create our live object dictionaries
        self.branches: dict = {}
        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}
        self.connections: dict = {} # Connect points, arcs, branch, etc.???

        # Apply our visibility
        self.visible = self.data['visible']

        # The control that shows up in the plotline widget OUTSIDE our mini widget
        self.timeline_control: ft.GestureDetector = ft.GestureDetector() 
        
        # Load the rest of our data from the file
        self.load_branches()
        self.load_plot_points() 
        self.load_arcs()
        self.load_time_skips()

        # Builds/reloads our timeline UI
        self.reload_mini_widget()

    
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
        from models.mini_widgets.plotline.arc import Arc
        
        # Looks up our arcs in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            self.arcs[key] = Arc(title=key, owner=self, page=self.p, data=data)
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''
        from models.mini_widgets.plotline.time_skip import Time_Skip

        for key, data in self.data['time_skips'].items():
            self.time_skips[key] = Time_Skip(title=key, owner=self, page=self.p, data=data)

        return self.time_skips
    
    def create_branch(self, title: str):
        ''' Creates a new branch inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.branch import Branch

        new_branch = Branch(title=title, owner=self, page=self.p, data=None)

        self.branches[title] = new_branch
        self.story.plotline.mini_widgets.append(self.branches[title])

        self.save_dict()

        self.reload_timeline()
        self.story.plotline.reload_widget()  # New branch needs to be added to mini widgets in the UI, so we reload the widget
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.plot_point import Plot_Point

        new_plot_point = Plot_Point(title=title, owner=self, page=self.p, data=None)

        self.plot_points[title] = new_plot_point
        self.story.plotline.mini_widgets.append(self.plot_points[title])

        # Update our data to match
        self.save_dict()

        # Apply our changes in the UI
        self.reload_timeline()
        self.story.plotline.reload_widget()

    # Called when creating a new arc
    def create_arc(self, title: str):
        ''' Creates a new arc inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.plotline.arc import Arc

        # Create the new arc
        new_arc = Arc(title=title, owner=self, page=self.p, data=None)

        # Add our arc to our arcs dict and to the plotline mini widgets list
        self.arcs[title] = new_arc
        self.story.plotline.mini_widgets.append(self.arcs[title]) 

        # Update our data to match
        self.save_dict()

        # Apply our changes in the UI
        self.reload_timeline()
        self.story.plotline.reload_widget()  # New arc needs to be added to mini widgets in the UI, so we reload the widget

    # Called when creating a new timeskip
    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''

        from models.mini_widgets.plotline.time_skip import Time_Skip

        new_time_skip = Time_Skip(title=title, owner=self, page=self.p, data=None)

        self.time_skips[title] = new_time_skip
        self.story.plotline.mini_widgets.append(self.time_skips[title])

        self.save_dict()

        self.reload_timeline()
        self.story.plotline.reload_widget()  # New timeskip needs to be added to mini

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
    def reload_mini_widget(self):

        # We only show branches, arcc, plotpoints, and timeskips using their UI elements, not their mini widget

        # Content of our Timeline (Gesture detector)
        self.timeline_control = ft.Container(
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
    



        