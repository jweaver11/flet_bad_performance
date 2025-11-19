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
                'x_position': int,             # X position on the timeline
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
            #alignment=ft.Alignment(-1, 0),
            left=self.data['x_position'],                                       # X position on the timeline                                     
            bottom=0, top=0,                                                    # Stick it vertically in middle of the stack
            content=ft.CircleAvatar(radius=6, bgcolor=self.data['color'])      # Visual representation on the timeline
            #content=ft.Container(shape=ft.BoxShape.CIRCLE, width=12, height=12, bgcolor=self.data['color'])
            #content=ft.Icon(ft.Icons.LOCATION_SEARCHING_OUTLINED, color=self.data['color'], size=16)
        )      

        self.reload_mini_widget()


    def reload_mini_widget(self):

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