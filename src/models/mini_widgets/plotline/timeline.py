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
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
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
            self.branches[key] = Branch(
                title=key, 
                owner=self.owner, 
                page=self.p, 
                dictionary_path=self.dictionary_path + ['branches', key],
                timeline=self,  # Branches can't own each other, only timelines can
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

    # Called when deleting a branch
    def delete_branch(self, branch):
        ''' Deletes a branch from our timeline object, and updates the data to match '''

        try:
            # Grab our title
            title = branch.title

            # Delete from our data, our live branches dict, and from our owners mini widgets list
            del self.data['branches'][title]
            del self.branches[title]
            self.owner.delete_mini_widget(branch)

            # Save our changes
            self.save_dict()

        # Errors
        except Exception as e:
            print(f"Error deleting branch {title}: {e}")

    # Called when deleting a plotpoint
    def delete_plot_point(self, plot_point):
        ''' Deletes a plotpoint from our timeline object, and updates the data to match '''

        try:
            # Grab our title
            title = plot_point.title

            # Delete from our data, our live plotpoints dict, and from our owners mini widgets list
            del self.data['plot_points'][title]
            del self.plot_points[title]
            self.owner.delete_mini_widget(plot_point)

            # Save our changes
            self.save_dict()
                
        # Errors
        except Exception as e:
            print(f"Error deleting plot point {title}: {e}")

    # Called when deleting an arc
    def delete_arc(self, arc):
        ''' Deletes an arc from our timeline object, and updates the data to match '''
        
        try:
            # Grab our title
            title = arc.title

            # Delete from our data, our live arcs dict, and from our owners mini widgets list
            del self.data['arcs'][title]
            del self.arcs[title]
            self.owner.delete_mini_widget(arc)

            # Save our changes
            self.save_dict()
        
        # Errors
        except Exception as e:
            print(f"Error deleting arc {title}: {e}") 

    # Called when deleting a timeskip
    def delete_time_skip(self, time_skip):
        ''' Deletes a timeskip from our timeline object, and updates the data to match '''
        
        try:
            # Grab our title
            title = time_skip.title

            # Delete from our data, our live time_skips dict, and from our owners mini widgets list
            del self.data['time_skips'][title]
            del self.time_skips[title]
            self.owner.delete_mini_widget(time_skip)

            # Save our changes
            self.save_dict()
        
        # Errors
        except Exception as e:
            print(f"Error deleting time skip {title}: {e}")

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_mini_widget(self):

        # We only show branches, arc, plotpoints, and timeskips using their UI elements, not their mini widget

        
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
    



        