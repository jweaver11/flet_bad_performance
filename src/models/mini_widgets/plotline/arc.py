import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data

# Data class for arcs on a timeline - change to branch as well later??
class Arc(MiniWidget):
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

        # The timeline or branch this arc belongs to
        self.branch_line = branch_line    # The timeline this arc belongs to. Needed for certain functions

        # Verifies this object has the required data fields, and creates them if not
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'tag': "arc",           # Tag to identify what type of object this is
                'content': str,
                'description': str,
                'start_date': str,
                'end_date': str,
                'events': list,       # Step by step of plot events through the arc. Call plot point??
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
        )

        # The control that will be displayed on our timeline for this arc, while the arc object is a mini widget
        self.timeline_control = ft.GestureDetector(
            on_enter=self.on_hover,
        )

        # Temp testing
        self.timeline_control = ft.TextButton(
            text=self.title,
            on_click=self.toggle_visibility,
        )


        self.title_control = ft.TextField(
            value=self.title,
            label=None,
        )

        self.content_control = ft.TextField(
            #value=self.data['content'],
            label="Body",
            expand=True,
            multiline=True,
            on_change=self.submit_description_change,
        )

        self.reload_mini_widget()


    def submit_description_change(self, e):
        self.data['description'] = e.control.value
        self.save_dict()

    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
                ft.TextButton(
                    "Delete ME", 
                    on_click=lambda e: self.branch_line.delete_arc(self)
                ),
            ],
            expand=True,
        )

        self.p.update()