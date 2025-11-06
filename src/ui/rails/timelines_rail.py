""" WIP """

import flet as ft
from models.story import Story
from ui.rails.rail import Rail
from styles.timeline_expansion_tile import Timeline_Expansion_Tile
from styles.timeline_item import Timeline_Item
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

    # Called recursively to load arcs, plotpoints, and timeskips of either a parent timeline or arc
    def load_timeline_or_arc_data(
        self,                                           
        father,                                         # Either timeilne or an arc
        father_expansion_tile: ft.ExpansionTile,         # Dropdown created for either timeline or arc
        additional_directory_menu_options: list[ft.Control] = None,   # Additional menu options for right click on directory
    ):    
        ''' Recursively loads the sub-arcs, plotpoints, and timeskips of an arc. Parent must be either arc or timeline'''

        # Create our 3 expansion tile for our plotpoints, time skips, and arcs
        plot_points_expansion_tile = Timeline_Expansion_Tile("Plot Points", self.story)
        time_skips_expansion_tile = Timeline_Expansion_Tile("Time Skips", self.story)
        arcs_expansion_tile = Timeline_Expansion_Tile("Arcs", self.story)
    

        # Go through our plotpoints from our parent arc or timeline, and add each item
        for plot_point in father.plot_points.values():
            plot_points_expansion_tile.content.controls.append(
                ft.Text(plot_point.title),
                # Timeline_Item(plot_point.title)
            )

        # For timeskips
        for time_skip in father.time_skips.values():
            # Add each timeskip to the expansion tile
            time_skips_expansion_tile.content.controls.append(
                ft.Text(time_skip.title),
                # Timeline_Item(time_skip.title)
            )
        
        # Go through all the arcs/sub arcs held in our parent arc or timeline
        for arc in father.arcs.values():

            # Create a new parent expansion tile we'll need for recursion
            sub_arc_expansion_tile = Timeline_Expansion_Tile(arc.title, self.story)
            
            # Since its an arc, we need to recursively load its data as well
            self.load_timeline_or_arc_data(
                father=arc, 
                father_expansion_tile=sub_arc_expansion_tile,
                additional_directory_menu_options=additional_directory_menu_options
            )

            # Add the new parent expansion tile to our current parents expansion tile controls
            arcs_expansion_tile.content.controls.append(sub_arc_expansion_tile)
            

        # Add our three expansion tiles to the parent expansion tile
        father_expansion_tile.content.controls.append(plot_points_expansion_tile)
        father_expansion_tile.content.controls.append(time_skips_expansion_tile)
        father_expansion_tile.content.controls.append(arcs_expansion_tile)

    
    def new_timeline_clicked(self, e):
        ''' Handles setting our textfield for new timeline creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Timeline Title"
        self.new_item_textfield.data = "timeline"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()

    def new_arc_clicked(self, e):
        ''' Handles setting our textfield for new arc creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Arc Name"
        self.new_item_textfield.data = "arc"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()

    def new_plotpoint_clicked(self, e):
        ''' Handles setting our textfield for new plotpoint creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Plot Point Name"
        self.new_item_textfield.data = "plot_point"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()

    def new_timeskip_clicked(self, e):
        ''' Handles setting our textfield for new timeskip creation '''
        
        # Makes sure the right textfield is visible and the others are hidden
        self.new_item_textfield.visible = True

        # Set our textfield value to none, and the hint and data
        self.new_item_textfield.value = None
        self.new_item_textfield.hint_text = "Time Skip Name"
        self.new_item_textfield.data = "time_skip"

        # Close the menu (if ones is open), which will update the page as well
        self.story.close_menu()


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


    # Called to return our list of menu options for the content rail
    def get_menu_options(self) -> list[ft.Control]:
            
        # Builds our buttons that are our options in the menu
        return [
            Menu_Option_Style(
                on_click=self.new_category_clicked,
                data="arc",
                content=ft.Row([
                    ft.Icon(ft.Icons.ALARM_ADD_OUTLINED),
                    ft.Text("Arc", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                #on_click=self.new_character_clicked,
                data="plot_point",
                content=ft.Row([
                    ft.Icon(ft.Icons.EXPAND_CIRCLE_DOWN_OUTLINED),
                    ft.Text("Plot Point", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
            Menu_Option_Style(
                #on_click=self.new_character_clicked,
                data="time_skip",
                content=ft.Row([
                    ft.Icon(ft.Icons.FAST_FORWARD_OUTLINED),
                    ft.Text("Time skip", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
            ),
        ]
    
    def get_directory_menu_options(self) -> list[ft.Control]:
        return [
            Menu_Option_Style(
                data="character",
                content=ft.Row([
                    ft.Icon(ft.Icons.PERSON_ADD_ALT_OUTLINED),
                    ft.Text("Character", color=ft.Colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
                ])
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

            # Create an expansion tile for our timeline
            timeline_expansion_tile = Timeline_Expansion_Tile(title=timeline.title, story=self.story)

            # Pass our timeline into the recursive loaded function to load its data
            self.load_timeline_or_arc_data( 
                father=timeline, 
                father_expansion_tile=timeline_expansion_tile,
                additional_directory_menu_options=self.get_directory_menu_options()
            )

            # If theres only one timeline, no need to add the parent expansion to the page. Just add the content
            if len(self.story.timelines) == 1:
                content.controls.append(timeline_expansion_tile.content)

            # Otherwise, add the full expansion panel
            else:
                content.controls.append(timeline_expansion_tile)


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
    
