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
                'x_alignment': float,          # -1 -> 1 for left to right
                'is_major': bool,              # If this plot point is a major event
                'date': str,                   # Date of the plot point
                'time': str,                   # Time of the plot point
                'color': "on_secondary",       # Color of the plot point on the timeline
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        )

        self.timeline_control = ft.Container(
            alignment=ft.Alignment(self.data.get('x_alignment', 0), 0),
            content=ft.CircleAvatar(radius=6, bgcolor=self.data['color'])      # Visual representation on the timeline
            #ft.Icons.LOCATION_SEARCHING_OUTLINED
        )      


        self.reload_mini_widget()

    def change_x_position(self, e):
        new_position = float(e.control.value)
        print("new position:", new_position)

        self.data['x_alignment'] = new_position
        self.save_dict()
        
        self.timeline_control.alignment = ft.Alignment(self.data.get('x_alignment', 0), 0)
        
        self.owner.reload_widget()


    def reload_mini_widget(self):

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