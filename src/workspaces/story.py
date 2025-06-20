''' Master Story/Project class for projects'''
from workspaces.character.character import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story
        self.visible_widgets = [] # list of active widgets shown in main workspace area
        self.characters = {}    # dict of characters name = name of character object

        
    # Method to add new character object to story object
    def create_character(self, name):
        self.characters.update({name: Character(name)})
    
    def reorder_widgets(self):
        # mess with position of active_widgets elements
        return(print("reorder_widgets was called"))
        

    # Workspaces within each story object
    # Content
    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??


story = Story("Story Title") 
story.create_character("joe")
story.create_character("bob")

