''' Master Story/Project class for projects'''
from workspaces.character.character_class import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Set title whenever new story is created
        print(self.title)

        for char in self.character_list:
            print(char.name)


    # Workspaces within each story object
    # Content

    character_list_index : int
    character_list = []

    # Plot & imeline = ?
    # World Building = ?
    # Drawing Board = ?
    # Notes = []
    # Other workspaces??

    # Method to add new character object to story object
    def create_character(self, name):
        self.character_list.append(Character(name))

story = Story("Story Title") 