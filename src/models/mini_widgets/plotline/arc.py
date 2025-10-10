import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data


# Data class for arcs on a timeline - change to branch as well later??
class Arc(MiniWidget):
    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        
        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

        # Verify our loaded data to make sure it has all the fields we need, and pass in our child class tag
        verify_data(
            self,   # Pass in our own data so the function can see the actual data we loaded
            {
                'content': str,
                'description': str,
                'start_date': str,
                'end_date': str,
                'events': list,       # Step by step of plot events through the arc. Call plot point??
                'involved_characters': list,
                'related_locations': list,
                'related_items': list,
            },
            tag="arc"
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

    # Called when saving our mini widget data
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        if self.owner.data is None or not isinstance(self.owner.data, dict):
            print("Error: owner data is None, cannot save mini widget data")
            return

        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['arcs'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()

    def on_hover(self, e: ft.HoverEvent):
        print(e)

    def submit_description_change(self, e):
        self.data['description'] = e.control.value
        self.save_dict()

    # Called after any changes happen to the data that need to be reflected in the UI
    def reload_mini_widget(self):
        ''' Reloads our mini widget UI based on our data '''

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
            ],
            expand=True,
        )

        self.p.update()