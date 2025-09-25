""" WIP """

import flet as ft
from models.story import Story


# Class is created in main on program startup
class Timeline_Rail(ft.Container):
    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Initialize the parent Container class first
        super().__init__()
            
        self.p = page

        self.reload_rail(story)

    # Reload the rail whenever we need
    def reload_rail(self, story: Story) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''
        

        # Build the content of our rail
        self.content = ft.Column(
            spacing=0,
            expand=True,
            scroll="auto",
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(height=10),
                ft.Row([
                    ft.TextField(
                        label="Start Date",
                        value=str(story.plotline.data['story_start_date']),
                        expand=True,
                    ),
                    ft.TextField(
                        label="End Date",
                        value=str(story.plotline.data['story_end_date']),
                        expand=True
                    ),
                ]),
               
                ft.Container(height=20),

                # Add more controls here as needed
            ]
        )

        self.content.controls.append(
            ft.Text("Plotlines:")
   
        )

        # Run through each plotline in the story
        for timeline in story.plotline.timelines.values():
            # Create an expansion tile for our plotpoints
            plotpoint_expansion_tile = ft.ExpansionTile(
                title=ft.Text("Plot Points"),
            )
            # Run through each plotpoint, and add it to our plotpoints expansion tile
            for plotpoint in timeline.plotpoints.values():
                plotpoint_expansion_tile.controls.append(
                    ft.Text(plotpoint.title)
                )
            # Add a text field at bottom to create new plotpoints
            plotpoint_expansion_tile.controls.append(
                ft.TextField(
                    label="Create Plot Point",
                    data=timeline.title,
                    on_submit=lambda e: self.submit_plotpoint(e, story),
                    expand=True,
                )
            )
            # TODO button that when pressed makes a textfield visible and autofocused to input plotpoint name

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

                    plotpoint_expansion_tile,   # Add our plotpoints expansion tile we built above

                    ft.ExpansionTile(title=ft.Text("Branches"), shape=ft.RoundedRectangleBorder()),
                    ft.ExpansionTile(title=ft.Text("Arcs"), shape=ft.RoundedRectangleBorder()),
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
                on_secondary_tap=lambda e: open_menu(story),
                mouse_cursor="click",
            )
        )
        

        self.content.controls.append(ft.Container(height=20))

        self.content.controls.append(
            ft.TextField(label="Create New Timeline", on_submit=lambda e: self.create_timeline(e.control.value, story)),
        )

        self.p.update()

    # Called when user creates a new plotline
    def create_timeline(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''

        # Check if name is unique
        name_is_unique = True

        for timeline in story.plotline.timelines.values():
            if timeline.title == title:
                name_is_unique = False
                print("Plotline name already exists!")
                break

        if name_is_unique:

            # Calls story function to create a new plotline
            story.plotline.create_new_timeline(title)
            self.reload_rail(story)
        


    # When new plotpoint is submitted
    def submit_plotpoint(self, e, story: Story):
        plotline_title = e.control.data
        plotpoint_title = e.control.value
        print(plotline_title)
        print(plotpoint_title)

        for timeline in story.plotline.timelines.values():
            if timeline.title == plotline_title:
                timeline.create_plotpoint(plotpoint_title)
                print(f"New plotpoint created on the {plotline_title} plotline. Name: {plotpoint_title} ")
                self.reload_rail(story)
                break

