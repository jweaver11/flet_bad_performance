'''
Our timeline object that stores plot points, arcs, and time skips.
These objects is displayed in the timelines widget, and store our mini widgets plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from models.story import Story
from models.widget import Widget
from models.mini_widgets.timelines.arc import Arc
from handlers.verify_data import verify_data

# Live objects that are stored in our timeline object
# We read data from this object, but it is displayed in the timelines widget, so need for this to be a flet control
class Timeline(Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Parent constructor
        super().__init__(
            title = title,  
            p = page,   
            directory_path = directory_path, 
            story = story,     
            data = data,  
        ) 


        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "timeline",
                'filters': {   
                    'show_timeskips': True,
                    'show_plot_points': True,
                    'show_arcs': True,
                },        
                'information_display': {
                    'visibility': True,
                },
                'start_date': str,                  # Start and end date of the branch, for timeline view
                'end_date': str,                    # Start and end date of the branch, for timeline view
                'color': "primary",                 # Color of the branch in the timeline
                'is_expanded': True,                # If the branch dropdown is expanded on the rail
                'plot_points_are_expanded': True,   # If the plotpoints section is expanded
                'arcs_are_expanded': True,          # If the arcs section is expanded
                'time_skips_are_expanded': True,    # If the timeskips section is expanded
                'plot_points': dict,                # Dict of plot points in this branch
                'time_skips': dict,                 # Dict of time skips in this branch
                'arcs': dict,                       # Dict of arcs in this branch
                'connections': dict,                # Connect points, arcs, branch, etc.???
                'rail_dropdown_is_expanded': True,  # If the rail dropdown is expanded  
                'description': str,
                'events': list,                     # Step by step of plot events through the arc. Call plot point??
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        ) 

        # Declare and create our information display, which is our timelines mini widget 
        self.information_display = None
        self.create_information_display()
        

        # Declare dicts of our data types   
        self.arcs: dict = {}
        self.plot_points: dict = {} 
        self.time_skips: dict = {}
        self.connections: dict = {}  # Needed????



        # Loads our three mini widgets into their dicts
        self.load_arcs()
        self.load_plot_points()
        self.load_time_skips()
        

        

        # Builds/reloads our timeline UI
        self.reload_widget()

    def create_information_display(self):
        ''' Creates our timeline information display mini widget '''
        from models.mini_widgets.timelines.timeline_information_display import Timeline_Information_Display
        self.information_display = Timeline_Information_Display(
            title=self.title,
            owner=self,
            father=self,
            page=self.p,
            dictionary_path="none",     # Not used, but its required so just whatever works
            data=None,      # It uses our data, so we don't need to give it a copy that we would have to constantly maintain
        )
        # Add to our mini widgets so it shows up in the UI
        self.mini_widgets.append(self.information_display)

    # Called in the constructor
    def load_arcs(self):
        ''' Loads branches from data into self.branches  '''

        # Looks up our branches in our data, then passes in that data to create a live object
        for key, data in self.data['arcs'].items():
            self.arcs[key] = Arc(
                title=key, 
                owner=self, 
                father=self,
                page=self.p, 
                dictionary_path="arcs",
                data=data
            )
            self.mini_widgets.append(self.arcs[key])  # Branches need to be in the owners mini widgets list to show up in the UI
    
    # Called in the constructor
    def load_plot_points(self):
        ''' Loads plotpoints from data into self.plotpoints  '''
        from models.mini_widgets.timelines.plot_point import Plot_Point

        # Looks up our plotpoints in our data, then passes in that data to create a live object
        for key, data in self.data['plot_points'].items():
            self.plot_points[key] = Plot_Point(
                title=key, 
                owner=self, 
                father=self,
                page=self.p, 
                dictionary_path="plot_points", 
                data=data
            )
            self.mini_widgets.append(self.plot_points[key])  # Plot points need to be in the owners mini widgets list to show up in the UI
        
    
    # Called in the constructor
    def load_time_skips(self):
        ''' Loads timeskips from data into self.time_skips  '''
        from models.mini_widgets.timelines.time_skip import Time_Skip

        for key, data in self.data['time_skips'].items():
            self.time_skips[key] = Time_Skip(
                title=key, 
                owner=self, 
                father=self,
                page=self.p, 
                dictionary_path="time_skips",
                data=data
            )
            self.mini_widgets.append(self.time_skips[key])  # Time skips need to be in the owners mini widgets list to show up in the UI
    
    # Called when creating a new arc
    def create_arc(self, title: str):
        ''' Creates a new arc inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.timelines.arc import Arc

        # Add our new Arc mini widget object to our arcs dict, and to our owners mini widgets
        self.arcs[title] = Arc(
            title=title, 
            owner=self, 
            father=self,
            page=self.p, 
            dictionary_path="arcs", 
            data=None
        )
        self.mini_widgets.append(self.arcs[title])

        # Apply our changes in the UI
        self.story.active_rail.content.reload_rail()
        self.reload_widget()
        
    # Called when creating a new plotpoint
    def create_plot_point(self, title: str):
        ''' Creates a new plotpoint inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.timelines.plot_point import Plot_Point

        # Add our new Plot Point mini widget object to our plot_points dict, and to our owners mini widgets
        self.plot_points[title] = Plot_Point(
            title=title, 
            owner=self, 
            father=self,
            page=self.p, 
            dictionary_path="plot_points", 
            data=None
        )
        self.mini_widgets.append(self.plot_points[title])

        # Apply our changes in the UI
        self.story.active_rail.content.reload_rail()
        self.reload_widget()

    # Called when creating a new timeskip
    def create_time_skip(self, title: str):
        ''' Creates a new timeskip inside of our timeline object, and updates the data to match '''
        from models.mini_widgets.timelines.time_skip import Time_Skip

        # Add our new Time Skip mini widget object to our time_skips dict, and to our owners mini widgets
        self.time_skips[title] = Time_Skip(
            title=title, 
            owner=self, 
            father=self,
            page=self.p, 
            dictionary_path="time_skips", 
            data=None
        )
        self.mini_widgets.append(self.time_skips[title])

        # Apply our changes in the UI
        self.story.active_rail.content.reload_rail()
        self.reload_widget()
   

    def on_hover(self, e: ft.HoverEvent):
        #print(e)
        pass
        # Grab local mouse to figure out x and map it to our timeline

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):

        # Right clicking arc or plotpoints opens multiple mini widgets at the same time
        
        # TODO:
        # When hovering over timeline or branch, make slightly brighter and thicker. Right clicking allows
        # adding/removing pp, branches, arcs, timeskips, etc.
        # Clicking brings up a mini-menu in the timelines widget to show details and allow editing
        # Data of the control ties back to the object
        # Drag pp, arcs, timeskips to change their date/time??
        # Timeline object andd all its children are gesture detectors
        # Have a show/hide filters button in top left of widget
        # Show zoomed in time dates when zoomed in??s
        # If event (pp, arc, etc.) is clicked on left side of screen bring mini widgets on right side, and vise versa

        #timelines_filters = []

        # The control that shows up in the timelines widget OUTSIDE our mini widget
        self.timeline_control: ft.GestureDetector = ft.GestureDetector() 


        # The UI element that will display our filters
        filters = ft.Row(scroll="auto")

        # UI elements
        filter_plot_points = ft.Checkbox(label="Show Plot Points", value=True, on_change=lambda e: print(self.filter_plot_points.value))
        filter_arcs = ft.Checkbox(label="Show Arcs", value=True, on_change=lambda e: print(self.filter_arcs.value))
        reset_zoom_button = ft.ElevatedButton("Reset Zoom", on_click=lambda e: print("reset zoom pressed"))

        # Header that shows our filter options, as well as what timeliness are visible
        # Add reset zoom button later
        header = ft.Row(
            #wrap=True,     # Want to wrap when lots of filters, but forces into column instead of row
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[filter_plot_points, filter_arcs],
        )


        filters.controls.append(reset_zoom_button)
            
        # Add our timeliness as filters to our header
        header.controls.append(filters)

        # MAKE INVISIBLE IN FUTURE, ONLY EDGES ARE VERTICAL LINES
        # The timeline shown under our timeliness that that will display timeskips, etc. 
        timeline = ft.Container(
            margin=ft.margin.all(10),
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(expand=True,),
                    ft.Divider(color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE), thickness=2),
                    ft.Container(expand=True,),
                ]
            )
        )


        # The body that is our interactive viewer, allowing zoom in and out and moving around
        interactive_viewer = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            expand=True,
            boundary_margin=ft.margin.all(20),
            #on_interaction_start=lambda e: print(e),
            #on_interaction_end=lambda e: print(e),
            #on_interaction_update=lambda e: print(e),
            content=timeline,
        )

        self.body_container.content = ft.Column([
            header,
            interactive_viewer
        ])

        self._render_widget()
    



        