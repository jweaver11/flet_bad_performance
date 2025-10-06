import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget


# Data class for plot points on a timeline - change to branch as well later??
class Plot_Point(MiniWidget):
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
            self.create_default_plot_point_data()  # Create data defaults for each chapter widget
            self.save_dict()    # Save our data to the file

        self.reload_mini_widget()

    
    # Have to save to plotline for mini widgets to function. 
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        if self.owner.data is None or not isinstance(self.owner.data, dict):
            print("Error: owner data is None, cannot save mini widget data")
            return

        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['plot_points'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()


    def create_default_plot_point_data(self):
        # Error catching
        if self.data is None or not isinstance(self.data, dict):
            # log("Data corrupted or did not exist, creating empty data dict")
            self.data = {}
        
        default_plot_point_data = {
            'title': self.title,
            'description': "",
            'is_major': False,
            'date': "",
            'time': "",
            'involved_characters': [],
            'related_locations': [],
            'related_items': [],

        }

        # Update existing data with any new default fields we added
        self.data.update(default_plot_point_data)  
        return


    def on_hover(self, e: ft.HoverEvent):
        print(e)

    def reload_mini_widget(self):

        self.content = ft.Column(
            [
                self.title_control,
                self.content_control,
            ],
            expand=True,
        )

        self.p.update()