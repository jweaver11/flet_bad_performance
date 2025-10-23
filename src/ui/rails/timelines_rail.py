""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail


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
    def submit_timeline(self, title: str,):
        ''' Creates a new timeline inside of the current story '''

        # Check if name is unique
        name_is_unique = True

        for timeline in self.story.plotline.timelines.values():
            if timeline.title == title:
                name_is_unique = False
                print("Plotline name already exists!")
                break
        
        if title == "plotline":
            name_is_unique = False
            print("Plotline name cannot be 'plotline' as it is reserved!")

        # Make sure the name is unique before creating
        if name_is_unique:

            # Calls story function to create a new plotline
            self.story.plotline.create_new_timeline(title)
            self.reload_rail(self.story)


    def submit_arc(self, e):
        ''' Creates a new arc object on the specified timeline '''

        # Our plotline title is stored in the data, while the new title is from the control value
        timeline_title = e.control.data
        arc_title = e.control.value

        # Go through each timeline until we find the right one
        for timeline in self.story.plotline.timelines.values():
            if timeline.title == timeline_title:
                timeline.create_arc(arc_title)
                print(f"New arc created on the {timeline_title} timeline. Name: {arc_title} ")
                self.reload_rail()     # Reload the rail to reflect the change and break the loop
                break
        

    # When new plotpoint is submitted
    def submit_plotpoint(self, e, story: Story):
        # Our plotline title is stored in the data, while the new title is from the control value
        timeline_title = e.control.data
        plotpoint_title = e.control.value

        # Go through each timeline until we find the right one
        for timeline in story.plotline.timelines.values():
            if timeline.title == timeline_title:
                timeline.create_plot_point(plotpoint_title)
                print(f"New plotpoint created on the {timeline_title} timeline. Name: {plotpoint_title} ")
                self.reload_rail(story)     # Reload the rail to reflect the change and break the loop
                break

    # Called when new timeskip is submitted
    def submit_timeskip(self, e, story: Story):
        ''' Creates a new timeskip object on the specified timeline '''

        # Our plotline title is stored in the data, while the new title is from the control value
        timeline_title = e.control.data
        timeskip_title = e.control.value

        # Go through each timeline until we find the right one
        for timeline in story.plotline.timelines.values():
            if timeline.title == timeline_title:
                timeline.create_time_skip(timeskip_title)
                print(f"New timeskip created on the {timeline_title} timeline Name: {timeskip_title} ")
                self.reload_rail(story)  # Reload the rail to reflect the change and break the loop
                break


    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''

        # PLOTLINE RAIL JUST HAS ABILITY TO CREATE NEW TIMELINES, PLOTPOINTS, ETC. AND VIEW HOW THEY ARE ORGANIZED
        # ALTERING THEM IS DONE IN THEIR MINI WIDGETS
        # WHEN CREATING NEW PP OR ARC, ADD IT DEFAULT TO MIDDLE OF TIMELINE AND BE ABLE TO BE DRAGGED AROUND

        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            scroll="auto",
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Text("Timelines:")
                # Add more controls here as needed
            ]
        )

        # Run through each plotline in the story
        for timeline in self.story.timelines.values():

            arcs_expansion_tile = ft.ExpansionTile(
                title=ft.Text("Arcs"),
                shape=ft.RoundedRectangleBorder(),
            )
            for arc in timeline.arcs.values():
                arcs_expansion_tile.controls.append(
                    ft.Text(arc.title),
                )
            arcs_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Arc",
                    expand=True,
                    on_submit=lambda e: self.submit_arc(e),
                    data=timeline.title,
                )
            )

            # Create an expansion tile for our plotpoints
            plot_points_expansion_tile = ft.ExpansionTile(
                title=ft.Text("Plot Points"),
                shape=ft.RoundedRectangleBorder(),
            )
            # Run through each plotpoint, and add it to our plotpoints expansion tile
            for plotpoint in timeline.plot_points.values():
                plot_points_expansion_tile.controls.append(
                    ft.Text(plotpoint.title)
                )
            # Add a text field at bottom to create new plotpoints
            plot_points_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Plot Point",
                    data=timeline.title,
                    on_submit=lambda e: self.submit_plotpoint(e),
                    expand=True,
                )
            )
            # TODO button that when pressed makes a textfield visible and autofocused when inputting plotpoint name

            time_skips_expansion_tile = ft.ExpansionTile(
                title=ft.Text("Time Skips"),
                shape=ft.RoundedRectangleBorder(),
            )
            for time_skip in timeline.time_skips.values():
                time_skips_expansion_tile.controls.append(
                    ft.Text(time_skip.title)
                )
            time_skips_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Time Skip",
                    expand=True,
                    on_submit=lambda e: self.submit_timeskip(e),
                    data=timeline.title,
                )
            )

            # Build our view for this plotline
            list_view = ft.ExpansionTile(
                shape=ft.RoundedRectangleBorder(),  # Get rid of edges of expansion tile
                
                #expand=True,
                #spacing=5,
                #padding=ft.padding.all(10),
                #auto_scroll=True,
                title=ft.Text(timeline.title),  # Set the title of expansion tile to the plotline
                controls=[
                    ft.Container(height=6), # Spacing
                    ft.Row([    # Add start date and end date text fields
                        ft.TextField(label="Start Date", value=str(timeline.data['start_date']), expand=True),
                        ft.TextField(label="End Date", value=str(timeline.data['end_date']), expand=True),
                    ]),

                    arcs_expansion_tile,    # Add our arcs expansion tile we built above

                    plot_points_expansion_tile,   # Add our plotpoints expansion tile we built above

                    time_skips_expansion_tile,
                ]
            )

            self.content.controls.append(list_view)
            self.content.controls.append(ft.Container(height=10))


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

            
        

        self.content.controls.append(
            ft.GestureDetector(
                content=ft.Text("GD"),
                on_secondary_tap=lambda e: open_menu(self.story),
                mouse_cursor="click",
            )
        )
        

        self.content.controls.append(ft.Container(height=20))

        self.content.controls.append(
            ft.TextField(label="Create New Timeline", on_submit=lambda e: self.submit_timeline(e.control.value, self.story)),
        )

        self.p.update()
    
