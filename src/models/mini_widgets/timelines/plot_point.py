import flet as ft
from models.mini_widget import Mini_Widget
from models.widget import Widget
from handlers.verify_data import verify_data
from models.widgets.timeline import Timeline


# Plotpoint mini widget object that appear on timelines and arcs
class Plot_Point(Mini_Widget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, father, page: ft.Page, key: str, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        
            owner=owner,        
            father=father,      # In this case, father is always a timeline or another arc
            page=page,          
            key=key,  
            data=data,    
        ) 
        

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "plot_point",           # Tag to identify what type of object this is
                'description': str,
                'events': list,                # Numbered list of events that occur at this plot point
                'x_alignment': float,          # Float between -1 and 1 on x axis of timeline. 0 is center
                'is_major': bool,              # If this plot point is a major event
                'date': str,                   # Date of the plot point
                'time': str,                   # Time of the plot point
                'color': "white",         # Color of the plot point on the timeline
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
                'new_x_alignment': 5000,       # Used as integer between -10,000-10,000 to calculate float x_alignment
            },
        )

        self.x_alignment = ft.Alignment(self.data.get('new_x_alignment', 0) /  10000, 0)
        #print("Initial x alignment:", self.x_alignment)

        # state used during dragging
        self.drag_bar = ft.Slider(
                    min=-100, 
                    visible=True,
                    max=100, 
                    value=50, 
                    divisions=200, 
                    interaction=ft.SliderInteraction.SLIDE_ONLY,
                    autofocus=False,
                    active_color=ft.Colors.TRANSPARENT,
                    inactive_color=ft.Colors.TRANSPARENT,
                    overlay_color=ft.Colors.with_opacity(.5, self.data.get('color', "primary")),
                    thumb_color=self.data.get('color', "primary"),
                    on_focus=lambda e: print("focused slider"),
                    on_change_start=lambda e: print("started changing slider"),     # Works as on_click method
                )
            
        

        self.timeline_control = ft.Stack(
            alignment=self.x_alignment,
            expand=True,            # Make sure it fills the whole timeline width
            controls=[
                ft.Container(expand=True, ignore_interactions=True),
                ft.Container(
                    #left=0, right=0, top=0, bottom=0,
                    #on_click=self.tapped,
                    expand=False,
                    content=ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.CLICK,
                        #on_enter=lambda e: print(self.data['color']),
                        expand=False,   
                        content=ft.CircleAvatar(radius=6, bgcolor=self.data.get('color', "white")),      # Visual representation on the timeline
                        #content=ft.Icon(ft.Icons.FIBER_MANUAL_RECORD),
                        on_horizontal_drag_update=self.is_dragging,
                        on_horizontal_drag_end=self.end_drag,
                        on_horizontal_drag_start=self.start_drag,
                        on_tap=self.tapped,
                    )
                    #ft.Icons.LOCATION_SEARCHING_OUTLINED
                ),
                self.drag_bar
            ]
        ) 


        self.reload_mini_widget()

    def change_x_position(self, e):
        new_position = float(e.control.value)
        print("new position:", new_position)

        self.data['x_alignment'] = new_position
        self.save_dict()

        self.x_alignment = ft.Alignment(self.data.get('x_alignment', 0), 0)
        
        self.owner.reload_widget()


    def tapped(self, e):
        print("Clicked plot point!")
        #self.p.overlay.append(ft.Slider(min=-100, max=100, value=50, divisions=200))
        self.drag_bar.visible = not self.drag_bar.visible
        #self.p.overlay.append(ft.Container(expand=True, bgcolor=ft.colors.BLACK54, content=ft.Center(content=ft.Slider(min=-100, max=100, value=50, divisions=200))))
        self.p.update()

    def start_drag(self, e):
        # remember starting alignment for this drag
        print("mouse x and y")
        print(self.owner.story.mouse_x)
        print(self.owner.story.mouse_y)
        



    def is_dragging(self, e: ft.DragUpdateEvent):

        #print(e)

        self.drag_x_change += e.delta_x


        print(e.local_x)

        #print("drag x change:", self.drag_x_change)

        #old_alignment = self.data.get("x_alignment", 0.0)
        #print("old x value:", old_alignment)

        #print(e)

        #new_alignment = old_alignment + (e.delta_x / 100)
        #print("new x value:", new_alignment)

        #self.data['x_alignment'] = new_alignment
        #self.save_dict()

        #self.x_alignment = ft.Alignment(new_alignment, 0)
        
        
        #self.reload_mini_widget()
        #self.owner.reload_widget()
        #self.reload_mini_widget()

    def end_drag(self, e):
        print("Ended drag!")

    def reload_timeline_control(self):
        self.timeline_control = ft.Stack(
            alignment=self.x_alignment,
            expand=True,            # Make sure it fills the whole timeline width
            controls=[
                ft.Container(expand=True, ignore_interactions=True),
                ft.Container(
                    expand=False,
                    content=ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.CLICK,
                        #on_enter=lambda e: print(self.data['color']),
                        expand=False,   
                        content=ft.CircleAvatar(radius=6, bgcolor=self.data.get('color', "white")),      # Visual representation on the timeline
                        #content=ft.Icon(ft.Icons.FIBER_MANUAL_RECORD)
                        on_horizontal_drag_update=self.is_dragging,
                        on_horizontal_drag_end=self.end_drag,
                        on_horizontal_drag_start=self.start_drag,
                        on_tap=self.tapped,
                    )
                    #ft.Icons.LOCATION_SEARCHING_OUTLINED
                ),
                self.drag_bar
            ]
        ) 

        #self.p.update()
        #pass


    def reload_mini_widget(self):

        self.reload_timeline_control()

        self.content_control = ft.TextField(
            hint_text="Change x position",
            on_submit=self.change_x_position,
            expand=True,
        )

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.delete_dict()
                ),
            ],
            expand=True,
        )

        self.p.update()