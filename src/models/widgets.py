import flet as ft

# Class for widgets
class widgets:
     def __init__(self, title):
        widget = ft.Container() # The rendered widget itself as a flet container
        self.title = title  # Title of the widget
        visible = True  # bool if widget is visible
        tag = ""    # Tag for tying widget to parent object, and auto sorting into pin lists
