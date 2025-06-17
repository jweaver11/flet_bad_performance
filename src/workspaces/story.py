''' Master Story/Project class for projects'''
from workspaces.character.character_class import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Set title whenever new story is created
        self.active_widgets = []  # list of active widgets shown in main workspace area
        self.characters = {}    # dict of characters name = name of character object

        
    # Method to add new character object to story object
    def create_character(self, name):
        self.characters[name] = Character(name) # Add our character to the dict

        self.active_widgets.append(self.characters[name].widget)    # Auto add created characters to the active widgets

    # reload our widget list used to render the workspace widgets
    def reload_widgets(self, row):
        self.active_widgets.clear()
        row.controls.clear()    # clear widgets-row
        for char_name in self.characters:
            character_obj = self.characters[char_name]
            if character_obj.visible == True:        # This line is the error
                self.active_widgets.append(character_obj.widget)
        row.controls = self.active_widgets

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
