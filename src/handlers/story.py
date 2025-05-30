''' Master Story/Project class for projects'''
from workspaces.character.character_pagelet import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    characters = []

    def __init__(self, title):
        self.title = title  # Set title whenever new story is created
        print(self.title)
        self.characters.append(Character("Billy"))
        print(self.characters[0].name)
        self.characters.append(Character("Johnny"))
        print(self.characters[1].name)

    
    # Workspaces within each story object
    # content
    #characters = []

    # plot_Timeline = ?
    # world_building = ?
    # drawing_board = ?
    Notes = []
    # Other workspaces??

    def create_character(self, name):
        self.characters.append(Character(name))
        print(self.characters[2].name)

        
    

# Creating new character object within story object
char2 = Character("character name 2")
story = Story("My story name")
story.characters[0] = char2

