'''
Our user of the application. This model stores their info and certain UI elements,
and their stories. It is a dead end file, that only imports the story model meaning...
All other files can import this function without issues
'''

from models.story import Story


class User:
    # Constructor
    def __init__(self):

        # Declares settings and workspace rail here, but we create/load them later in main
        self.settings = None
        self.all_workspaces_rail = None   # All workspaces rail
        
        # Dict of all our stories.
        self.stories = {}

        # For now, create the default story cuz loading logic is not implemented yet
        self.create_new_story("default_story")
        
        # Sets our active story, in this case the default story
        self.active_story = self.stories['default_story'] 


    # Called when user creates a new story
    def create_new_story(self, title: str) -> Story:
        ''' Creates the new story object, then saves it to a new folder '''
        
        # Create a new story object and add it to our stories dict
        new_story = Story(title)
        self.stories[title] = new_story
        # Save story dict (doesnt exist yet)

        return new_story

# Sets our global user object
user = User()