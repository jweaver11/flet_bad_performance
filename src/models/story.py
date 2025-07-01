''' Master Story/Project class for projects'''

# Class for each seperate story/project
# Only used for data storage, methods don't pass properly to update the UI
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story

        # Holds our widgets list.
        self.widgets = [
            # widget_object has control:ft.Container, title:str, tag:str, visible:bool
        ]

        # Hold our widgets in each pin area
        self.top_pin_widgets = []
        self.left_pin_widgets = []
        self.main_pin_widgets = []
        self.right_pin_widgets = []
        self.bottom_pin_widgets = []

        # Make a list for positional indexing
        self.characters = []    # Dict of character object. Used for storing/deleting characters

        

    # Workspaces within each story object
    # Description
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??

story = Story("Story Title") 
