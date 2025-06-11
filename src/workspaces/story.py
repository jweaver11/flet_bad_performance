''' Master Story/Project class for projects'''
from workspaces.character.character_pagelet import Character


# Class for each seperate story/project
class Story:
    # Constructor for when new story is created
    def __init__(self, title):
        self.title = title  # Set title whenever new story is created
        print(self.title)
        self.character_list.append(Character("Billy"))  #temp
        self.character_list.append(Character("Johnny")) #temp
        self.character_list.append(Character("Willy")) #temp
        self.character_list.append(Character("Willy")) #temp
        self.character_list.append(Character("Wi")) #temp
        self.character_list.append(Character("Willy")) #temp
        self.character_list.append(Character("Willysdsdfgszxcvbnmlkjhg")) #temp

        for char in self.character_list:
            print(char.name)
        

        #active_workspace = "character" ?

    
    # Index workspaces to see which is active

    # Workspaces within each story object
    # content
    character_list = []
    # plot_Timeline = ?
    # world_building = ?
    # drawing_board = ?
    # Notes = []
    # Other workspaces??

    # Adds a new character object to story object
    def create_character(self, name):
        self.character_list.append(Character(name))
        # print(self.character_list[self.character_list(len)].name)

story = Story("Story Title") 