'''
Our app of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model meaning...
All other files can import this function without issues
'''

from models.story import Story
import flet as ft
from models.widget import Widget


class App:

    # Constructor
    def __init__(self):

        # Declares settings and workspace rail here, but we create/load them later in main
        self.settings: Widget = ft.Container()
        
        # Dict of all our stories.
        self.stories = {}
        
        

    # Called when app creates a new story. Accepts our title, page reference, a template, and a type
    def create_new_story(self, title: str, page: ft.Page, template: str) -> Story:
        ''' Creates the new story object and has it run its 'startup' method. Changes route so our view displays the new story '''

        # TODO: Add a type to accept for novel/comic
        
        # Create a new story object and add it to our stories dict
        self.stories[title] = Story(title, page, data=None, template=template)

        # Opens this new story as the active one on screen
        page.route = self.stories[title].route

        
    
# Sets our global app object that main uses and some functions call
app = App()

