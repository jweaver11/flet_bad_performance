''' Master Story/Project class for projects'''
from workspaces.character.character_pagelet import characters_view
from workspaces.character.character_pagelet import Character

# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title
    
    # Workspaces within each story object
    # content
    characters = []
    # plot_Timeline = ?
    # world_building = ?
    # drawing_board = ?
    Notes = []
    # Other workspaces??
    

# Creating new character object within story object
char2 = Character("character name 2")
story = Story("story name")
story.characters[0] = char2