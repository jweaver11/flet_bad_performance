
# Class for widgets
class Widget:
     def __init__(self, control, title, tag):
        self.control = control      # The rendered widget itself as a flet container
        self.title = title    # Title of the widget
        self.tag = tag        # Tag for tying widget to parent object, and auto sorting into pin lists
        self.visible = True      # bool if widget is visible
