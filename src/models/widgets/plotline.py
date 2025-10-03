import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget
from models.timeline import Timeline


# Class that holds our timeline object, that holds our plotlines
# Stories generally only have one plotline, unless we want multiple timelines, regression, multiverse, etc.
class Plotline(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):

        # Check if we're loading our plotline or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "plotline",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # Saves our data passed in (if there is any)
        )

        # Our timeline controls
        self.timelines = {}

        # If our plotline is new and not loaded, give it default data
        if not loaded:
            self.create_default_plotline_data()  # Create data defaults for our plotline widget
            self.save_dict()    # Save our data to the file

        # Load our timelines from our data
        self.load_timelines()

        # If no plotlines exist, we create a default one to get started
        if len(self.timelines) == 0:
            # Create one like this so we don't call reload_widget before our UI elements are defined
            timeline_directory_path = os.path.join(self.directory_path, "timelines")
            self.timelines["Main Timeline"] = Timeline("Main Timeline", timeline_directory_path, data=None)

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

        # Default data for our plotline widget
        default_plotline_data = {
            
            'pin_location': "bottom",

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

        for timeline in self.timelines.values():
            for arc in timeline.arcs.values():
                self.mini_widgets[arc.title] = arc



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

        # When hovering over timeline or branch, make slightly brighter and thicker. Right clicking allows
        # adding/removing pp, branches, arcs, timeskips, etc.
        # Clicking brings up a mini-menu in the plotline widget to show details and allow editing
        # Data of the control ties back to the object
        # Drag pp, arcs, timeskips to change their date/time??
        # Timeline object andd all its children are gesture detectors
        # Have a show/hide filters button in top left of widget
        # Show zoomed in time dates when zoomed in??

        self.stack.controls.clear()

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
        body = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            expand=True,
            boundary_margin=ft.margin.all(20),
            #on_interaction_start=lambda e: print(e),
            #on_interaction_end=lambda e: print(e),
            #on_interaction_update=lambda e: print(e),
            content=stack,
        )

        # Our column that will display our header filters and body of our widget
        column = ft.Column(
            expand=True,
            #alignment=ft.MainAxisAlignment.CENTER,
            controls=[header, body]
        )

        self.stack.controls.append(column)

        # Column that holds our mini note controls on the right 1/3 of the widget
        mini_widgets_column = ft.Column(
            spacing=6,
            controls=self.mini_widgets.values(),   # They'll only be rendered if visible
        )

        for mini_widget in self.mini_widgets.values():
            if mini_widget.visible:
                mini_widgets_column.expand = True
                break

        # Spacing container to give some space between our body and mini notes
        mini_widgets_row = ft.Row(expand=True)

        # Create a spacinig container and add it so our mini notes only take up the right most 1/3 of widget
        spacing_container = ft.Container(expand=True, ignore_interactions=True)
        mini_widgets_row.controls.append(spacing_container)
        mini_widgets_row.controls.append(spacing_container)

        mini_widgets_row.controls.append(mini_widgets_column)

        # Add the column on top of our stack
        self.stack.controls.append(mini_widgets_row)


        # our tab.content is the column we build above.
        # Our tab content holds the stack that holds our body
        self.tab.content=self.stack  # We add this in combo with our 'tabs' later

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
        
        self.p.update()
        
        