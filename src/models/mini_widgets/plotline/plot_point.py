import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data
from models.mini_widgets.plotline.timeline import Timeline


# Data class for plot points on a timeline - change to branch as well later??
class Plot_Point(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], branch_line, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # Owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

        # Either the timeline or the branch MUST be passed in
        self.branch_line = branch_line    # The timeline this arc belongs to. Needed for certain functions
        

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "plot_point",           # Tag to identify what type of object this is
                'description': str,
                'is_major': bool,              # If this plot point is a major event
                'date': str,                   # Date of the plot point
                'time': str,                   # Time of the plot point
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        )

        self.reload_mini_widget()


    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.owner.delete_mini_widget(self)
                ),
            ],
            expand=True,
        )

        self.p.update()