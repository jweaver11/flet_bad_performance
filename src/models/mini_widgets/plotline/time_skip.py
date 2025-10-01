import flet as ft

class Time_Skip(ft.GestureDetector):

    def __init__(self, title: str, data: dict=None):
        super().__init__(
            on_enter=self.on_hover,
        )

        self.title = title
        self.data = data    # Optional, if none given, will be created with default values

        if self.data is None:
            self.data = self.create_default_data()

        
    def create_default_data(self):
        return {
            'title': self.title,
            'start_date': "",
            'end_date': "",
        }
    
    def on_hover(self, e: ft.HoverEvent):
        print(e)