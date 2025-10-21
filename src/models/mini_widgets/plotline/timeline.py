'''
Our timeline object that stores plot points, branches, arcs, and time skips.
These objects is displayed in the plotline widget, and store our mini widgets branches, plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from models.widget import Widget
from models.mini_widgets.plotline.branch import Branch
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timeline widget, so need for this to be a flet control
class Timeline(Branch):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            timeline=self,
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "timeline",
                'rail_dropdown_is_expanded': True,
                'branches_are_expanded': True,      # If the branches section is expanded
                'plot_points_are_expanded': True,   # If the plotpoints section is expanded
                'arcs_are_expanded': True,         # If the arcs section is expanded
                'time_skips_are_expanded': True,    # If the timeskips section is expanded
                'start_date': str,    # Start and end date of this particular plotline
                'end_date': str,
                'color': "primary",
                'branches': dict,   # Branches in the timeline used to seperate disconnected story events that could merge seperately
                'plot_points': dict,      # Events that happen during our stories plot. Character deaths, catastrophies, major events, etc.
                'arcs': dict,     # Arcs, like character arcs, wars, etc. Events that span more than a single point in time
                'time_skips': dict,  
            },
        ) 


        # Create our live object dictionaries
        self.branches: dict = {}
        self.plot_points: dict = {} # Declare plot_points dictionary
        self.arcs: dict = {}
        self.time_skips: dict = {}
        self.connections: dict = {} # Connect points, arcs, branch, etc.???

        # The control that shows up in the plotline widget OUTSIDE our mini widget
        self.timeline_control: ft.GestureDetector = ft.GestureDetector() 
        
        # Load the rest of our data from the file
        self.load_branches()

        # Builds/reloads our timeline UI
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
                timeline=self,  # Branches can't own each other, only timelines can
                data=data
            )
            self.owner.mini_widgets.append(self.branches[key])  # Branches need to be in the owners mini widgets list to show up in the UI
    
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
            timeline=self,
            data=None
        )
        self.owner.mini_widgets.append(self.branches[title])

        # Apply our changes in the UI
        self.reload_mini_widget()
        self.owner.reload_widget()
        

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_mini_widget(self):

        
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
    



        