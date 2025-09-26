import flet as ft


# Data class for plot points on a timeline - change to branch as well later??
class Branch(ft.GestureDetector):

    def __init__(self, title: str, data: dict=None):

        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title  # Required, has no default
        self.data = data    # Optional, if none given, will be created with default values

        # Gives us default data if none was passed in
        if self.data is None:
            self.data = self.create_default_data()

    def create_default_data(self):
        return {
            'title': self.title,
            'start_date': "",
            'end_date': "",
            'involved_characters': [],
            'related_locations': [],
            'related_items': [],
            'other': "",
        }
    
    def on_hover(self, e: ft.HoverEvent):
        print(e)