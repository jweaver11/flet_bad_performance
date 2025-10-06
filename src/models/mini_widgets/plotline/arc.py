import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget


# Data class for arcs on a timeline - change to branch as well later??
class Arc(MiniWidget):
    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):
        # Check if we're loading an arc or creating a new one
        if data is None:
            loaded = False
        else:
            loaded = True

        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        )

        # If our character is new and not loaded, give it default data
        if not loaded:
            self.create_default_arc_data()  # Create data defaults for each chapter widget
            self.save_dict()    # Save our data to the file

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

    # Have to save to plotline for mini widgets to function. 
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        if self.owner.data is None:
            print("Error: owner data is None, cannot save mini widget data")
            return

        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['arcs'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()

    # Called when creating a new arc object
    def create_default_arc_data(self):
        ''' Gives default data for all arc objects '''

        default_arc_data = {
            
            'tag': "arc",
   
            'description': "",
            'start_date': "",
            'end_date': "",
            'events': [],       # Step by step of plot events through the arc. Call plot point??
            'involved_characters': [],
            'related_locations': [],
            'related_items': [],
        }

        # Update existing data with any new default fields we added
        self.data.update(default_arc_data)
        return

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