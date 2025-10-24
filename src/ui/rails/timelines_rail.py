""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail
from styles.styles import Timeline_Expansion_Tile


# Class is created in main on program startup
class Timelines_Rail(Rail):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Rail class first
        super().__init__(
            page=page,
            story=story
        )
 
        self.reload_rail()

    # Called when user creates a new plotline
    def submit_timeline(self, title: str):
        ''' Creates a new timeline inside of the current story '''

        # Check if name is unique
        name_is_unique = True

        for timeline in self.story.timelines.values():
            if timeline.title == title:
                name_is_unique = False
                print("Plotline name already exists!")
                break

        # Make sure the name is unique before creating
        if name_is_unique:

            # Calls story function to create a new plotline
            self.story.create_timeline(title)

    # Called when new arc is submitted 
    def submit_arc(self, e, parent):
        ''' Creates a new arc on the parent arc or timeline '''

        # Our plotline title is stored in the data, while the new title is from the control value
        arc_title = e.control.value

        # Go through each timeline until we find the right one
        for arc in parent.arcs.values():
            if arc.title == arc_title:
                print("Arc name already exists!")
                return
            
        # Otherwise create the arc
        parent.create_arc(arc_title)
        print(f"New arc created on the {parent.title} arc or timeline. Name: {arc_title} ")
                
        

    # When new plotpoint is submitted
    def submit_plotpoint(self, e, parent):
        ''' Creates a new plotpoint on the parent arc or timeline '''
        
        plot_point_title = e.control.value

        # Go through each timeline until we find the right one
        for plot_point in parent.plot_points.values():
            if plot_point.title == plot_point_title:
                print("Arc name already exists!")
                return
            
        # Otherwise create the arc
        parent.create_plot_point(plot_point_title)
        print(f"New arc created on the {parent.title} arc or timeline. Name: {plot_point_title} ")

    # Called when new timeskip is submitted
    def submit_timeskip(self, e, parent):
        ''' Creates a new timeskip on the parent arc or timeline '''

        time_skip_title = e.control.value

        # Go through each timeline until we find the right one
        for time_skip in parent.time_skips.values():
            if time_skip.title == time_skip_title:
                print("Arc name already exists!")
                return
            
        # Otherwise create the timeskip
        parent.create_time_skip(time_skip_title)
        print(f"New arc created on the {parent.title} arc or timeline. Name: {time_skip_title} ")


    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''
        from models.widgets.timeline import Timeline

        # TIMELINES RAIL ONLY HAS THE ABILITY TO CREATE NEW TIMELINES, PLOTPOINTS, ETC. AND VIEW HOW THEY ARE ORGANIZED
        # ALTERING THEM IS DONE IN THEIR MINI WIDGETS
        # WHEN CREATING NEW PP OR ARC, ADD IT DEFAULT TO MIDDLE OF TIMELINE AND BE ABLE TO BE DRAGGED AROUND


        # Called recursively to load arcs, plotpoints, and timeskips of either a timeline or arc
        def _load_timeline_or_arc_data(parent, parent_expansion_tile: ft.ExpansionTile):    
            ''' Recursively loads the sub-arcs, plotpoints, and timeskips of an arc. Parent must be either arc or timeline'''

            # Create an expansion tile for our plotpoints, time skips, and arcs
            plot_points_expansion_tile = Timeline_Expansion_Tile("Plot Points")
            time_skips_expansion_tile = Timeline_Expansion_Tile("Time Skips")
            arcs_expansion_tile = Timeline_Expansion_Tile("Arcs")
        

            # Go through our plotpoints from our parent arc or timeline
            for plot_point in parent.plot_points.values():

                # Add each plot point to the expansion tile
                plot_points_expansion_tile.controls.append(
                    ft.Text(plot_point.title),
                )


            # Go through our timeskips from our parent arc or timeline
            for time_skip in parent.time_skips.values():

                # Add each timeskip to the expansion tile
                time_skips_expansion_tile.controls.append(
                    ft.Text(time_skip.title),
                )
            

            # Go through all the sub arcs held in our parent arc or timeline
            for sub_arc in parent.arcs.values():

                # Create a new parent expansion tile we'll need for recursion
                sub_arc_expansion_tile = Timeline_Expansion_Tile(sub_arc.title)

                # Add the new parent expansion tile to our current parents expansion tile controls
                arcs_expansion_tile.controls.append(sub_arc_expansion_tile)
                
                # Recursively load them, passing in our new parent and parent expansion tile
                _load_timeline_or_arc_data(parent=sub_arc, parent_expansion_tile=sub_arc_expansion_tile)
                

            # Add text field to create new plot points 
            plot_points_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Plot Point",
                    data=timeline.title,
                    on_submit=lambda e: self.submit_plotpoint(e, parent),
                    expand=True,
                )
            )

            # Add text field to create new time skips
            time_skips_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Time Skip",
                    expand=True,
                    on_submit=lambda e: self.submit_timeskip(e, parent),
                    data=timeline.title,
                )
            )

            # Add text field to create new sub arcs
            arcs_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Arc" if isinstance(parent, Timeline) else "Create Sub-Arc",
                    expand=True,
                    on_submit=lambda e: self.submit_arc(e, parent),
                    data=parent.title,
                )
            )

            # Add our three expansion tiles to the parent expansion tile

            parent_expansion_tile.controls.append(plot_points_expansion_tile)
            parent_expansion_tile.controls.append(time_skips_expansion_tile)
            parent_expansion_tile.controls.append(arcs_expansion_tile)


            

        # Set our content to be a column for a top down view
        self.content = ft.Column(
            spacing=0,
            expand=True,
            scroll="auto",
            alignment=ft.MainAxisAlignment.START,
            controls=[],
        )

        # Run through each timeline in the story
        for timeline in self.story.timelines.values():

            # Create an expansion tile for our timeline
            timeline_expansion_tile = Timeline_Expansion_Tile(title=timeline.title, scale=1.0)

            # Take our data, and add it to the rail under each timeline
            _load_timeline_or_arc_data(parent=timeline, parent_expansion_tile=timeline_expansion_tile)

            # Add our expansion tile to the rail content
            self.content.controls.append(timeline_expansion_tile)
            self.content.controls.append(ft.Container(height=10))

            # If theres only one timeline, no need to add the parent expansion to the page
            if len(self.story.timelines) == 1:
                self.content.controls = timeline_expansion_tile.controls
                break


        def open_menu(story: Story):
            
            #print(f"Open menu at x={story.mouse_x}, y={story.mouse_y}")

            def close_menu(e):
                self.p.overlay.clear()
                self.p.update()
            
            menu = ft.Container(
                left=story.mouse_x,     # Positions the menu at the mouse location
                top=story.mouse_y,
                border_radius=ft.border_radius.all(6),
                bgcolor=ft.Colors.ON_SECONDARY,
                padding=2,
                alignment=ft.alignment.center,
                content=ft.Column([
                    ft.TextButton("Option 1"),
                    ft.TextButton("Option 2"),
                    ft.TextButton("Option 3"),
                ]),
            )
            outside_detector = ft.GestureDetector(
                expand=True,
                on_tap=close_menu,
                on_secondary_tap=close_menu,
            )

            self.p.overlay.append(outside_detector)
            self.p.overlay.append(menu)
            
            self.p.update()

            
        self.content.controls.append(ft.Container(height=50))

        self.content.controls.append(
            ft.GestureDetector(
                content=ft.Text("GD"),
                on_secondary_tap=lambda e: open_menu(self.story),
                mouse_cursor="click",
            )
        )
        

        self.content.controls.append(ft.Container(height=20))

        self.content.controls.append(
            ft.TextField(label="Create New Timeline", on_submit=lambda e: self.submit_timeline(e.control.value)),
        )

        self.p.update()
    
