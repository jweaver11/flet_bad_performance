import flet as ft
import json
import os
from models.story import Story
from models.widget import Widget
from models.plotline.timeline import Timeline


# Class that holds our timeline object, that holds our plotlines
# Stories generally only have one plotline, unless we want multiple timelines, regression, multiverse, etc.
class Plotline(Widget):
    # Constructor
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict = None):
        
        # Initialize from our parent class 'Widget'. 
        super().__init__(
            title = title,  # Title of the widget that will show up on its tab
            tag = "plotline",  # Tag for logic, might be phasing out later so ignore this
            p = page,   # Grabs our original page for convenience and consistency
            directory_path = directory_path,  # Path to our timeline json file
            story = story,       # Saves our story object that this widget belongs to, so we can access it later
            data = data,    # Saves our data passed in (if there is any)
        )

        self.timelines = {}

        # If we don't have data (New story with no plotline data yet), create default data
        if self.data is None:
            self.data = self.create_default_data()  # Create default data if none was passed in

        self.visible = self.data['visible']  # If we will show this widget or not


        # UI elements
        self.filter_plot_points = ft.Checkbox(label="Show Plot Points", value=True, on_change=lambda e: print(self.filter_plot_points.value))
        self.filter_arcs = ft.Checkbox(label="Show Arcs", value=True, on_change=lambda e: print(self.filter_arcs.value))
        self.reset_zoom_button = ft.ElevatedButton("Reset Zoom", on_click=lambda e: print("reset zoom pressed"))

        # The UI element that will display our filters
        self.filters = ft.Row(scroll="auto")

        # Loads our notes data from file, or sets default data if no file exists. Also loads our plotlines
        #self.load_from_dict(directory_path)
        # Load our timelines if we have any
        self.load_timelines()
        self.save_dict()


        # Load our widget UI on start after we have loaded our data
        self.reload_widget() 


    # Called at end of constructor
    def create_default_data(self) -> dict:
        ''' Loads our plotline data and timelines data from our seperate timelines files inside the timelines directory '''
  
        print("Creating default data for plotline: " + self.title)

        return {
            'title': self.title,
            'directory_path': self.directory_path,
            'tag': "timeline",

            'pin_location': "bottom",
            'visible': True,    
            
            # Start and end date of entire story
            'story_start_date': "", 
            'story_end_date': "",

            'filters': {    # Filters we can apply to change the view of our plotline, while keeping the data intact
                'show_timeskips': True,
                'show_plot_points': True,
                'show_arcs': True,
            },
            
        }
        
    def load_timelines(self):

        from models.plotline.timeline import Timeline

        # Sets the path to our file based on our title inside of the plotline directory
        #timeline_file_path = os.path.join(self.directory_path, "plotline.json")
        # ---------------------------------------------------------
        # Load our PLOTLINES from the plotlines directory
        timelines_directory_path = os.path.join(os.path.dirname(self.story.data['plotline_directory_path']), "timelines")

        # title, dir path, data
        
        try: 
            # Go through all the saved files in the plotlines
            if os.path.exists(timelines_directory_path):
                for dirpath, dirnames, filenames in os.walk(timelines_directory_path):
                    for filename in filenames:
                        
                        # All our objects are stored as JSON
                        if filename.endswith(".json"):
                            file_path = os.path.join(dirpath, filename)     # Pass in whatever our directory is (have not tested)
                            try:
                                # Read the JSON file
                                with open(file_path, "r") as f:
                                    timeline_data = json.load(f)
                                    #print(plotline_data)
                                
                                # Extract the title from the data
                                timeline_title = timeline_data.get("title", filename.replace(".json", ""))

                                self.timelines[timeline_title] = Timeline(timeline_title, file_path, timeline_data)
                                #print(self.plotlines[plotline_title].title) 

                            # Handle errors if the path is wrong
                            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                                print(f"Error loading timeline from {filename}: {e}")    

             
                            
        # Handle errors if the path is wrong
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error loading any timelines from {filename}: {e}")

        # If no plotlines exist, we create a default one to get started
        if len(self.timelines) == 0:
            #print("No plotlines found for this timeline, creatting one to get started")
            self.create_timeline("Main Timeline")
            #print(self.timelines)
                

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_widget(self):
        ''' Reloads/Rebuilds our widget based on current data '''

        plotline_filters = []

        # Header that shows our filter options, as well as what plotlines are visible
        # Add reset zoom button later
        header = ft.Row(
            #wrap=True,     # Want to wrap when lots of filters, but forces into column instead of row
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[self.filter_plot_points, self.filter_arcs],
        )

        # Run through our plotlines and create a checkbox for each one for filtering
        for key, timeline in self.timelines.items():
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
                    ft.Divider(color=ft.Colors.with_opacity(0.4, ft.Colors.RED), thickness=2),
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
            if timeline.data['visible']:
                timelines.controls.append(
                    ft.Container(
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
                )

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


        # our tab.content is the column we build above.
        self.tab.content=column   # We add this in combo with our 'tabs' later

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


    # Called when we want to create a new plotline
    def create_timeline(self, title: str) -> Timeline:  # -> Timeline
        ''' Creates a new plotline object (branch), saves it to our live story object, and saves it to storage'''

        # Check for invalid names
        if title == "plotline":
            print("Cannot name timeline plotline")
            return
        
        # Check timeline name doesn't already exist
        for key, timeline in self.timelines.items():
            if timeline.title == title:
                print("Plotline with that title already exists")
                return
        

        # Set file path for our plotline
        file_path = os.path.join(self.story.data['plotline_directory_path'], "timelines", f"{title}.json")

        # Passes all checks, create our new plotline. We pass in no data, so plotline will use its own default data
        self.timelines[title] = Timeline(title, file_path)

        self.reload_widget()  # Reload our widget to show the new plotline

        return 
        
        