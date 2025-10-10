'''
Our widget class that displays our plot and timelines of our story.
Our stories have one plotline, but can contain multiple timelines if doing regression/timetravel/multiverse
Our timelines (stored in their own directory) contain branches, plot points, arcs, and timeskips
'''

import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget
from models.mini_widgets.plotline.timeline import Timeline
from handlers.verify_data import verify_data


class Plotline(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # Saves our data passed in (if there is any)
        )

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': str,
                'story_start_date': str,
                'story_end_date': str,
                'filters': dict,

                # Dict of timelines in this plotline. Timelines are the only stored mini widgets in plotlines data
                'timelines': dict,  
            },
            tag="plotline"
        )

        # Check if we loaded our character or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If not loaded, set default values. No new data here, just giving values to existing fields
        if not loaded:
            self.data.update({
                'pin_location': "bottom",     # Start our plotline on the bottom pin
                'filters': {   
                    'show_timeskips': True,
                    'show_plot_points': True,
                    'show_arcs': True,
                },
                'mini_widgets': {
                    'timelines': {},
                }
            })
            self.save_dict()
            

        # Our timeline controls
        self.timelines = {}

        # Load our timelines from our data
        self.load_timelines()

        # Set visibility from our data
        self.visible = self.data['visible']  # If we will show this widget or not

        # The UI element that will display our filters
        self.filters = ft.Row(scroll="auto")

        # UI elements
        self.filter_plot_points = ft.Checkbox(label="Show Plot Points", value=True, on_change=lambda e: print(self.filter_plot_points.value))
        self.filter_arcs = ft.Checkbox(label="Show Arcs", value=True, on_change=lambda e: print(self.filter_arcs.value))
        self.reset_zoom_button = ft.ElevatedButton("Reset Zoom", on_click=lambda e: print("reset zoom pressed"))

        # Load our widget UI on start after we have loaded our data
        self.reload_widget() 

    
    
    # Function to load our timline objects from the data 
    def load_timelines(self):
        ''' Loads our timelines from our timelines directory inside our plotline directory '''

        from models.mini_widgets.plotline.timeline import Timeline
        
        try: 

            # Check every item (file) in this story folder
            for timeline_title, timeline_data in self.data['mini_widgets']['timelines'].items():

                # Create using the object (not the function) so we can pass in data
                self.timelines[timeline_title] = Timeline(timeline_title, self, self.p, timeline_data) 

            # If no plotlines exist, we create a default one to get started
            if len(self.timelines) == 0:
                print("No timelines found, creating default timeline")
                self.timelines["Main Timeline"] = Timeline(title="Main Timeline", owner=self, page=self.p, data=None)             
                            
        # Handle errors if the path is wrong
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error loading timelines: {e}")


        # After our timeline has been created, it will have loaded its branches, plot points, arcs, and timeskips
        # We take those, and load them into our mini widgets list, since our timeline is not a widget itself
        # And uses them differently
        def load_mini_widgets():

            for timeline in self.timelines.values():

                for branch in timeline.branches.values():
                    self.mini_widgets.append(branch)

                for plot_point in timeline.plot_points.values():
                    self.mini_widgets.append(plot_point)

                for arc in timeline.arcs.values():
                    self.mini_widgets.append(arc)

                for time_skip in timeline.time_skips.values():
                    self.mini_widgets.append(time_skip)

        #load_mini_widgets()



    # Called when we want to create a new plotline
    def create_new_timeline(self, title: str) -> Timeline:  # -> Timeline
        ''' Creates a new plotline object (branch), saves it to our live story object, and saves it to storage'''


        # Passes all checks, create our new plotline. We pass in no data, so plotline will use its own default data
        self.timelines[title] = Timeline(title, self, self.p, data=None)
        
        self.reload_widget()  # Reload our widget to show the new timeline

        return 
    
    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        # TODO:
        # When hovering over timeline or branch, make slightly brighter and thicker. Right clicking allows
        # adding/removing pp, branches, arcs, timeskips, etc.
        # Clicking brings up a mini-menu in the plotline widget to show details and allow editing
        # Data of the control ties back to the object
        # Drag pp, arcs, timeskips to change their date/time??
        # Timeline object andd all its children are gesture detectors
        # Have a show/hide filters button in top left of widget
        # Show zoomed in time dates when zoomed in??s
        # If event (pp, arc, etc.) is clicked on left side of screen bring mini widgets on right side, and vise versa

        plotline_filters = []

        # Header that shows our filter options, as well as what plotlines are visible
        # Add reset zoom button later
        header = ft.Row(
            #wrap=True,     # Want to wrap when lots of filters, but forces into column instead of row
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.filter_plot_points, self.filter_arcs],
        )

        # Run through our plotlines and create a checkbox for each one for filtering
        for timeline in self.timelines.values():
            #print(plotline.title, " is being shown")
            plotline_filters.append(
                ft.Checkbox(
                    label=timeline.title, 
                    value=True, 
                    data=timeline.title,
                    on_change=lambda e: print(timeline.title + " is now " + str(timeline.data['visible']))
                )
            )

        plotline_filters.append(self.reset_zoom_button)
            
        # Add our plotlines as filters to our header
        header.controls.extend(plotline_filters)

        # MAKE INVISIBLE IN FUTURE, ONLY EDGES ARE VERTICAL LINES
        # The timeline shown under our plotlines that that will display timeskips, etc. 
        plotline = ft.Container(
            top=0,
            left=0,
            right=0,
            bottom=0,
            margin=ft.margin.all(10),
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(expand=True,),
                    ft.Divider(color=ft.Colors.with_opacity(0.3, ft.Colors.RED), thickness=2),
                    ft.Container(expand=True,),
                ]
            )
        )

        timelines = ft.Column(
            top=0,
            left=0,
            right=0,
            bottom=0,
            expand=True,
        )

        timelines.controls.append(ft.Container(expand=True))

        for timeline in self.timelines.values():
            if timeline.visible:
                timelines.controls.append(timeline.timeline_control)

            for arc in timeline.arcs.values():
                if arc.visible:
                    timelines.controls.append(arc.timeline_control)
                

        timelines.controls.append(ft.Container(expand=True))

        # Stack that holds our timeline and any plotlines that sit overtop it (may not use in future)
        stack = ft.Stack(
            expand=True,
            controls=[
                plotline,
                timelines
            ]
        )


        # The body that is our interactive viewer, allowing zoom in and out and moving around
        self.body_container.content = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            expand=True,
            boundary_margin=ft.margin.all(20),
            #on_interaction_start=lambda e: print(e),
            #on_interaction_end=lambda e: print(e),
            #on_interaction_update=lambda e: print(e),
            content=stack,
        )

        print("Number of timelines in plotline: " + str(len(self.timelines)))

        self.render_widget()
        
        