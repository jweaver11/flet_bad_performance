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
                        value=str(story.timeline.data['story_start_date']),
                        expand=True,
                    ),
                    ft.TextField(
                        label="End Date",
                        value=str(story.timeline.data['story_end_date']),
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

        for key, plotline in story.timeline.plotlines.items():
            list_view = ft.ExpansionTile(
                shape=ft.RoundedRectangleBorder(),
                
                #expand=True,
                #spacing=5,
                #padding=ft.padding.all(10),
                #auto_scroll=True,
                title=ft.Text(plotline.title),
                controls=[
                    ft.Container(height=6),
                    ft.Row([
                        ft.TextField(label="Start Date", value=str(plotline.data['start_date']), expand=True),
                        ft.TextField(label="End Date", value=str(plotline.data['end_date']), expand=True),
                    ]),
                    ft.ExpansionTile(title=ft.Text("Branches")),
                    ft.ExpansionTile(title=ft.Text("Plot Points")),
                    ft.ExpansionTile(title=ft.Text("Arcs")),
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
            ft.TextField(label="Create New Plotline", on_submit=lambda e: self.create_plotline(e.control.value, story)),
        )

        self.p.update()

    # Called when user creates a new plotline
    def create_plotline(self, title: str, story: Story):
        ''' Creates a new plotline branch inside of the current story '''

        # Check if name is unique
        name_is_unique = True

        for key, plotline in story.timeline.plotlines.items():
            if plotline.title == title:
                name_is_unique = False
                print("Plotline name already exists!")
                break

        if name_is_unique:

            # Calls story function to create a new plotline
            story.timeline.create_plotline(title)
            self.reload_rail(story)
        
        print(len(story.timeline.plotlines))
