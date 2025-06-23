''' Master Story/Project class for projects'''

# Class for each seperate story/project
# Only used for data storage, methods don't pass properly to update the UI
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story
        self.visible_widgets = [] # Dict on widget title, object, and true/false for visibility
        self.characters = {}    # Dict of character object

        

    # Workspaces within each story object
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??

story = Story("Story Title") 
