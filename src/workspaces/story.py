''' Master Story/Project class for projects'''
from workspaces.character.character_class import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Set title whenever new story is created

        # list of widgets which are just flet containers
        self.widgets = []  

        self.characters = {}    # dict of characters name = name of character object

        
    # Method to add new character object to story object
    def create_character(self, name):
        self.characters[name] = Character(name) # Add our character to the dict
        # Create our character widget
        self.widgets.append(self.characters[name].widget)  # Assign our char name as index for widget

    # Workspaces within each story object
    # Content


    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??


story = Story("Story Title") 
