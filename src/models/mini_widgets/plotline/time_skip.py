import flet as ft
from models.mini_widget import MiniWidget
from models.widget import Widget
from handlers.verify_data import verify_data


class Time_Skip(MiniWidget):

    # Constructor. Requires title, owner widget, page reference, and optional data dictionary
    def __init__(self, title: str, owner: Widget, page: ft.Page, data: dict=None):

        # Parent constructor
        super().__init__(
            title=title,        # Title of our mini note
            owner=owner,      # owner widget that holds us
            page=page,          # Page reference
            data=data,          # Data if we're loading an existing mini note, otherwise blank
        ) 

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

    # Called when saving our mini widget data
    def save_dict(self):
        ''' Saves our current data to the OWNERS json file '''

        if self.owner.data is None or not isinstance(self.owner.data, dict):
            print("Error: owner data is None, cannot save mini widget data")
            return

        # Grab our owner object, and update their data pertaining to this mini widget
        self.owner.data['time_skips'][self.title] = self.data

        # Save our owners json file to match their data
        self.owner.save_dict()
        
    
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