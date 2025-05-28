''' Master Story/Project class for projects'''
from models.characters import characters_view
from models.characters import Character

# Class for each seperate story/project
class Story:
    # Page navigations
    characters = [Character]
    Notes = []

    # Constructor that sets the story name
    def __init__(self, name):
        self.name = name

    # Create our character 
    def CreateCharacter(self, character_name):
        # Create the character name
        self.name = character_name
        char3 = Character(self.name)
        self.characters[0] = char3
        return print(self.characters[0].name)
    

# Creating new character object within story object
char2 = Character("character name 2")
story = Story("story name")
story.characters[0] = char2

story.CreateCharacter("my brand new characters name")