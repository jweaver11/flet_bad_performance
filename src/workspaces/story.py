''' Master Story/Project class for projects'''
from workspaces.character.character_class import Character
from handlers.layout_widgets import layout_widgets


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

    # Reload our widget list and how widget_row to hold our widgets
    # passes in whatever flet control holds our other controls
    def reload_widgets(self):
        self.active_widgets.clear()
        for char_name in self.characters:
            character_obj = self.characters[char_name]
            if character_obj.visible == True:        # This line is the error
                self.active_widgets.append(character_obj.widget)    # Make our list current with visible widgets

        layout_widgets(self.active_widgets)
    
    def reorder_widgets(self):
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
story.create_character("steve")
