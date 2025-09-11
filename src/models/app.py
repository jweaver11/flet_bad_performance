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

    # Called when app creates a new story
    def create_new_story(self, title: str, page: ft.Page, template: str) -> Story:
        ''' Creates the new story object, then saves it to a new folder WIP '''
        #from handlers.reload_workspace import reload_workspace
        
        # Create a new story object and add it to our stories dict
        self.stories[title] = Story(title, page, template)
        self.stories[title].startup()

        page.route = self.stories[title].route

        
    
app = App()

# Sets our global app object
