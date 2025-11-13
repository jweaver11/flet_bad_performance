""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail
from styles.timelines.timeline_dropdown import Timeline_Dropdown
from styles.timelines.timeline_label import Timeline_Label
from styles.timelines.timeline_item import Timeline_Item
from styles.menu_option_style import Menu_Option_Style


# Class is created in main on program startup
class Timelines_Rail(Rail):

    # Constructor
    def __init__(self, page: ft.Page, story: Story):
        
        # Parent constructor
        super().__init__(
            page=page,
            story=story,
            directory_path=story.data['timelines_directory_path']
        )
 
        self.reload_rail()

    # Called recursively to load arcs (and sub arcs) and plotpoings within a timeline. Called in reload_rail
    def load_timeline_or_arc_data(
        self,                                           
        father,                                             # Either timeline or an arc
        father_dropdown: Timeline_Dropdown,                 # Dropdown created for parent arc
        arcs_dropdown_title: str = "Sub Arcs",              # Title for the arcs dropdown. We can overwrite this to 'arcs' for timelines
    ):    
        ''' Recursively loads the sub-arcs, plotpoints, and timeskips of an arc. Parent must be either arc or timeline'''


        

        # Create our label for plotpoints
        plot_points_label = Timeline_Label(
            title="Plot Points:",
            icon=ft.Icons.LOCATION_SEARCHING_OUTLINED,
            story=self.story,
            father=father,
        )       #Icons.LOCATION_PIN

        # Add our label to the father dropdown and add the textfield for new plotpoints
        father_dropdown.content.controls.append(plot_points_label)
        father_dropdown.content.controls.append(ft.Divider())
        father_dropdown.content.controls.append(father_dropdown.new_plot_point_textfield)
    
        # Go through our plotpoints from our parent arc or timeline, and add each item
        for plot_point in father.plot_points.values():
            father_dropdown.content.controls.append(
                Timeline_Item(title=plot_point.title, mini_widget=plot_point)
            )

        # Create our label for arcs
        arcs_label = Timeline_Label(
            title=f"{arcs_dropdown_title}:",
            icon=ft.Icons.ARCHITECTURE_OUTLINED,
            story=self.story,
            father=father,
        )

        # Add our label to the father dropdown and add the textfield for new arcs
        father_dropdown.content.controls.append(arcs_label)
        father_dropdown.content.controls.append(ft.Divider())
        father_dropdown.content.controls.append(father_dropdown.new_arc_textfield)

        # Go through all the arcs/sub arcs held in our parent arc or timeline
        for arc in father.arcs.values():

            # Create a new parent expansion tile we'll need for recursion
            sub_arc_expansion_tile = Timeline_Dropdown(arc.title, self.story, type="arc", father=father, additional_menu_options=self.get_sub_menu_options())
            
            # Create our label for plotpoints
            plot_points_label = Timeline_Label(
                title="Plot Points:",
                icon=ft.Icons.LOCATION_SEARCHING_OUTLINED,
                story=self.story,
                father=arc,
            )       #Icons.LOCATION_PIN

            # Add our label to the father dropdown and add the textfield for new plotpoints
            sub_arc_expansion_tile.content.controls.append(plot_points_label)
            sub_arc_expansion_tile.content.controls.append(ft.Divider())
            sub_arc_expansion_tile.content.controls.append(father_dropdown.new_plot_point_textfield)

            for plot_point in arc.plot_points.values():
                sub_arc_expansion_tile.content.controls.append(
                    Timeline_Item(title=plot_point.title, mini_widget=plot_point)
                )

            # Add the new parent expansion tile to our current parents expansion tile controls
            #arcs_expansion_tile.content.controls.append(sub_arc_expansion_tile)
            father_dropdown.content.controls.append(sub_arc_expansion_tile)
            

    # Called when a new timeline button is clicked
    def new_timeline_clicked(self, e):
        ''' Sets our textfield visibility, reset value, hint text, and data '''
        
        self.new_item_textfield.visible = True
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Timeline Title"
        self.new_item_textfield.data = "timeline"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()

    # New arcs
    def new_arc_clicked(self, e):
        ''' Sets our textfield visibility, reset value, hint text, data, and gives us the right timeline reference'''
        
        self.new_item_textfield.visible = True
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Arc Name"
        self.new_item_textfield.data = "arc"

        # Since this is only clicked when there's one timeline, we just grab it
        for timeline in self.story.timelines.values():
            self.timeline = timeline
        self.story.close_menu()

    # New plot points
    def new_plotpoint_clicked(self, e):
        ''' Handles setting our textfield for new plotpoint creation '''

        self.new_item_textfield.visible = True
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Plot Point Name"
        self.new_item_textfield.data = "plot_point"
        for timeline in self.story.timelines.values():
            self.timeline = timeline
        self.story.close_menu()

    # New time skips
    def new_timeskip_clicked(self, e):
        ''' Handles setting our textfield for new timeskip creation '''
        
        self.new_item_textfield.visible = True
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Time Skip Name"
        self.new_item_textfield.data = "time_skip"
        for timeline in self.story.timelines.values():
            self.timeline = timeline
        self.story.close_menu()


    # Called to return our list of menu options when right clicking on the timeline rail
    def get_menu_options(self) -> list[ft.Control]:
        ''' Returns our menu options for the timelines rail. In this case just timelines '''

        if len(self.story.timelines) == 1:
            return [
                Menu_Option_Style(
                    on_click=self.new_arc_clicked,
                    data="arc",
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED),
                        ft.Text("Arc", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                    ])
                ),
                Menu_Option_Style(
                    on_click=self.new_plotpoint_clicked,
                    data="plot_point",
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED),
                        ft.Text("Plot Point", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                    ])
                ),
                Menu_Option_Style(
                    on_click=self.new_timeline_clicked,
                    data="timeline",
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED),
                        ft.Text("Timeline", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                    ])
                ),
            ]

        else:
            return [
                Menu_Option_Style(
                    on_click=self.new_timeline_clicked,
                    data="timeline",
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADD_ROUNDED),
                        ft.Text("Timeline", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                    ])
                ),
            ]
    
    # Called when right clicking a timeline, arc, or the arc/plot point drop downs
    def get_sub_menu_options(self) -> list[ft.Control]:
        ''' Returns all possible menu options. The class that receives this option filters out what it needs '''

        return [
            # Create plot point button
            Menu_Option_Style(
                data="plot_point",
                content=ft.Row([
                    ft.Icon(ft.Icons.EVENT_OUTLINED),
                    ft.Text("Plot Point", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            # Create arc button
            Menu_Option_Style(
                data="arc",
                content=ft.Row([
                    ft.Icon(ft.Icons.EVENT_OUTLINED),
                    ft.Text("Arc", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            # Rename button
            Menu_Option_Style(
                #on_click=self.rename_clicked,
                content=ft.Row([
                    ft.Icon(ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED),
                    ft.Text(
                        "Rename", 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.ON_SURFACE
                    ), 
                ]),
            ),
            # Color changing popup menu
            Menu_Option_Style(
                content=ft.PopupMenuButton(
                    expand=True,
                    tooltip="",
                    padding=None,
                    content=ft.Row(
                        expand=True,
                        controls=[
                            ft.Icon(ft.Icons.COLOR_LENS_OUTLINED, color=ft.Colors.PRIMARY),
                            ft.Text("Color", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True), 
                            ft.Icon(ft.Icons.ARROW_DROP_DOWN_OUTLINED, color=ft.Colors.ON_SURFACE, size=16),
                        ]
                    ),
                    #items=self.get_color_options()
                )
            ),
            
            # Delete button
            Menu_Option_Style(
                #on_click=lambda e: self.delete_clicked(e),
                content=ft.Row([
                    ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED),
                    ft.Text("Delete", weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE, expand=True),
                ]),
            ),
        ]


    # Reload the rail whenever we need
    def reload_rail(self) -> ft.Control:
        ''' Reloads the plot and timeline rail, useful when switching stories '''

        # TIMELINES RAIL ONLY HAS THE ABILITY TO CREATE NEW TIMELINES, PLOTPOINTS, ETC. AND VIEW HOW THEY ARE ORGANIZED
        # ALTERING THEIR DATA IS DONE IN THEIR MINI WIDGETS
        # WHEN CREATING NEW PP OR ARC, ADD IT DEFAULT TO MIDDLE OF TIMELINE AND BE ABLE TO BE DRAGGED AROUND



        header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            
            controls=[

                # Add here, story name, and buttons to create new stuff.
                # As well as right click options here that work like normal.

                ft.Container(expand=True),

                ft.IconButton(
                    tooltip="New Timeline",
                    icon=ft.Icons.TIMELINE_OUTLINED,
                    on_click=self.new_timeline_clicked
                ),
                
                ft.Container(expand=True),
            ]
        )

        # Build the content of our rail
        content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
            controls=[]
        )

        # Run through each timeline in the story
        for timeline in self.story.timelines.values():

            # Create an expansion tile for our timeline that we need in order to load its data
            timeline_dropdown = Timeline_Dropdown(
                title=timeline.title, 
                story=self.story, 
                father=timeline, 
                type="timeline",
                additional_menu_options=self.get_sub_menu_options()
            )


            # Pass our timeline into the recursive loaded function to load its data
            self.load_timeline_or_arc_data( 
                father=timeline, 
                father_dropdown=timeline_dropdown,
                arcs_dropdown_title="Arcs"
            )

            # If theres only one timeline, no need to add the parent expansion to the page.
            if len(self.story.timelines) == 1:

                # Just Two dropdowns 
                content.controls.extend(timeline_dropdown.content.controls)

            # Otherwise, add the full expansion panel
            else:
                content.controls.append(timeline_dropdown)


        # Finally, add our new item textfield at the bottom
        content.controls.append(self.new_item_textfield)

        # Gesture detector to put on top of stack on the rail to pop open menus on right click
        gd = ft.GestureDetector(
            expand=True,
            on_secondary_tap=lambda e: self.story.open_menu(self.get_menu_options()),
            content=content,
        )

        # Set our content to be a column
        self.content = ft.Column(
            spacing=0,
            expand=True,
            controls=[
                header,
                ft.Divider(),
                gd
            ]
        )

        # Apply the changes to the page
        self.p.update()


    
