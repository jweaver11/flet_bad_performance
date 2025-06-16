''' Master Story/Project class for projects'''
from workspaces.character.character_class import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Set title whenever new story is created
        print(self.title)

        self.characters = {}    # dict of characters name = name of character object

        self.active_widgets = {}   # Dict of active widgets


    # Workspaces within each story object
    # Content


    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??

    # Method to add new character object to story object
    def create_character(self, name):
        self.characters[name] = Character(name) # Add our character to the dict

story = Story("Story Title") 

# Class for widget objects in each story 
class Widget:
    def __init__(self, title, body):
        self.title = title
        self.body = body