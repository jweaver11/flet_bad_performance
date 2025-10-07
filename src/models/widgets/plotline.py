import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget
from models.timeline import Timeline


# Class that holds our timeline object, that holds our plotlines
# Stories generally only have one timeline, unless we want multiple timelines, regression, multiverse, etc.
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

        # Check if we loaded our settings data or not
        if data is None:
            loaded = False
        else:
            loaded = True

        # If our settings are new and not loaded, give it default data
        if not loaded:
            self.create_default_plotline_data()  # Create data defaults for our settings widgets

        # Otherwise, verify the loaded data
        else:
            # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
            self.verify_plotline_data()
            

        # Our timeline controls
        self.timelines = {}

        # Load our timelines from our data
        self.load_timelines()

        # If no plotlines exist, we create a default one to get started
        if len(self.timelines) == 0:
            # Create one like this so we don't call reload_widget before our UI elements are defined
            timeline_directory_path = os.path.join(self.directory_path, "timelines")
            self.timelines["Main Timeline"] = Timeline("Main Timeline", timeline_directory_path, page=self.p, story=self.story, data=None)

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


    # Called at end of constructor
    def create_default_plotline_data(self) -> dict:
        ''' Loads our plotline data and timelines data from our seperate timelines files inside the timelines directory '''

        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}

        # Default data for our plotline widget
        default_plotline_data = {
            
            'pin_location': "bottom",
            'tag': "plotline",  

            # Start and end date of entire story
            'story_start_date': "", 
            'story_end_date': "",

            'filters': {    # Filters we can apply to change the view of our plotline, while keeping the data intact
                'show_timeskips': True,
                'show_plot_points': True,
                'show_arcs': True,
            },
        }

        # Update existing data with any new default fields we added
        self.data.update(default_plotline_data)
        return
    
    # Called to verify loaded data
    def verify_plotline_data(self):
        ''' Verify loaded any missing data fields in our plotline '''

        # Required data for all widgets and their types
        required_data_types = {
            'tag': str,
            'story_start_date': str,
            'story_end_date': str,
            'filters': dict,
        }

        # Defaults we can use for any missing fields
        data_defaults = {
            'tag': "plotline",  

            # Start and end date of entire story
            'story_start_date': "", 
            'story_end_date': "",

            'filters': {    # Filters we can apply to change the view of our plotline, while keeping the data intact
                'show_timeskips': True,
                'show_plot_points': True,
                'show_arcs': True,
            },
        }

        # Run through our keys and make sure they all exist. If not, give them default values
        for key, required_data_type in required_data_types.items():
            if key not in self.data or not isinstance(self.data[key], required_data_type):
                self.data[key] = data_defaults[key]  

        self.data['tag'] = "plotline"   # Make sure our tag is always correct

        # Save our updated data
        self.save_dict()
        return


    # Function to load our timline objects from the data 
    def load_timelines(self):
        ''' Loads our timelines from our timelines directory inside our plotline directory '''

        from models.timeline import Timeline
        # Load our timelines from our timeline directory
        timelines_directory_path = os.path.join(self.data['directory_path'], "timelines")
        
        try: 

            # Check every item (file) in this story folder
            for item in os.listdir(timelines_directory_path):

                # Set the file path to this json file so we can open it
                file_path = os.path.join(timelines_directory_path, item)

                # Read the JSON file
                with open(file_path, "r", encoding='utf-8') as f:
                    # Set our data to be passed into our objects
                    timeline_data = json.load(f)

                # Our story title is the same as the folder
                timeline_title = timeline_data.get("title", file_path.replace(".json", ""))

                # Create using the object (not the function) so we can pass in data
                self.timelines[timeline_title] = Timeline(timeline_title, timelines_directory_path, self.p, self.story, timeline_data)              
                            
        # Handle errors if the path is wrong
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error loading any timelines from {timelines_directory_path}: {e}")


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

        load_mini_widgets()



    # Called when we want to create a new plotline
    def create_new_timeline(self, title: str) -> Timeline:  # -> Timeline
        ''' Creates a new plotline object (branch), saves it to our live story object, and saves it to storage'''

        # Check for invalid names
        if title == "plotline":
            print("Cannot name timeline plotline")
            return
        
        # Check timeline name doesn't already exist
        for timeline in self.timelines.values():
            if timeline.title == title:
                print("Plotline with that title already exists")
                return
        

        # Set file path for our plotline
        directory_path = os.path.join(self.story.data['plotline_directory_path'], "timelines")

        # Passes all checks, create our new plotline. We pass in no data, so plotline will use its own default data
        self.timelines[title] = Timeline(title=title, directory_path=directory_path, page=self.p, story=self.story, data=None)
        
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
        # Show zoomed in time dates when zoomed in??

        # TODO If event (pp, arc, etc.) is clicked on left side of screen bring mini widgets on right side, and vise versa

        # Set the mini widgets visibility to false so we can check later if we want to add it to the page
        self.mini_widgets_container.visible = False
        self.content_row.controls.clear()   # Clear our content row so we can rebuild it

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
                timelines.controls.append(timeline)

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

        # Add the body container to our content row
        self.content_row.controls.append(self.body_container)

        # BUILDING MINI WIDGETS - Column that holds our mini note controls on the side 1/3 of the widget
        self.mini_widgets_column.controls = self.mini_widgets   
        
        # Add our column that we build to our mini widgets container
        self.mini_widgets_container.content = self.mini_widgets_column
        
        # Check if we are showing any mini widgets. If we are, add the container to our content row
        for mini_widget in self.mini_widgets_column.controls:
            # TODO: Add check for right or left side mini widgets. Either insert at controls[0] or append
            if mini_widget.visible:
                self.mini_widgets_container.visible = True
                self.content_row.controls.append(self.mini_widgets_container)
                break

        # BUILD OUR TAB CONTENT - Our tab content holds the row of our body and mini widgets containers
        self.tab.content = self.content_row  # We add this in combo with our 'tabs' later
        
        # Add our tab to our tabs control so it will render. Set our widgets content to our tabs control and update the page
        self.tabs.tabs = [self.tab]
        self.content = self.tabs
        self.p.update()
        
        