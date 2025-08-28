'''
Our app of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model meaning...
All other files can import this function without issues
'''

from models.story import Story
import os
import flet as ft
from constants import data_paths


class App:
    # Constructor
    def __init__(self, page: ft.Page=None):

        #from models.settings import Settings

        # Declares settings and workspace rail here, but we create/load them later in main
        self.settings = None
        #self.all_workspaces_rail = None   # All workspaces rail
        
        # Dict of all our stories.
        self.stories = {}
        
        # Load existing stories from the directory
        #self.load_stories()
        
        # When settings is created, it uses default story if none exists
        #self.active_story = self.stories['default_story']

    # Called when opening a different story, or when new story is created
    def set_new_active_story(self) -> Story:
        ''' Sets a new active story based on the title given WIP '''

        print("Setting new active story called")

        # When settings is created, it uses default story if none exists
        #self.active_story = self.stories[self.settings.data['active_story']]


    # Called when app creates a new story
    def create_new_story(self, title: str) -> Story:
        ''' Creates the new story object, then saves it to a new folder WIP '''
        
        # Create a new story object and add it to our stories dict
        new_story = Story(title)
        self.stories[title] = new_story
        #self.active_story = new_story
        # Save story dict (doesnt exist yet)

        #self.set_new_active_story(title)

        return new_story
    
app = App()

# Sets our global app object
