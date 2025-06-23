''' Master Story/Project class for projects'''
from workspaces.character.character import Character
from handlers.layout_widgets import layout_widgets


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Title of story
        self.visible_widgets = [] # list of active widgets shown in main workspace area
        self.characters = {}    # dict of characters name = name of character object

        
    # Method to add new character object to story object
    def create_character(self, name):
        self.characters.update({name: Character(name, self)})
        story.visible_widgets.append(self.characters[name].widget)   # auto open new widgets on creation

    # Reload our widget list and how widget_row to hold our widgets
    # Passes in a story object
    def reload_widgets(self):
        self.visible_widgets.clear()    # clear our visible widget list
        for key, character in self.characters.items():
            print(f"{key}: visible={character.visible}")
            if character.visible == True:        # This line is the error
                self.visible_widgets.append(character.widget)    # Make our list current with visible widgets


        layout_widgets(self.visible_widgets) # layout our widgets, and update everything
    
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
