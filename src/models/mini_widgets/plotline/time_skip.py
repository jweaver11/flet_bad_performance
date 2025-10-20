import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data
from models.mini_widgets.plotline.timeline import Timeline


class Time_Skip(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, dictionary_path: list[str], branch_line, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            dictionary_path=dictionary_path,  # Path to our dict WITHIN the owners json file. Mini widgets are stored in their owners file, not their own file
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

        self.branch_line = branch_line    # The timeline this arc belongs to. Needed for certain functions

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {   
                'tag': "time_skip",           # Tag to identify what type of object this is
                'start_date': str,
                'end_date': str,
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
                    on_click=lambda e: self.branch_line.delete_time_skip(self)
                ),
            ],
            expand=True,
        )

        self.p.update()