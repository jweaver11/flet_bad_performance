''' Master Story/Project class for projects'''

# Class for each seperate story/project
# Only used for data storage, methods don't pass properly to update the UI
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story

        # Make a list for positional indexing
        # Need this that will tie widgets to parent objects names, but can be reordered independently
        self.widgets = {    # Dict of all the widgets in the story
            # 'widget_name': widget_object, bool,
        } 

        self.visible_widgets = []  # List of widgets that are currently visible

        # Make a list for positional indexing
        self.characters = {}    # Dict of character object. Used for storing/deleting characters

        

    # Workspaces within each story object
    # Description
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??

story = Story("Story Title") 
