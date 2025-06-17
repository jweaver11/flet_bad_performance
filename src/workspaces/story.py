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

        # Add our character widget from the new char object above to our widgets list. 
        # Use bool to determine what all goes on the widget list, but default goes on
        self.widgets.append(self.characters[name].widget)
        print(f"# of active widgets: ", len(self.widgets))


    def reload_widgets(self):
        self.widgets.clear()
        for char_name in self.characters:
            character_obj = self.characters[char_name]
            if character_obj.visible == True:        # This line is the error
                self.widgets.append(character_obj.widget)

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
