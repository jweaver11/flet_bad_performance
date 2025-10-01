import flet as ft

# Data class for arcs on a timeline - change to branch as well later??
class Arc(ft.GestureDetector):
    def __init__(self, title: str, data: dict=None):

        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title  # Required, has no default
        self.data = data    # Optional, if none given, will be created with default values

        if self.data is None:
            self.data = self.create_default_data()

   
    def create_default_data(self):
        return {
            'title': self.title,
            'description': "",
            'start_date': "",
            'end_date': "",
            'involved_characters': [],
            'related_locations': [],
            'related_items': [],
        }

    def on_hover(self, e: ft.HoverEvent):
        print(e)