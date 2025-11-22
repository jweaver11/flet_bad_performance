'''
Our timeline object that stores plot points, arcs, and time skips.
These objects is displayed in the timelines widget, and store our mini widgets plot points, arcs, and time skips.
'''

import json
import os
import flet as ft
from styles.menu_option_style import Menu_Option_Style
from models.story import Story
from models.widget import Widget
from models.mini_widgets.timelines.arc import Arc
from handlers.verify_data import verify_data
import flet.canvas as cv


class Timeline(Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, page: ft.Page, directory_path: str, story: Story, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title = title,  
            page = page,   
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
                'information_display': {'visibility': True},
                'time_label': str,                          # Label for the time axis (any str they want)
                'start_date': str,                          # Start and end date of the branch, for timeline view
                'end_date': str,                            # Start and end date of the branch, for timeline view
                'color': "primary",                         # Color of the branch in the timeline
                'dropdown_is_expanded': True,               # If the branch dropdown is expanded on the rail
                'plot_points_are_expanded': True,           # If the plotpoints section is expanded
                'plot_points_dropdown_color': "primary",    # Color of the plot points dropdown in the rail
                'arcs_are_expanded': True,                  # If the arcs section is expanded
                'arcs_dropdown_color': "primary",           # Color of the arcs dropdown in the rail

                'plot_points': dict,                        # Dict of plot points in this branch
                'time_skips': dict,                         # Dict of time skips in this branch
                'arcs': dict,                               # Dict of arcs in this branch
                'connections': dict,                        # Connect points, arcs, branch, etc.???
                'rail_dropdown_is_expanded': True,          # If the rail dropdown is expanded  
                'description': str,
                'events': list,                             # Step by step of plot events through the arc. Call plot point??
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
                'divisions': 10,                            # Number of divisions on the timeline

                'left_edge_label': 0,                    # Label for the left edge of the timeline
                'right_edge_label': 10,                  # Label for the right edge of the timeline
            },
        ) 

        # For tracking mouse position on timeline when adding new items
        self.x_alignment: float = 0.00

        # Declare and create our information display, which is our timelines mini widget 
        self.information_display: ft.Container = None
        self.create_information_display()
        

        # Declare dicts of our data types   
        self.arcs: dict = {}        # TODO: No more infinite arcs
        self.plot_points: dict = {} 
        self.time_skips: dict = {}
        self.connections: dict = {}  # Needed????


        # Loads our three mini widgets into their dicts
        self.load_arcs()
        self.load_plot_points()
        self.load_time_skips()
        
        # UI elements
        self.timeline_control = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            expand=True,
            on_exit=self.on_exit,        
            on_tap=self.on_clicked,
            hover_interval=20,
        )

        # Edges of our timeline
        self.timeline_left_edge = ft.GestureDetector(
            height=50,
            data=0,
            content=ft.VerticalDivider(color=ft.Colors.with_opacity(0.7, self.data.get('color', "primary")), thickness=3, width=3), 
            mouse_cursor=ft.MouseCursor.CLICK,
            on_exit=self.on_exit,
            on_enter=self.on_enter,
            on_tap=self.on_click,
        )
        self.timeline_right_edge = ft.GestureDetector(
            height=50,
            data=200,
            content=ft.VerticalDivider(color=ft.Colors.with_opacity(0.7, self.data.get('color', "primary")), thickness=3, width=3), 
            mouse_cursor=ft.MouseCursor.CLICK,
            on_exit=self.on_exit,
            on_enter=self.on_enter,
            on_tap=self.on_click,
        )

        # Text field for adding new items
        self.new_item_text_field = ft.TextField(hint_text="Add new item here", )
        #on_blur=self.hide_new_item_container

        # Container that contains text box for adding new items
        self.new_item_container = ft.Stack(
            expand=True,
            visible=False,
            alignment=ft.Alignment(0, 0),
            controls=[self.new_item_text_field]
        )
        

        # Builds/reloads our timeline UI
        self.reload_widget()

    # Called in the constructor
    def create_information_display(self):
        ''' Creates our timeline information display mini widget '''
        from models.mini_widgets.timelines.timeline_information_display import Timeline_Information_Display
        
        self.information_display = Timeline_Information_Display(
            title=self.title,
            owner=self,
            father=self,
            page=self.p,
            key="none",     # Not used, but its required so just whatever works
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
                key="arcs",
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
                key="plot_points", 
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
                key="time_skips",
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
            key="arcs", 
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
            key="plot_points", 
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
            key="time_skips", 
            data=None
        )
        self.mini_widgets.append(self.time_skips[title])

        # Apply our changes in the UI
        self.story.active_rail.content.reload_rail()
        self.reload_widget()

    # Called when right clicking our controls for either timeline or an arc
    def get_menu_options(self) -> list[ft.Control]:
        return [
            Menu_Option_Style(
                #on_click=self.new_timeline_clicked,
                data="arc",
                content=ft.Row([
                    ft.Icon(ft.Icons.CIRCLE_OUTLINED),
                    ft.Text("Arc", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                #on_click=self.new_timeline_clicked,
                data="plot_point",
                content=ft.Row([
                    ft.Icon(ft.Icons.ADD_LOCATION_OUTLINED),
                    ft.Text("Plot Point", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
        ]
    
    # Called when mouse enters our timeline area
    def on_enter(self, e: ft.HoverEvent = None):
        ''' Highlights our timeline control for visual feedback '''

        # During hover, set our x position so we know where to add new items on the timeline
        self.x_alignment = (e.control.data - 100) / 100

        # Make the edges highlight
        self.timeline_left_edge.content.color = ft.Colors.with_opacity(1, self.data.get('color', "primary"))
        self.timeline_right_edge.content.color = ft.Colors.with_opacity(1, self.data.get('color', "primary"))

        # Make the main timeline control highlight
        for control in self.timeline_control.content.controls:
            if isinstance(control, ft.GestureDetector):
                control.content.color = ft.Colors.with_opacity(1, self.data.get('color', "primary"))

        # Apply the update
        self.p.update()

    # Called when mouse exits our timeline area
    def on_exit(self, e: ft.HoverEvent):
        ''' Un-highlights our timeline control for visual feedback '''
        
        self.timeline_left_edge.content.color = ft.Colors.with_opacity(.7, self.data.get('color', "primary"))
        self.timeline_right_edge.content.color = ft.Colors.with_opacity(.7, self.data.get('color', "primary"))

        for control in self.timeline_control.content.controls:
            if isinstance(control, ft.GestureDetector):
                control.content.color = ft.Colors.with_opacity(0.7, self.data.get('color', "primary"))

        self.p.update()



    # Called when clicking on our timeline control
    def on_clicked(self, e):
        ''' Shows our timeline information display '''
        print("Timeline clicked")
        

    # Called when we need to rebuild out timeline UI
    def reload_widget(self):

        # Rebuild our tab to reflect any changes
        self.reload_tab()
        
        # TODO:
        # Clicking brings up a mini-menu in the timelines widget to show details and allow editing
        # Drag pp, arcs, timeskips to change their date/time??
        # Timeline object and all its children are gesture detectors
        # If event (pp, arc, etc.) is clicked on left side of screen bring mini widgets on right side, and vise versa
        # Time label is optional. Label vertial markers along the timeline with int and label if user provided



        # UI elements
        filters = ft.Row(scroll="auto", alignment=ft.MainAxisAlignment.START)     # Row to hold our filter options
        show_information_display = ft.Checkbox(         # Checkbox to show/hide information display
            label="Show Information Display",
            value=self.data['information_display']['visibility'], 
            on_change=lambda e: self.information_display.toggle_visibility(e)
        )
        filter_plot_points = ft.Checkbox(label="Show Plot Points", value=True)      # Checkbox to filter plot points
        filter_arcs = ft.Checkbox(label="Show Arcs", value=True)                    # Checkbox to filter arcs
        reset_zoom_button = ft.ElevatedButton("Reset Zoom", on_click=lambda e: print("reset zoom pressed"))         # Button to reset zoom level

        # Add our filter options to the filters row
        filters.controls = [filter_plot_points, filter_arcs]

        # Header that shows our filter options, as well as what timeliness are visible
        # Add reset zoom button later
        header = ft.Row(
            #wrap=True,     # Want to wrap when lots of filters, but forces into column instead of row
            alignment=ft.MainAxisAlignment.CENTER,
            scroll="auto",
            controls=[show_information_display, reset_zoom_button, filters],
        )

        

        # Row to hold our timeline edges and control
        timeline_row = ft.Row(
            spacing=0,
            controls=[
                ft.Container(width=20),
                self.timeline_left_edge,
                self.timeline_control,
                self.timeline_right_edge,
                ft.Container(width=20),
            ]
        )

        # Reset the content of our timeline control so we can rebuild it
        self.timeline_control.content = ft.Row(spacing=0, expand=True)

        # Called right after this to give us our list of division positions
        def _set_division_list(total: int)-> list[int]:

            # Calculate step size based on total width and number of divisions
            step = total / self.data.get('divisions', 10)

            # Our list may initially a float if not divisible evenly
            float_list = [i * step for i in range(self.data.get('divisions', 10) + 1)]

            # Convert to int list
            int_list = [int(i) for i in float_list]

            # Remove first and last item in list so we don't double up edges
            int_list = int_list[1:-1]

            # Return our list
            return int_list

        # Set our division list
        division_list = _set_division_list(201)

        # Add line segments so our timeline control isn't just flat
        for i in range(201):

            # Track if we are on a division
            not_division = True

            print(i)

            # Go through our divisions list. If we are on there, add vertical line, then break and continue
            for num in division_list:
                if i == num:
                    # Vertical line only
                    vertical_line = ft.GestureDetector(
                        on_enter=self.on_enter, on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
                        height=16, expand=True, 
                        content=ft.VerticalDivider(color=ft.Colors.with_opacity(0.7, "primary"), thickness=3, width=3),
                        data=i      # Set our data so we know where to add new items
                    )
                    self.timeline_control.content.controls.append(vertical_line)
                    not_division = False
                    break

            # If we are not a division, add a horizontal line segment
            if not_division:

                # Horizontal followed up by a vertical line
                horizontal_line = ft.GestureDetector(
                    on_enter=self.on_enter, on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
                    expand=True, height=16, 
                    content=ft.Divider(color=ft.Colors.with_opacity(0.7, "primary"), thickness=3), 
                    data=i      # Set our data so we know where to add new items
                )
                self.timeline_control.content.controls.append(horizontal_line)

            else:  
                continue
            


        # Create a stack so we can sit our plotpoints and arcs on our timeline
        timeline_stack = ft.Stack(
            expand=True, 
            alignment=ft.Alignment(0, 0),
            controls=[
                ft.Container(expand=True, ignore_interactions=True),    # Make sure we're expanded
                timeline_row
            ]
        )
        
        # Handler for timeline resize events
        for arc in self.arcs.values():


            # Add a stack so we can position our plot point control correctly by grabbing its alignment
            stack = ft.Stack(
                alignment=arc.x_alignment,
                expand=True,            # Make sure it fills the whole timeline width
                controls=[
                    ft.Container(expand=True, ignore_interactions=True),        # Make sure it fills the whole timeline width so alignment works
                    arc.timeline_control,            # Add the plotpoint control
                ]
            )
        
            # Add this temporary stack to the timeline stack
            timeline_stack.controls.append(stack)



        # Add our plot points to the timeline (They position themselves)
        for plot_point in self.plot_points.values():    

            # Add a stack so we can position our plot point control correctly by grabbing its alignment
            stack = ft.Stack(
                expand=True,            # Make sure it fills the whole timeline width
                controls=[
                    ft.Container(expand=True, ignore_interactions=True),        # Make sure it fills the whole timeline width so alignment works
                    plot_point.timeline_control,            # Add the plotpoint control
                ]
            )
        
            # Add this temporary stack to the timeline stack
            timeline_stack.controls.append(plot_point.timeline_control)


        timeline_stack.controls.append(self.new_item_container)
    


        # MAKE INVISIBLE IN FUTURE, ONLY EDGES ARE VERTICAL LINES
        # The timeline shown under our timeliness that that will display timeskips, etc. 
        timeline = ft.Container(
            margin=ft.margin.all(10),
            expand=True,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    timeline_stack,   
                ]
            )
        )

        # Make it so not have to rebuild interactive viewer every time??

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
    



        